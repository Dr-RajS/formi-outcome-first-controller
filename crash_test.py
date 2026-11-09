import json
import os
import signal
import socket
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCENARIO = "scenarios/public_01_dev.yaml"
PYTHON = sys.executable

def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())

def wait_health(url, proc):
    for _ in range(120):
        if proc.poll() is not None:
            raise RuntimeError("Simulator exited before becoming ready")
        try:
            if get(url + "/health").get("ok"):
                return
        except Exception:
            pass
        time.sleep(0.25)
    raise TimeoutError("Simulator did not become ready")

def start_sim(run_dir, port, log):
    url = f"http://127.0.0.1:{port}"
    proc = subprocess.Popen(
        [PYTHON, "-m", "sim", "serve", "--scenario", SCENARIO,
         "--run-dir", str(run_dir), "--port", str(port)],
        cwd=ROOT, stdout=log, stderr=subprocess.STDOUT
    )
    wait_health(url, proc)
    return proc, url

def run_controller(url, db, log):
    env = os.environ.copy()
    env["CONTROLLER_DB"] = str(db)
    return subprocess.Popen(
        [PYTHON, "controller.py", "--url", url, "--db", str(db)],
        cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT
    )

def finish_controller(proc, url, db, log, kill_after=None):
    if kill_after is not None:
        time.sleep(kill_after)
        if proc.poll() is None:
            os.kill(proc.pid, signal.SIGKILL)
            proc.wait()
            print(f"  killed controller at {kill_after}s")
    else:
        proc.wait()

    if proc.poll() is not None and proc.returncode not in (0, -signal.SIGKILL):
        raise RuntimeError(f"Controller exited unexpectedly: {proc.returncode}")

    if kill_after is not None:
        proc = run_controller(url, db, log)

    try:
        code = proc.wait(timeout=900)
    except subprocess.TimeoutExpired:
        proc.kill()
        raise TimeoutError("Controller did not finish within 15 minutes")

    if code != 0:
        raise RuntimeError(f"Controller restart failed with exit code {code}")

def run_case(root, name, crash_at=None):
    case = root / name
    case.mkdir()
    run_dir = case / "sim_run"
    db = case / "controller.sqlite3"
    port = free_port()
    with open(case / "sim.log", "w") as sim_log, open(case / "controller.log", "w") as ctl_log:
        sim, url = start_sim(run_dir, port, sim_log)
        try:
            ctl = run_controller(url, db, ctl_log)
            finish_controller(ctl, url, db, ctl_log, crash_at)
            state = get(url + "/sim/state")
            workflows = get(url + "/workflows")
            histories = {
                w["workflow_id"]: get(
                    url + "/workflows/" + w["workflow_id"] + "/config/history"
                ) for w in workflows
            }
            approvals = get(url + "/approvals")
            with sqlite3.connect(db) as conn:
                counts = {
                    "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
                    "metrics": conn.execute("SELECT COUNT(*) FROM metrics").fetchone()[0],
                }
            if not state["finished"]:
                raise RuntimeError(f"{name}: simulator did not finish")
            return {
                "finished": state["finished"],
                "sim_minute": state["sim_minute"],
                "last_event_id": state["last_event_id"],
                **counts,
                "approvals": approvals,
                "config_history": histories,
            }
        finally:
            sim.terminate()
            try:
                sim.wait(timeout=10)
            except subprocess.TimeoutExpired:
                sim.kill()
                sim.wait()

def main():
    report_dir = ROOT / "reports" / "crash_recovery"
    report_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ofal-crash-") as temp:
        temp = Path(temp)
        print("Running uninterrupted reference case...")
        reference = run_case(temp, "clean")
        results = {"clean": {
            **{k: reference[k] for k in
               ("finished", "sim_minute", "last_event_id", "events", "metrics")},
            "approval_count": len(reference["approvals"]),
            "config_history_entries": sum(map(len, reference["config_history"].values()))
        }}
        for delay in (1, 4, 7):
            print(f"Running forced-restart case at {delay}s...")
            result = run_case(temp, f"crash_{delay}s", delay)
            comparable = {
                k: result[k] for k in
                ("finished", "sim_minute", "last_event_id", "events", "metrics",
                 "approvals", "config_history")
            }
            results[f"crash_{delay}s"] = {
                **{k: comparable[k] for k in
                   ("finished", "sim_minute", "last_event_id", "events", "metrics")},
                "approval_count": len(comparable["approvals"]),
                "config_history_entries": sum(map(len, comparable["config_history"].values())),
                "approvals_match_clean": comparable["approvals"] == reference["approvals"],
                "config_history_matches_clean": comparable["config_history"] == reference["config_history"]
            }
            if comparable != {
                k: reference[k] for k in comparable
            }:
                raise AssertionError(
                    f"Recovery mismatch at {delay}s. "
                    "Inspect temporary logs before changing the controller."
                )
            print(f"  PASS: recovered state matches clean run at {delay}s")

        output = report_dir / "results.json"
        output.write_text(json.dumps(results, indent=2))
        print(f"\nALL CRASH RECOVERY CHECKS PASSED. Evidence: {output}")

if __name__ == "__main__":
    main()
