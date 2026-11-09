# Operations guide

## Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m sim serve --scenario scenarios/public_01_dev.yaml --run-dir runs/mine01 --port 8700
```

In another terminal:

```bash
./run.sh http://127.0.0.1:8700
```

On Windows PowerShell, run the controller directly:

```powershell
python controller.py --url http://127.0.0.1:8700 --db controller_state.sqlite3
```

## Restart and database handling

- To resume the same simulator run, restart the controller with the same `--db` path while the simulator is still running.
- The controller persists event IDs, chunk cursor, proposal intents, approval IDs and audit records in SQLite.
- It queries the event chunk index after its durable cursor on each tick. Replayed event IDs are ignored.
- On a different scenario name or a simulator clock reset, the controller archives the previous database and its SQLite `-wal`/`-shm` sidecars before bootstrapping the new run.
- Do not manually delete a database while its controller is running.

## Evidence and diagnosis

Run `python -m pytest -q`. Query the audit trail with:

```sql
SELECT ts, wf, action, detail FROM audit ORDER BY id;
```

Inspect proposal state with:

```sql
SELECT pid, wf, aid, status, base, ts FROM proposals ORDER BY ts;
```

## Known limitations / escalation

This version does not automatically remediate caller-ID or prompt incidents, perform decay rollback, or expose a supervisor dashboard. It does not yet publish ingest-lag or memory metrics. For an approved change that is not applied, inspect `apply_attempt` and the corresponding approval status before retrying. Do not manually replay an approval POST with a new proposal ID.

For a production deployment, page the on-call engineer for sustained ingestion lag, repeated apply conflicts after approval, database write failures, or an incident approval that is blocked beyond its operational window. Individual call outcomes should not page.
