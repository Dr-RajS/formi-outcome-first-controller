# Outcome-First Agent Loop — Submission

**Name:** Raj Shah  
**Date:** 9 November 2026  
**Hours actually spent:** Not tracked reliably; do not infer from this delivery.  
**Language / storage:** Python 3.13, HTTPX, SQLite (WAL + FULL synchronous commits).

## 0. TL;DR

This is an HTTP-only, persistent controller that bootstraps from event history, deduplicates events by `event_id`, tracks voice-arm outcomes, uses conservative Wilson-interval comparisons, submits governed proposals, and reconciles approvals after restart. Public_01 and public_02 both completed end-to-end. Public_02 finished +0.3% overall conclusion rate versus baseline, with two beneficial and one neutral applied changes. Public_01 finished +0.1% overall conclusion rate, with one beneficial and two neutral applied changes. This is a working, deliberately narrow submission—not a claim that all 15 capabilities are complete: load-scale measurement, a demonstrated kill/restart run, caller-ID incident remediation, prompt incident remediation, decay rollback and supervisor UI remain incomplete.

## 1. Assumptions

1. The HTTP API is the only source of operational truth; controller code does not import `sim` or inspect scenario truth.
2. `event_id` is globally unique and monotonically increasing as documented.
3. A call's `connected` and `engaged` booleans are the observed pickup and engagement outcomes; engagement is evaluated conditional on connection.
4. Public scenarios expose a single default cohort in the call events used here. The current controller therefore does not claim to have built a general feature-based cohort system.
5. A safe initial policy is preferable to frequent changes: at most one successful promotion per workflow per run, and proposals are made during approver hours.
6. Voice is the only variant dimension currently experimented on. Other dimensions are deliberately not changed by this controller.

## 2. Scope decisions

| # | Capability | Built / Partial / Cut | Why | What it would take to finish |
|---|---|---|---|---|
| C1 | Event ingestion at load scale | Partial | NDJSON chunks, SQLite persistence, event-ID dedupe and chunk cursor; public_03 throughput not measured | Benchmark on public_03 and tune batched writes/partitioning |
| C2 | Shared cohort object | Cut | Current public run uses the default cohort only; no false claim of shared segmentation | Join lead features and define a versioned cohort object used by every subsystem |
| C3 | Historical bootstrapping | Built | Reads history chunks before advancing the simulator | Add schema-versioned feature snapshots |
| C4 | Call-time optimisation | Cut | Scheduling/cadence is business-owned and explicitly out of scope | None for this assignment's chosen scope |
| C5 | Caller-ID health | Cut | Public_02 contains a DID flag; no automated rotation was shipped | Population-level DID health monitor, policy-aware rotation and post-change verification |
| C6 | Welcome/voice experiments | Partial | Voice-only comparison; no factorial welcome × voice experiment | Concurrent multi-arm experiment registry, interaction-aware analysis and multiplicity correction |
| C7 | Winner promotion, decay and rollback | Partial | Conservative one-promotion cap avoids repeated mining of cumulative data; no decay rollback | Sequential monitoring, holdout windows and automatic governed rollback proposals |
| C8 | Hallucination incident response | Cut | No LLM/validation credits spent; no prompt change | Detector calibration, LLM suggestion, validation evidence and post-apply verification |
| C9 | Governance client | Partial | Approval request, approver-hour timing, TTL/status polling, stale/lapsed handling, audit and remote reconciliation | Full batching, policy-aware retry queue and richer stale re-proposal strategy |
| C10 | Impact, affected leads, dry run | Partial | Includes explicit dry-run method and a conservative observed-effect score; affected-lead estimate is zero rather than invented | Historical cohort replay and a validated future-lead forecast |
| C11 | Supervisor view | Cut | Audit DB is queryable but no UI/API dashboard was built | Read-only dashboard over audit and experiment tables |
| C12 | Decision/audit store | Built | SQLite audit trail records bootstrap, proposals, decisions, config changes, apply attempts and finish | Add query CLI and retention/backup policy |
| C13 | Crash recovery | Partial | Durable event cursor, idempotent events, SQLite WAL and pending-approval reconciliation implemented; a formal kill/restart evidence run is not included | Execute and attach a controlled kill/restart test against the final controller |
| C14 | Observability | Partial | Durable counts/audit available in SQLite; no metrics endpoint or alerting | Export lag, throughput, credits and decision counters to metrics/alerts |
| C15 | Fair credit/approver allocation | Cut | No credit-consuming endpoint is called; only one proposal per workflow per day is allowed by policy | Tenant-level fair scheduler and credit budgets |

