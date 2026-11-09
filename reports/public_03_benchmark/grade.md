# Grade report — public_03_load

## Outcomes vs baseline (no-op controller)

| workflow | conclusion rate | Δ | pickup | Δ | engagement | Δ | engagement gap captured | hallucinated calls (base) |
|---|---|---|---|---|---|---|---|---|
| arav_cancel_2 | 0.340 | +0.9% | 0.245 | +0.7% | 0.498 | +0.4% | 0% | 412 (409) |
| arav_kyc_1 | 0.360 | +0.4% | 0.214 | -0.3% | 0.604 | +0.6% | 7% | 340 (352) |
| arav_renewal_0 | 0.405 | -0.1% | 0.264 | -0.1% | 0.549 | +0.2% | 0% | 387 (408) |
| kest_cancel_2 | 0.339 | +0.6% | 0.244 | +0.6% | 0.499 | +0.0% | 0% | 435 (418) |
| kest_kyc_1 | 0.359 | +1.0% | 0.215 | +0.4% | 0.598 | +0.1% | 7% | 346 (370) |
| kest_renewal_0 | 0.402 | -0.1% | 0.263 | -0.5% | 0.547 | +0.4% | 0% | 414 (403) |
| nort_cancel_2 | 0.341 | +0.6% | 0.244 | +0.1% | 0.499 | +0.1% | 0% | 390 (368) |
| nort_kyc_1 | 0.359 | +1.0% | 0.215 | -0.0% | 0.600 | +0.7% | 5% | 317 (318) |
| nort_renewal_0 | 0.404 | -0.2% | 0.264 | -0.1% | 0.547 | -0.1% | 0% | 392 (419) |
| tide_cancel_2 | 0.338 | -1.5% | 0.243 | -0.4% | 0.497 | -0.8% | 0% | 386 (401) |
| tide_kyc_1 | 0.361 | +1.2% | 0.215 | -0.1% | 0.602 | +0.6% | 7% | 339 (376) |
| tide_renewal_0 | 0.406 | +0.3% | 0.265 | +0.5% | 0.546 | +0.1% | 0% | 425 (425) |
| ALL | 0.368 | +0.3% | 0.241 | +0.1% | 0.547 | +0.2% | 2% | 4583 (4667) |

## Changes applied by the controller

12 applied — neutral: 8, beneficial: 4

- nort_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- tide_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- nort_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- kest_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_cancel_2 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- kest_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- tide_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.021 didΔ=+0.000 → **beneficial**
- kest_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.021 didΔ=+0.000 → **beneficial**
- tide_renewal_0 v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- arav_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.021 didΔ=+0.000 → **beneficial**
- nort_kyc_1 v2 (controller_approved) dims=['voice'] engageΔ=+0.021 didΔ=+0.000 → **beneficial**

## Governance

```
{
  "approval_requests": 13,
  "decisions": {
    "approved": 12,
    "expired": 1
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