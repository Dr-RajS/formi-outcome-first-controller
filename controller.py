#!/usr/bin/env python3
"""HTTP-only outcome controller with durable event ingestion and audit."""
import argparse, copy, json, math, os, sqlite3
import httpx

class Store:
 def __init__(self,path):
  self.d=sqlite3.connect(path,timeout=30); self.d.execute('PRAGMA journal_mode=WAL'); self.d.execute('PRAGMA synchronous=FULL')
  self.d.executescript('''CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY,v TEXT); CREATE TABLE IF NOT EXISTS events(event_id INTEGER PRIMARY KEY,chunk INTEGER,body TEXT); CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY,ts TEXT,wf TEXT,action TEXT,detail TEXT); CREATE TABLE IF NOT EXISTS proposals(pid TEXT PRIMARY KEY,wf TEXT,aid TEXT,status TEXT,base INTEGER,cfg TEXT,ts TEXT); CREATE TABLE IF NOT EXISTS metrics(wf TEXT,dim TEXT,val TEXT,cohort TEXT,n INTEGER,p INTEGER,gn INTEGER,g INTEGER,PRIMARY KEY(wf,dim,val,cohort));'''); self.d.commit()
 def get(self,k,default=None):
  r=self.d.execute('SELECT v FROM kv WHERE k=?',(k,)).fetchone(); return json.loads(r[0]) if r else default
 def set(self,k,v): self.d.execute('INSERT INTO kv VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=excluded.v',(k,json.dumps(v))); self.d.commit()
 def audit(self,ts,wf,a,x): self.d.execute('INSERT INTO audit(ts,wf,action,detail) VALUES(?,?,?,?)',(ts,wf,a,json.dumps(x,sort_keys=True))); self.d.commit()
 def add_event(self,e,ch,wfs):
  try: self.d.execute('INSERT INTO events VALUES(?,?,?)',(int(e.get('event_id',-1)),ch,json.dumps(e)))
  except sqlite3.IntegrityError: return False
  if e.get('type')=='call':
   wf=e['workflow_id']; obj=wfs.get(wf,{}).get('objective',{}).get('primary','engagement_rate'); cohort=e.get('cohort_id','default')
   for dim in ('voice','welcome_message','caller_id'):
    v=e.get('variant',{}).get(dim)
    if v is None: continue
    p=int(bool(e.get('connected'))); g=int(bool(e.get('engaged'))) if e.get('connected') else 0
    self.d.execute('''INSERT INTO metrics VALUES(?,?,?,?,1,?,?,?) ON CONFLICT(wf,dim,val,cohort) DO UPDATE SET n=n+1,p=p+excluded.p,gn=gn+excluded.gn,g=g+excluded.g''',(wf,dim,str(v),cohort,p,p,g))
  return True
 def stats(self,wf,dim,cohort='default'):
  return {v:{'n':n,'p':p,'gn':gn,'g':g} for v,n,p,gn,g in self.d.execute('SELECT val,n,p,gn,g FROM metrics WHERE wf=? AND dim=? AND cohort=?',(wf,dim,cohort))}

def lo(x,n,z=1.96):
 if not n:return 0
 p=x/n; d=1+z*z/n; return (p+z*z/(2*n)-z*math.sqrt((p*(1-p)+z*z/(4*n))/n))/d
def hi(x,n,z=1.96):
 if not n:return 1
 p=x/n; d=1+z*z/n; return (p+z*z/(2*n)+z*math.sqrt((p*(1-p)+z*z/(4*n))/n))/d
