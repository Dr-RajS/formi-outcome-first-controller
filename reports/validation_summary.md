# Validation summary

- Starter simulator tests: `python -m pytest -q` — **6 passed** before controller tests were added.
- Controller regression tests: **7 passed**; starter simulator tests: **6 passed**; the current full test suite: **14 passed**.
- `python -m py_compile controller.py` — passed.
- Fresh public_01 smoke run with the updated controller — completed; controller ingested 297,068 events and exited successfully. The resulting grader report was not retained as an official scenario report because this was a smoke test, not a replacement for the recorded public_01 result.
- Recorded Public_01 and Public_02 grader outputs remain in `public_01.md` and `public_02.md`.
- Recorded Public_03 grader output remains in `public_03.md`; it is outcome evidence, not a throughput/peak-memory/10× benchmark.
- Controlled termination/restart tests at 1s, 4s and 7s completed successfully, matching the clean run's event counts, approvals and configuration history. Broader failure-mode coverage remains outstanding.
- The controller communicates with the simulator over HTTP and does not import `sim`, read `runs/`, or parse scenario YAML at runtime.

Run from the repository root:

```bash
python -m pytest -q
python -m py_compile controller.py
```

See `docs/OPERATIONS.md` for start, restart, database and audit instructions.
