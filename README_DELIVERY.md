# Formi Outcome-First Controller — delivery notes

This repository includes the supplied simulator assignment plus `controller.py`, `run.sh`, `SUBMISSION.md`, and public scenario grader reports.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
python -m sim baseline --scenario scenarios/public_01_dev.yaml --run-dir runs/base01
python -m sim serve --scenario scenarios/public_01_dev.yaml --run-dir runs/mine01
```

In a second terminal:

```bash
./run.sh http://127.0.0.1:8700
```

Then grade:

```bash
python -m sim grade --run runs/mine01 --baseline runs/base01 --out reports/public_01.md
```

The controller persists state in `controller_state.sqlite3` in the repository root by default. Set `CONTROLLER_DB=/path/to/state.sqlite3` to choose another path. To resume after a controller restart, use the same DB and the same running simulator.

**Read `SUBMISSION.md` before submitting.** It clearly distinguishes implemented, partial and unimplemented scope. Public_03 load testing and a controlled kill/restart evidence run are still open; do not claim those have been completed.
