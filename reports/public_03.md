# Grade report — public_03_load

## Outcomes vs baseline (no-op controller)

| workflow | conclusion rate | Δ | pickup | Δ | engagement | Δ | engagement gap captured | hallucinated calls (base) |
|---|---|---|---|---|---|---|---|---|
| arav_cancel_2 | 0.340 | +0.8% | 0.245 | +0.7% | 0.496 | -0.0% | 0% | 396 (409) |
| arav_kyc_1 | 0.364 | +1.4% | 0.213 | -0.8% | 0.610 | +1.5% | 12% | 334 (352) |
| arav_renewal_0 | 0.403 | -0.7% | 0.264 | +0.1% | 0.544 | -0.6% | 0% | 447 (408) |
| kest_cancel_2 | 0.339 | +0.6% | 0.244 | +0.7% | 0.497 | -0.3% | 0% | 386 (418) |
| kest_kyc_1 | 0.367 | +3.3% | 0.215 | +0.4% | 0.611 | +2.3% | 12% | 368 (370) |
| kest_renewal_0 | 0.404 | +0.5% | 0.263 | -0.6% | 0.548 | +0.5% | 0% | 422 (403) |
| nort_cancel_2 | 0.339 | -0.2% | 0.244 | +0.2% | 0.496 | -0.5% | 0% | 399 (368) |
| nort_kyc_1 | 0.363 | +2.0% | 0.214 | -0.5% | 0.607 | +1.9% | 12% | 342 (318) |
| nort_renewal_0 | 0.402 | -0.9% | 0.265 | +0.1% | 0.541 | -1.3% | 0% | 432 (419) |
| tide_cancel_2 | 0.338 | -1.6% | 0.244 | +0.1% | 0.496 | -1.1% | 0% | 412 (401) |
| tide_kyc_1 | 0.365 | +2.5% | 0.214 | -0.5% | 0.612 | +2.3% | 12% | 343 (376) |
| tide_renewal_0 | 0.401 | -0.9% | 0.263 | -0.4% | 0.545 | -0.2% | 0% | 369 (425) |
| ALL | 0.369 | +0.5% | 0.241 | -0.0% | 0.547 | +0.3% | 4% | 4650 (4667) |

## Changes applied by the controller

12 applied — neutral: 8, beneficial: 4

- nort_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- tide_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- nort_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- kest_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- kest_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- tide_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.035 didΔ=+0.000 → **beneficial**
- kest_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.035 didΔ=+0.000 → **beneficial**
- tide_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.035 didΔ=+0.000 → **beneficial**
- nort_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.035 didΔ=+0.000 → **beneficial**

## Governance

```
{
  "approval_requests": 12,
  "decisions": {
    "approved": 12,
    "expired": 0
  },
  "rejection_reasons": {},
  "applied_via_approval": 12,
  "auto_applied": 0,
  "auto_apply_rejected": 0,
  "apply_conflicts": 0,
  "lapsed": 0,
  "peak_requests_per_24h": {
    "nort_renewal_0": 1,
    "nort_kyc_1": 1,
    "nort_cancel_2": 1,
    "kest_renewal_0": 1,
    "kest_kyc_1": 1,
    "kest_cancel_2": 1,
    "arav_renewal_0": 1,
    "arav_kyc_1": 1,
    "arav_cancel_2": 1,
    "tide_renewal_0": 1,
    "tide_kyc_1": 1,
    "tide_cancel_2": 1
  }
}
```

## Incidents

```
[]
```

## Decaying variants — share of in-population calls still on the variant, by day after onset

```
{}
```

Credits used: 0 · validation runs: 0 · LLM fix calls: 0