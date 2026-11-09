# Formi Outcome-First Controller — delivery notes

The repository contains the HTTP-only controller, simulator, stakeholder memos, tests, reports and submission.

## Quick validation

```bash
pip install -r requirements.txt
python -m pytest -q
python -m py_compile controller.py
```

Expected test result: **14 passed**.

For start, restart, database handling and audit queries, see `docs/OPERATIONS.md`. For design choices, stakeholder responses and limitations, see `SUBMISSION.md`.

**Evidence boundary:** prior public scenario grader reports are retained. This delivery includes a fresh public_01 smoke run and controlled termination/restart tests at 1s, 4s and 7s, with results matching the clean run. Formal Public_03 throughput, decision-lag, controller memory and 10× capacity benchmarks remain outstanding.
