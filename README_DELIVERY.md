# Formi Outcome-First Controller — delivery notes

The repository contains the HTTP-only controller, simulator, stakeholder memos, tests, reports and submission.

## Quick validation

```bash
pip install -r requirements.txt
python -m pytest -q
python -m py_compile controller.py
```

Expected test result: **13 passed**.

For start, restart, database handling and audit queries, see `docs/OPERATIONS.md`. For design choices, stakeholder responses and limitations, see `SUBMISSION.md`.

**Evidence boundary:** prior public scenario grader reports are retained. This delivery includes a fresh public_01 smoke run, but does not claim a formal SIGKILL/restart acceptance test or formal Public_03 throughput, decision-lag, memory and 10× benchmark.