def wins(base,cand,primary):
 if not base or not cand: return False
 n1,n2=base['n'],cand['n']; x1,x2=base['p'],cand['p']
 if primary=='engagement_rate': n1,n2=base['gn'],cand['gn']; x1,x2=base['g'],cand['g']
 return n1>=100 and n2>=100 and lo(x2,n2)>hi(x1,n1)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--url',required=True); ap.add_argument('--db',default='controller_state.sqlite3'); ap.add_argument('--tick',type=int,default=60); a=ap.parse_args()
 s=Store(a.db); c=httpx.Client(base_url=a.url,timeout=120); wfs={w['workflow_id']:w for w in c.get('/workflows').json()}; last=s.get('last_chunk',-1)
 if last<0:
  for ch in c.get('/events/chunks',params={'kind':'history'}).json():
   for ln in c.get(f"/events/chunks/{ch['chunk']}").text.splitlines():
    if ln.strip(): s.add_event(json.loads(ln),ch['chunk'],wfs)
   last=max(last,ch['chunk'])
  s.set('last_chunk',last); s.audit('D0',None,'bootstrap',{'history_chunk':last})
 pending={wf:aid for wf,aid in s.d.execute("SELECT wf,aid FROM proposals WHERE status='pending' AND aid IS NOT NULL")}
 # Reconcile remote approvals by durable proposal ID, covering a crash after POST /approvals
 # succeeds but before its approval_id is committed locally.
 intents={}
 for row in s.d.execute("SELECT detail FROM audit WHERE action IN ('proposal_intent','proposal_attempt')"):
  try:
   d=json.loads(row[0]); b=d.get('body') or d.get('request') or {}; pid=b.get('proposal_id')
   if pid: intents[pid]=b
  except Exception: pass
 for status in ('pending','approved'):
  try: remote=c.get('/approvals',params={'status':status}).json()
  except Exception: remote=[]
  for apv in remote:
   pid=apv.get('proposal_id','')
   if not pid.startswith('ofal-'): continue
   wf=apv['workflow_id']; aid=apv['approval_id']; b=intents.get(pid,{})
   s.d.execute('INSERT OR IGNORE INTO proposals VALUES(?,?,?,?,?,?,?)',
    (pid,wf,aid,'pending',apv.get('base_version',0),json.dumps(b.get('proposed_config',{})),apv.get('created_at','')))
   pending[wf]=aid
 s.d.commit()
 while True:
  if c.get('/sim/state').json().get('finished'): break
  r=c.post('/sim/advance',json={'minutes':a.tick})
  if r.status_code==409: break
  r.raise_for_status(); st=r.json(); ts=st.get('ts',''); chunks=st.get('new_chunks',[])
  for ch in chunks:
   for ln in c.get(f"/events/chunks/{ch['chunk']}").text.splitlines():
    if not ln.strip(): continue
    e=json.loads(ln); s.add_event(e,ch['chunk'],wfs)
    if e.get('type')=='config_changed':
     s.audit(e.get('ts'),e.get('workflow_id'),'config_changed',e)
     if e.get('actor')=='supervisor':
      s.d.execute("UPDATE proposals SET status='stale' WHERE wf=? AND status='pending'",(e['workflow_id'],)); s.d.commit(); pending.pop(e['workflow_id'],None)
    elif e.get('type')=='approval_decided': s.audit(e.get('ts'),e.get('workflow_id'),'approval_decided',e)
   s.d.commit()
  if chunks: last=max(x['chunk'] for x in chunks); s.set('last_chunk',last)
  # Durable approval reconciliation: poll after every tick; approved items are applied once.
  for wf,aid in list(pending.items()):
   try: apv=c.get(f'/approvals/{aid}').json()
   except Exception: continue
   status=apv.get('status')
   if status=='approved':
    rr=c.post(f'/workflows/{wf}/apply',json={'approval_id':aid}); s.audit(ts,wf,'apply_attempt',{'approval_id':aid,'status':rr.status_code,'body':rr.json()})
    if rr.status_code in (200,409,410):
     s.d.execute('UPDATE proposals SET status=? WHERE aid=?',('applied' if rr.status_code==200 else 'stale_or_lapsed',aid)); s.d.commit(); pending.pop(wf,None)
   elif status in ('rejected','expired','lapsed'):
    s.d.execute('UPDATE proposals SET status=? WHERE aid=?',(status,aid)); s.d.commit(); s.audit(ts,wf,status,apv); pending.pop(wf,None)
  # Evaluate once per day at 10:00, inside every public approver window.
  if len(ts)>=16 and ts[11:16]=='10:00':
   for wf,w in wfs.items():
    if wf in pending: continue
    gov=w.get('governance',{}); recent=s.d.execute('SELECT COUNT(*) FROM proposals WHERE wf=? AND ts>=?',(wf,ts[:10])).fetchone()[0]
    # Conservative safety policy: one approved promotion per workflow per run.
    # Do not repeatedly mine cumulative, non-concurrent data and risk a false second winner.
    promoted=s.d.execute("SELECT COUNT(*) FROM proposals WHERE wf=? AND status='applied'",(wf,)).fetchone()[0]
    if promoted >= 1 or recent>=gov.get('max_requests_per_24h',1): continue
    cur=c.get(f'/workflows/{wf}/config').json(); cfg=copy.deepcopy(cur['config']); opts=w.get('options',{}); primary=w.get('objective',{}).get('primary','engagement_rate')
    # Conservative, one-factor voice experiment; no cohort fragmentation or cross-tenant promotion.
    dim='voice'; dist=cfg.get('allocations',{}).get('default',{}).get(dim,{})
    current=max(dist,key=dist.get) if dist else (opts.get(dim) or [''])[0]; stats=s.stats(wf,dim)
    # First create a genuine concurrent 50/50 experiment; never wait for an unobserved arm to win.
    if len(dist)<=1:
     challenger=next((v for v in opts.get(dim,[]) if str(v)!=str(current) and stats.get(str(v),{}).get('n',0)<100),None)
     if challenger is None: continue
     target={current:0.5,challenger:0.5}; chosen=None
    else:
     # Keep the highest-weight arm as the incumbent until a challenger clears the evidence bar.
     incumbent=max(dist,key=dist.get); base=stats.get(str(incumbent),{}); chosen=None
     for v in opts.get(dim,[]):
      cand=stats.get(str(v),{})
      if str(v)==str(incumbent) or not wins(base,cand,primary): continue
      # Guardrail is the opposite KPI and must not show a >2pp lower confidence bound.
      if primary=='engagement_rate': cg,cn,bg,bn=cand['p'],cand['n'],base['p'],base['n']
      else: cg,cn,bg,bn=cand['g'],cand['gn'],base['g'],base['gn']
      if cn>=100 and bn>=100 and lo(cg,cn) < lo(bg,bn)-.02: continue
      chosen=v; break
     if chosen is None: continue
     target={chosen:1.0}
    new=copy.deepcopy(cfg); new.setdefault('allocations',{}).setdefault('default',{})[dim]=target
    pid='ofal-'+wf+'-'+ts[:10].replace('-','')+'-v'+str(cur['version'])+'-'+dim+'-'+('promote' if chosen is not None else 'explore'); auto=gov.get('auto_apply',{})
    if auto.get('enabled') and dim in auto.get('allowed_dims',[]) and auto.get('max_shift',0)>=.5:
     rr=c.put(f'/workflows/{wf}/config',json={'proposal_id':pid,'base_version':cur['version'],'proposed_config':new,'rationale':'Voice winner passed conservative 95% Wilson screen; guardrail checked separately.'})
     s.audit(ts,wf,'auto_apply_attempt',{'proposal_id':pid,'http':rr.status_code,'body':rr.json()})
     if rr.status_code==200: continue
    if chosen is None:
     impact=0.0
    else:
     cst=stats.get(str(chosen),{}); bn=max(1,base.get('gn',1)); cn=max(1,cst.get('gn',1))
     delta=cst.get('g',0)/cn-base.get('g',0)/bn
     impact=round(min(1.0,max(0.0,delta*10*min(1.0,min(cn,bn)/500))),3)
    body={'proposal_id':pid,'workflow_id':wf,'base_version':cur['version'],'proposed_config':new,'change_summary':(f'Promote voice {chosen} after controlled comparison' if chosen is not None else f'Start 50/50 voice experiment: {current} vs {challenger}'),'diff':{'allocations.default.voice':{'from':dist,'to':target}},'affected_leads':0,'dry_run':{'method':'Observed arm comparison; at least 100 observations per arm; no unobserved counterfactual asserted.'},'impact_score':impact,'rationale':(f'{primary} challenger has non-overlapping 95% Wilson interval; guardrail evaluated independently.' if chosen is not None else 'Exploratory split only; no winner claim is made before minimum evidence.'),'expires_in_hours':min(12,gov.get('proposal_ttl_hours',12))}

    s.audit(ts,wf,'proposal_intent',{'body':body})
    rr=c.post('/approvals',json=body); s.audit(ts,wf,'proposal_attempt',{'body':body,'http':rr.status_code,'response':rr.json()})
    if rr.status_code==200:
     aid=rr.json()['approval_id']; pending[wf]=aid; s.d.execute('INSERT OR REPLACE INTO proposals VALUES(?,?,?,?,?,?,?)',(pid,wf,aid,'pending',cur['version'],json.dumps(new),ts)); s.d.commit()
  if st.get('finished'): break
 s.audit('END',None,'finished',c.get('/sim/state').json()); print(json.dumps({'finished':True,'events':s.d.execute('SELECT COUNT(*) FROM events').fetchone()[0],'audit':s.d.execute('SELECT COUNT(*) FROM audit').fetchone()[0],'db':a.db}))
if __name__=='__main__': main()
