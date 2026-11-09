# Grade report — public_01_dev

## Outcomes vs baseline (no-op controller)

| workflow | conclusion rate | Δ | pickup | Δ | engagement | Δ | engagement gap captured | hallucinated calls (base) |
|---|---|---|---|---|---|---|---|---|
| ks_cancel | 0.348 | +1.8% | 0.244 | +2.0% | 0.499 | -0.3% | 0% | 57 (52) |
| nw_kyc | 0.366 | -2.8% | 0.239 | -1.4% | 0.612 | -0.0% | 15% | 23 (21) |
| nw_renewal | 0.420 | -0.1% | 0.261 | -0.3% | 0.546 | -0.3% | 0% | 50 (39) |
| ALL | 0.376 | +0.1% | 0.249 | +0.5% | 0.537 | -0.3% | 3% | 130 (112) |

## Changes applied by the controller

3 applied — neutral: 2, beneficial: 1

- nw_renewal v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- ks_cancel v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- nw_kyc v2 (controller_approved) dims=['voice'] engageΔ=+0.035 didΔ=+0.000 → **beneficial**

## Governance

```
{
  "approval_requests": 3,
  "decisions": {
    "approved": 3,
    "expired": 0
  },
  "rejection_reasons": {},
  "applied_via_approval": 3,
  "auto_applied": 0,
  "auto_apply_rejected": 0,
  "apply_conflicts": 0,
  "lapsed": 0,
  "peak_requests_per_24h": {
    "nw_renewal": 1,
    "nw_kyc": 1,
    "ks_cancel": 1
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