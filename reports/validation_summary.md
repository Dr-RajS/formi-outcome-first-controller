# Validation summary

- Starter simulator tests: `python -m pytest -q` — **6 passed**.
- Public_01: completed end-to-end; see `public_01.md`.
- Public_02: completed end-to-end; see `public_02.md`.
- Public_03: not run; no scale metrics claimed.
- Controlled process kill/restart: not run; recovery mechanisms are implemented but C13 remains partial.
- Controller only calls documented HTTP endpoints; it does not import `sim` or read scenario YAML/hidden truth.

Reproduction commands (from repository root):

```bash
pip install -r requirements.txt
python -m pytest -q
python -m sim baseline --scenario scenarios/public_01_dev.yaml --run-dir runs/base01
python -m sim serve --scenario scenarios/public_01_dev.yaml --run-dir runs/mine01
# in another terminal:
./run.sh http://127.0.0.1:8700
python -m sim grade --run runs/mine01 --baseline runs/base01 --out reports/public_01.md
```
