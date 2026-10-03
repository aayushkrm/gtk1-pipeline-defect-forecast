# GUARDRAILS — mandatory language and reporting rules (reviewer round 3)

## Naming (code, metrics, filenames, slides)
- Say `newly-reported ≥10%`, `report-forecast`. NEVER `new corrosion / initiation / growth`
  as a physical claim. "New" = unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match;
  includes true initiation + re-detected misaligned old + sensitivity gain (proven by
  60%/39% vanished-frac and cut-driven prevalence 0.27→0.08).

## Disclaimer (every results page / slide / handover)
> "New = unmatched future ≥10% row under pipe+2m/0.5m/1h match; includes re-detection.
> Absolute AP is cut- and survey-conditional." Always print alongside AP:
> match-rate, vanished-frac, cut-sensitivity column (≥10% primary, ≥12%/≥15% sensitivity).

## Thresholds
- Per-section operating thresholds (ON vs SRTO never pooled). cut≥10% primary; ≥12%/≥15% sensitivity.
- ≥80% reliability claim: not made; operating point still open (R@P0.7 retired as vacuous).

## Model quarantine
- E03 HGB-count "win" quarantined: tuned log-Ridge (MAE 6.48) beats HGB-poisson (8.52);
  HGB stays a comparator, never the headline, until residual/shuffle controls pass per experiment.
