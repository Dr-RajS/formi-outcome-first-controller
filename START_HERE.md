# Start here — submission checklist

## Important status

This is a working, deliberately scoped controller submission. It includes the HTTP-only controller, durable SQLite event/audit state, governed voice experiment loop, public_01 and public_02 grader reports, and the supplied simulator/tests. It is **not** a claim that all 15 optional capabilities are complete. In particular, public_03 load-scale measurement and a controlled process kill/restart evidence run are still open. Caller-ID incident remediation, prompt/hallucination incident remediation, decay rollback, shared feature cohorts, and a supervisor UI are also out of scope in this version. Read `SUBMISSION.md` before sharing it.

## 1. Download and extract

Download `Formi-Outcome-Controller-Submission.zip` from this chat and extract it. Open the extracted `sde-assignment-2026-main` folder in Terminal.

## 2. Check prerequisites

Use Python 3.10+ (tested with Python 3.13) and Git. From the project root:

```bash
python --version
git --version
```

## 3. Create an isolated environment and install dependencies

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Run the supplied tests

```bash
python -m pytest -q
```

Expected result for the supplied simulator tests: `6 passed`.

## 5. Reproduce a public scenario (recommended before upload)

Open three terminals, all in the project root, and activate `.venv` in each.

Terminal A — create a baseline:

```bash
python -m sim baseline --scenario scenarios/public_01_dev.yaml --run-dir runs/base01
```

Terminal B — start the simulator:

```bash
python -m sim serve --scenario scenarios/public_01_dev.yaml --run-dir runs/mine01 --port 8700
```

Terminal C — start the controller:

```bash
./run.sh http://127.0.0.1:8700
```

On Windows, if shell execution of `run.sh` is unavailable, use:

```powershell
python controller.py --url http://127.0.0.1:8700 --db controller_state.sqlite3
```

When the controller exits, grade the run:

```bash
python -m sim grade --run runs/mine01 --baseline runs/base01 --out reports/reproduced_public_01.md
```

The checked-in reports `reports/public_01.md` and `reports/public_02.md` are the recorded public scenario results for this version. Reproduction may take several minutes.

## 6. Review before sharing

Read these files in order:

1. `README.md` — assignment and evaluation contract.
2. `docs/SIMULATOR.md` — simulator API and governance details.
3. `SUBMISSION.md` — design, assumptions, stakeholder responses, scope cuts and limitations.
4. `reports/validation_summary.md`, `reports/public_01.md`, `reports/public_02.md` — evidence.

Do not delete `sim/`, `scenarios/`, `stakeholders/`, `tests/`, `reports/`, or `.git/`.

## 7. Create the private GitHub repository

1. Sign in to GitHub.
2. Click **New repository**.
3. Repository name: `formi-outcome-first-controller`.
4. Select **Private**.
5. Do not initialise with a README, .gitignore, or licence (the project already contains these).
6. Create the repository and copy its HTTPS URL, e.g. `https://github.com/YOUR_USERNAME/formi-outcome-first-controller.git`.

## 8. Push this existing Git repository

The extracted project contains its own `.git` history. From the project root run:

```bash
git status
git remote -v
```

If there is no `origin` remote, add it:

```bash
git remote add origin https://github.com/YOUR_USERNAME/formi-outcome-first-controller.git
```

Then push:

```bash
git push -u origin master
```

If GitHub asks you to authenticate, complete its browser/device login or use a GitHub personal access token through Git Credential Manager. Never paste a token into chat or commit it into the repository.

If `origin` already exists but points somewhere else, inspect it first. Change it only if it is your newly created assignment repository:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/formi-outcome-first-controller.git
git push -u origin master
```

## 9. Verify GitHub

Refresh the repository page. Confirm you can see `controller.py`, `run.sh`, `SUBMISSION.md`, `START_HERE.md`, `reports/`, `sim/`, `scenarios/`, `stakeholders/`, and `tests/`. Open `SUBMISSION.md` on GitHub and check formatting. Confirm the commit history is visible.

## 10. Share access and submit

Use the exact recipient email/instructions from the assignment form. Since the repository is private, add the evaluator as a collaborator only if the form or assignment explicitly tells you which GitHub username/email to invite. Do not guess the evaluator identity. Submit the repository URL in the assignment form, together with any requested details. Do not send the ZIP as a substitute if they specifically requested a Git repository.

## 11. Before an interview/review

Be ready to explain: (a) why the controller currently experiments on voice only, (b) why it uses a conservative confidence-interval screen, (c) how SQLite event IDs and chunk cursors support idempotency, (d) how approval polling and config-version checks protect governance, and (e) why public_03 performance and formal kill/restart evidence are not claimed yet. You should understand and be able to defend every design decision in `SUBMISSION.md`.
