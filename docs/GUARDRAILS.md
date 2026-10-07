# GUARDRAILS: mandatory language and reporting rules (reviewer round 3)

## Naming (code, metrics, filenames, slides)
- Say `newly-reported ≥10%` and `report-forecast`. NEVER say `new corrosion / initiation / growth` as a physical claim. Define "New" as unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match. Include true initiation + re-detected misaligned old + sensitivity gain. Prove this scope by 60%/39% vanished-frac and cut-driven prevalence 0.27→0.08.

## Disclaimer (every results page / slide / handover)
> "New = unmatched future ≥10% row under pipe+2m/0.5m/1h match; includes re-detection.
> Absolute AP is cut- and survey-conditional." Always print alongside AP:
> match-rate, vanished-frac, cut-sensitivity column (≥10% primary, ≥12%/≥15% sensitivity).

## Thresholds
- Set operating thresholds per section (ON vs SRTO never pooled). Use cut≥10% primary with ≥12%/≥15% sensitivity.
- Exclude the boundary cell from prospective ranking by default (E13: overrun rows accumulate there). Leave retrospective frozen pages unchanged.

## Replication tally rules (R1–R4; reviewer round 12 — a pair counts iff ALL hold)
- R1 frozen pipeline/matcher/cut. R2 source-grade inputs (no repaired/salvage copy).
- R3 stationarity screen: future/past d≥10 ratio in [0.5,2.0] AND match ≥0.20 or ≥50% of same-section prior.
- R4 lift-CI lower>0 with n_pos≥30. R2∧R3 are instrument-validity gates; R4 is the statistical gate.
- Failing R2/R3 with passing R4 = instrument changed ("newly-reported" changed meaning) → void as
  replication evidence, kept as break evidence only. Current tally: 3 clean (ON, SRTO-1608,
  PK1) + E10 weak/insufficient (SRTO-1717, suggestive only) + E14 void (repaired copy, ratio 4.78, match 0.134). No consumer may read
  results_e14* (handover pages assert only ON/PK1/SRTO-1608 frozen numbers).
- ≥80% reliability claim: not made; operating point still open (R@P0.7 retired as vacuous).

## Model quarantine
- Quarantine E03 HGB-count "win". Tuned log-Ridge (MAE 6.48) beats HGB-poisson (8.52). Keep HGB as a comparator, never the headline. Promote it only after residual/shuffle controls pass per experiment.