The scope prioritises a narrow governed learning loop and durable evidence over a superficial implementation of every requested feature. The controller does not change call cadence, schedules, prompts or caller IDs.

## 3. Stakeholders

### 01 — Sales
- **Accepted:** measurable workflow-level outcomes and low approver fatigue.
- **Declined:** a blended KPI, instant rollout, and assuming auto-apply is universally enabled. Pickup, engagement and conclusion remain separate. Auto-apply is dimension- and shift-limited by policy.
- **Incorrect claim:** Kestrel's auto-apply is not unrestricted; its allowed dimensions and max shift are constrained. Northwind KYC has auto-apply disabled in the supplied policy. Prompt changes require validation evidence.
- **Reply:** “We will report conclusion, pickup and engagement separately. We will only promote a winner after population-level evidence and the workflow's governance policy permits it. Auto-apply is not a blanket permission, and prompt changes require validation evidence. We are deliberately limiting proposal frequency so supervisors receive decisions they can review rather than a stream of speculative changes.”

### 02 — Client Compliance
- **Accepted:** human approval for customer-facing changes, validation for scripts, and variant-level auditability.
- **Pushback:** do not infer that every operational setting needs the same approval route; the signed workflow policy defines the allowed auto-apply boundary. This implementation avoids auto-applying customer-facing voice changes regardless.
- **Reply:** “Every voice change in this release is routed through approval. Prompt changes are not automated. We persist call-level variant and config-version events alongside the decision audit. The current implementation is intentionally conservative; a production compliance export and retention SLA would be a separate release gate.”

### 03 — Platform/SRE
- **Accepted:** idempotent ingestion, durable SQLite state, WAL, restart cursor and no new server dependency.
- **Partial:** crash-recovery design is present, but a formal kill/restart evidence run and public_03 performance numbers are not attached. SQLite is suitable for this single-process simulator submission, not a multi-replica production deployment.
- **Reply:** “The controller persists event IDs, chunk progress, proposals and audit rows in SQLite WAL mode. Restart replays are deduplicated. I have not represented this as production-scale proof: the public_03 benchmark and controlled kill/restart evidence remain release gates.”

### 04 — Client Ops Supervisor
- **Accepted:** do not overwrite supervisor edits; send proposals during approver hours; limit proposal volume; keep changes explainable.
- **Pushback:** the memo's requested two-per-day maximum is a stakeholder preference, not a universal platform policy. The controller uses the stricter one-successful-promotion-per-workflow-per-run rule.
- **Reply:** “Supervisor edits are ingested and invalidate pending proposals for that workflow. We do not silently restore the prior config. Proposals are sent during the configured approval window, and this release caps successful promotions at one per workflow to avoid noisy experimentation. A consolidated supervisor screen is not yet included.”

### 05 — Product
- **Accepted:** pickup and engagement are separate; evidence must come from observed calls; proposals carry a diff, rationale, impact score and dry-run description; promotion is workflow-local.
- **Partial:** a general shared cohort object, historical cohort replay, robust multiplicity control, and a fully calibrated impact model are not implemented. The reported affected-lead estimate is deliberately zero rather than fabricated.
- **Reply:** “The controller only uses observed call outcomes and keeps pickup separate from engagement. It currently experiments on voice only in the default cohort; it does not claim to solve per-person timing, caller-ID health or a supervisor dashboard. Those are explicitly scoped follow-on capabilities.”

