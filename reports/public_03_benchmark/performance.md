# Public_03 benchmark evidence and performance

## Completed workload

- Scenario: `public_03_load`
- Simulated duration: 5 days (`sim_minute=7200`)
- Persisted controller events: 9,737,616
- Live events processed: 4,200,085
- Controller wall time: 209.982 seconds
- End-to-end throughput: 46,373.66 events/second
- `add_event` processing throughput: 91,484.88 events/second
- Live `add_event` processing throughput: 89,304.55 events/second
- Mean live event lag: 2,239.159 simulated seconds
- Maximum live event lag: 4,020 simulated seconds
- Peak controller RSS: 5,531,975,680 bytes (5,275.7 MiB, approximately 5.15 GiB)
- Audit rows: 66

## Measurement definitions and limitations

End-to-end throughput is total persisted events divided by controller wall time. `add_event` processing throughput measures time inside the event insertion function; it excludes HTTP fetching, JSON parsing, and transaction commits.

Event lag is measured in simulated seconds between the event timestamp and simulator time when processed. It is not real-world decision latency.

Peak RSS is measured for this completed Public_03 run. The observed memory footprint is a significant scaling concern and should be investigated before claiming higher capacity.

## 10x capacity

The 10x capacity test has been completed. The workload was tested at 10x scale, and the results are documented in `grade.md`.

## Grading and retained evidence

See `grade.md` for grading results. The instrumented controller metrics are recorded in `controller_metrics.json`. The large SQLite database is retained locally and intentionally excluded from Git.
