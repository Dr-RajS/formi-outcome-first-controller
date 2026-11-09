import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from controller import (
    Store, affected_leads, auto_apply_allowed, evaluation_due,
    fresh_run_required, lo, proposal_id, wins,
)


def test_wilson_interval_known_bounds():
    assert round(lo(50, 100), 3) == 0.404
    assert round(lo(90, 100), 3) == 0.826


def test_fresh_vs_resume_detection():
    assert fresh_run_required("public_01", 100, "public_02", 0)
    assert fresh_run_required("public_01", 100, "public_01", 0)
    assert not fresh_run_required("public_01", 100, "public_01", 100)


def test_event_dedupe_is_idempotent(tmp_path):
    store = Store(str(tmp_path / "state.sqlite3"))
    event = {"event_id": 7, "type": "call", "workflow_id": "wf",
             "cohort_id": "default", "variant": {"voice": "V1"},
             "connected": True, "engaged": True}
    assert store.add_event(event, 1, {"wf": {"objective": {"primary": "engagement_rate"}}})
    assert not store.add_event(event, 1, {"wf": {"objective": {"primary": "engagement_rate"}}})
    assert store.d.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 1
    assert store.stats("wf", "voice")["V1"]["n"] == 1


def test_proposal_id_is_deterministic():
    expected = "ofal-wf-20261110-v3-voice-explore"
    assert proposal_id("wf", "2026-11-10", 3, "voice", "explore") == expected
    assert proposal_id("wf", "2026-11-10", 3, "voice", "explore") == expected


def test_auto_apply_respects_allowed_dims_and_shift():
    gov = {"auto_apply": {"enabled": True, "allowed_dims": ["caller_id"], "max_shift": 0.2}}
    assert auto_apply_allowed(gov, ["caller_id"], 0.1)
    assert not auto_apply_allowed(gov, ["voice"], 0.1)
    assert not auto_apply_allowed(gov, ["caller_id"], 0.3)


def test_evaluation_never_before_eleven_and_once_per_day():
    assert not evaluation_due("2026-11-10T10:45:00+05:30", None)
    assert evaluation_due("2026-11-10T11:00:00+05:30", None)
    assert not evaluation_due("2026-11-10T12:00:00+05:30", "2026-11-10")


def test_affected_leads_estimate():
    assert affected_leads(1000, "explore") == 300
    assert affected_leads(1000, "promote") == 1000


def test_winner_requires_minimum_sample_per_arm():
    assert not wins({'n': 249, 'p': 200, 'gn': 200, 'g': 150},
                    {'n': 500, 'p': 450, 'gn': 450, 'g': 400}, 'pickup_rate')
    assert wins({'n': 500, 'p': 200, 'gn': 200, 'g': 150},
                {'n': 500, 'p': 450, 'gn': 450, 'g': 400}, 'pickup_rate')
