# Public_03 benchmark evidence and limitations

## Completed workload

- Scenario: `public_03_load`
- Simulated duration: 5 days (`sim_minute=7200`)
- Persisted controller event count: 9,737,616
- Durable chunk cursor: 88
- Grader outcome: overall conclusion rate 0.368, +0.3% versus baseline
- Pickup: 0.241, +0.1%; engagement: 0.547, +0.2%
- Changes: 12 applied (4 beneficial, 8 neutral)
- Governance: 13 approval requests; 12 approved and applied, 1 expired; 0 apply conflicts; 0 incidents

## Performance measurement limitations

The available `time.txt` record measures the grading command, not a verified end-to-end controller execution. It must not be used as controller runtime or peak-memory evidence.

End-to-end ingest throughput, decision lag, controller peak RSS under the target workload, and 10x capacity were not measured with a valid benchmark. These requirements remain open. No 10x capacity claim is made.

The 4.8 GB SQLite database is retained locally as evidence and is intentionally excluded from Git.
