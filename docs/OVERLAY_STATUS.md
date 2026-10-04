# OVERLAY_STATUS — LR-nlag experimental branch (archived, OFF by default, kill-switch engaged)

## What it is
7-feature LogisticRegression (driver: neighbor-lag, ablation-vs-full −0.039) over B1.
ON-only experimental overlay. Frozen; no further tuning permitted without reviewer re-approval.

## Evidence (why OFF)
- ON: Δ-vs-B1 +0.032 [+0.011,+0.053] (≥10%), +0.040 (≥12%), −0.024 (≥15%, sparse fail).
- SRTO holdout: LR 0.281 vs B1 0.277, dCI [−0.032,+0.039] — zero transfer.
- E09 block-CV: +0.032/+0.011/+0.005, 2/3 CIs cross 0 — dense-ground only.
- Null-calibration saga closed (E07b): pipeline sane; effect is small/local, not general.

## Promotion rule (all required)
"Dead unless prospective dense-ground confirms": needs (a) next-survey prospective Δ-vs-B1 lower>0
on dense ground, (b) 100-shuffle null re-pass, (c) reviewer round approving default-on.
Until then: ship B1-only paths. Provenance: experiments/e07_*.py + results_e07*.json (frozen).