### 06 — CTO
- **Accepted:** compute/credits should be spent only when they change a decision; explainability and scope discipline matter more than feature count.
- **Pushback:** none of the stakeholder wishlists is treated as an automatic P0. This release spends no LLM or validation credits.
- **Reply:** “I chose a narrow, auditable voice experiment and governed promotion path. The public_02 result is positive but modest; public_01 is near-flat, so this should be treated as an engineering prototype, not a production-ready optimiser. The next gates are load testing, controlled crash recovery, DID/prompt incident response and rollback.”

## 4. Architecture

```text
HTTP simulator
   |  history + event NDJSON chunks
   v
Event reader -> SQLite event_id dedupe -> metric aggregates
   |                                  |
   |                                  v
   |                         Wilson interval comparison
   |                                  |
   v                                  v
chunk cursor                    proposal intent + audit
                                      |
                                      v
                                POST /approvals
                                      |
                           poll approval status by ID
                                      |
                          approved -> apply exactly once
                                      |
                                      v
                              config_changed events
                                      |
                                      v
                            SQLite audit + proposal state
```

SQLite uses WAL and `synchronous=FULL`. Event insertion and metric updates are committed per chunk; the durable chunk cursor is advanced only after the chunk has been ingested. Duplicate event IDs are ignored. Proposal intents are written before the approval POST, and remote pending/approved approvals with the controller's proposal prefix are reconciled on restart.

## 5. The learning loop

- **Cohorts:** only the simulator's `default` cohort is used. There is no claim of feature-based segmentation.
- **Experiment design:** one factor at a time (voice); no welcome × voice factorial design. Where the current distribution is a single arm, the controller requests a 50/50 split; otherwise it evaluates observed arms. It does not use hidden simulator truth.
- **Winner selection:** 95% Wilson interval non-overlap with at least 100 observations per arm; the opposite KPI is screened as a guardrail with a 2 percentage-point lower-bound tolerance. This is conservative relative to a raw point-estimate comparison but does not fully correct for multiple comparisons or temporal drift.
- **Promotion limit:** at most one approved promotion per workflow per run. This was added to avoid repeated mining of cumulative historical arm data; it trades learning speed for reduced repeated false-winner risk.
- **Decay/rollback:** not implemented. No claim of rollback capability is made.
- **Call time / caller ID:** not changed. Caller-ID incident response remains a known gap.
- **Guardrail:** pickup and engagement are calculated separately; the non-primary metric is screened before a voice promotion is proposed.

## 6. Governance

The controller proposes only through `/approvals` for voice changes. It observes approver windows, respects the workflow request-rate cap, persists proposal intent and approval IDs, polls approval status, applies approved proposals, and marks rejected/expired/lapsed/stale outcomes. A supervisor `config_changed` event invalidates the workflow's pending proposal. It does not use auto-apply in this release, even when policy permits it. Proposal impact is based on the observed effect estimate and sample support; the exploratory split has impact score 0. Affected leads are set to zero because no reliable future-lead forecast is available. The dry-run field describes the actual observed-arm comparison and explicitly avoids claiming an unobserved counterfactual replay.

## 7. Incidents

Public_02 includes a flagged caller ID and supervisor edits. The controller records the incident-related configuration events and respects supervisor edits, but it does **not** rotate the flagged caller ID or repair prompt hallucinations. No LLM/validation credits are spent. Caller-ID detection/remediation and prompt incident response are incomplete. The public_02 grade report is the evidence for outcomes and incident timeline.

## 8. Scale

