# Grade report — public_02_incidents

## Outcomes vs baseline (no-op controller)

| workflow | conclusion rate | Δ | pickup | Δ | engagement | Δ | engagement gap captured | hallucinated calls (base) |
|---|---|---|---|---|---|---|---|---|
| ks_cancel | 0.244 | +0.0% | 0.184 | +0.8% | 0.467 | -1.0% | 0% | 325 (310) |
| nw_kyc | 0.382 | -0.5% | 0.242 | -2.4% | 0.609 | +1.6% | 22% | 30 (38) |
| nw_renewal | 0.434 | +1.0% | 0.260 | -1.2% | 0.562 | +2.5% | 8% | 59 (58) |
| ALL | 0.337 | +0.3% | 0.221 | -0.7% | 0.535 | +1.0% | 6% | 414 (406) |

## Changes applied by the controller

3 applied — neutral: 1, beneficial: 2

- ks_cancel v2 (controller_approved) dims=['voice'] engageΔ=+0.000 didΔ=+0.000 → **neutral**
- nw_renewal v2 (controller_approved) dims=['voice'] engageΔ=+0.014 didΔ=+0.000 → **beneficial**
- nw_kyc v2 (controller_approved) dims=['voice'] engageΔ=+0.021 didΔ=+0.000 → **beneficial**

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
[
  {
    "type": "did_flagged",
    "workflow": "ks_cancel",
    "at": "D2 10:00",
    "flagged_did_share_by_day": {
      "2": 0.505,
      "3": 0.493,
      "4": 0.504,
      "5": 0.503,
      "6": 0.504,
      "7": 0.497,
      "8": 0.491,
      "9": 0.504
    }
  },
  {
    "type": "supervisor_edit",
    "workflow": "ks_cancel",
    "at": "D3 11:30",
    "mttr_minutes": null,
    "fixed_by": null
  },
  {
    "type": "supervisor_edit",
    "workflow": "nw_renewal",
    "at": "D5 15:00"
  }
]
```

## Decaying variants — share of in-population calls still on the variant, by day after onset

```
{}
```

Credits used: 0 · validation runs: 0 · LLM fix calls: 0