Public_03 was not run in this delivery. Therefore no ingest-throughput, decision-lag, peak-memory or simulated-day wall-clock claim is made. SQLite's per-event work and the Python process are the likely first bottlenecks at 10×. The next benchmark should batch inserts, index by workflow/cohort/time, partition ingestion by workflow, and measure under the stated 4-vCPU/8-GB envelope.

## 9. Reliability

The code uses SQLite WAL, FULL synchronous commits, event-ID uniqueness, a persisted chunk cursor, persisted proposal intent, and remote approval reconciliation. Public_01 and public_02 completed end-to-end. A controlled process kill/restart run has not yet been captured as evidence, so C13 is marked partial rather than claimed complete. HTTP 4xx responses are logged for proposal/apply operations; transport failures stop the process and are recoverable by rerunning against the same DB and simulator state.

## 10. Audit & observability

Example query:

```sql
SELECT ts, wf, action, detail
FROM audit
WHERE wf = 'nw_renewal'
ORDER BY id;
```

This returns the bootstrap, proposal intent/request, approval decision, apply attempt and config-change records. The database also has event and proposal tables. A metrics endpoint and paging rules are not implemented. Production alerts should page on sustained event-ingest lag, failed apply after approval, repeated stale-base conflicts, expired approvals that block an incident, and DB write failures—not on individual call outcomes.

## 11. Results

See `reports/public_01.md` and `reports/public_02.md` for complete grader output.

- **Public_01:** overall conclusion rate +0.1% versus baseline; pickup +0.5%; engagement -0.3%. Three changes applied: one beneficial, two neutral. Three approval requests were made and approved.
- **Public_02:** overall conclusion rate +0.3%; pickup -0.7%; engagement +1.0%. Three changes applied: two beneficial, one neutral. Three approval requests were approved; no harmful applied change was reported by the grader.

The results are mixed. Public_02 is modestly positive; public_01 is near-flat. This is not sufficient evidence to claim a robust optimiser or ship to production. The first improvement should be stronger experiment design (pre-registered arms, concurrent holdouts, multiplicity control and cohort-aware windows), then rerun both scenarios.

## 12. Trade-offs & rejected alternatives

| Option | Why considered | Why rejected / what instead |
|---|---|---|
| LLM prompt changes | Could address hallucination incidents | Requires credits and validation evidence; not implemented in this narrow release |
| Auto-apply | Faster rollout | Avoided customer-facing changes and policy ambiguity; use approval path |
| Factorial welcome × voice | Could learn interactions | Needs more traffic and multiplicity-aware analysis; voice-only first |
| Caller-ID rotation | Public_02 contains DID flag | Requires a dedicated health model and policy-aware rotation; not improvised |
| Postgres/Redis | Production multi-worker scale | SQLite avoids new infrastructure for the single-process assignment; production migration would be required |

## 13. Known weaknesses

1. Public_01 result is near-flat; public_02 is only modestly positive.
2. Minimum sample size of 100 is a starting threshold, not a power analysis.
3. No multiple-comparison correction, cohort feature join, or temporal holdout.
4. No caller-ID rotation, prompt validation, hallucination remediation, decay rollback, supervisor UI, or load benchmark.
5. No formal kill/restart evidence is attached.
6. Impact score and affected-lead estimate are intentionally conservative but not yet a fully calibrated business model.

## 14. If this went to production at Formi next month

1. Freeze automated promotions; run in shadow mode until experiment power and guardrails are validated.
2. Add feature joins and one versioned cohort object shared by detection, experiment and supervisor views.
3. Implement DID health detection and a prompt safety incident path with validation evidence.
4. Add concurrent holdouts, multiplicity correction, sequential monitoring, decay detection and governed rollback.
5. Run public_03 and 10× stress tests; move state to managed Postgres and add metrics/alerts.
6. Execute controlled crash/restart and supervisor-edit chaos tests; add compliance export and retention controls.
7. Only then enable policy-permitted automation with staged rollout and per-tenant kill switches.
