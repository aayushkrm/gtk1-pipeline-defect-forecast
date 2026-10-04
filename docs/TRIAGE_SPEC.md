# TRIAGE-SPEC — honest December deliverable (reviewer rounds 4c–10; evidence as of E13 + prospective harness)

## What ships
Calibrated **inspection-report triage tool**, not a reliability guarantee:
ranked 100m segments by P(newly-reported ≥10% defect) + linear heatmap with uncertainty bands
and audit columns (B1 score, model score, match/vanished flags). No red/green pass-fail badges.
No ≥80% meter. Per-section recalibration control. GUARDRAILS disclaimer on every page.

## Expected numbers (honest, section-conditional)
- ON @100m cut≥10%: B1 0.644; LR 0.676, Δ-vs-B1 +0.032 [+0.011,+0.053] **ON-only experimental**
  (driver nlag −0.039 vs full; cut≥12 replicates +0.040, cut≥15 fails −0.024).
  SRTO: B1 0.277, LR 0.281, Δ +0.004 [−0.032,+0.039] — **overlay adds zero off-site; ship B1 only there.**
  Headline stays AP ~0.65±0.05 ON (~2.4× base), ~0.28 SRTO at 6% prevalence.
- SRTO: substantially lower absolute AP (~0.28 at 6% prevalence); rank-order replicates.
  SRTO-1717: 0.181/0.031 (13 pos, liftCI lower>0; 2021 covers ~30/42km).
- PK1: B1 0.779/0.574/0.375 at ≥10/12/15% (562 pos, all lift-CIs lower>0; stable 8982-vs-8989
  methodology; match cut-invariant 0.715/0.715/0.690). Two-section triage demo set (ON + PK1).
- Count: MAE ~6.5 via log-linear vs 11.3 mean baseline (HGB quarantined).

## Task definition (operational, never physical)
"Newly-reported ≥10% @100m": unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match.
Includes initiation + re-detected misaligned old + sensitivity gain (60%/39% vanished-frac,
cut-driven prevalence 0.27→0.08). Every number ships with match-rate, vanished-frac,
cut-sensitivity triple (≥10% primary; ≥12%/≥15% sensitivity).

## Partner data requests (blockers for stronger claims)
1. Repair logs per section/year (exclusion for vanished-deep rows; currently 2.8% suspect tail train).
2. Re-export of 5 damaged files from source (CRC-truncated .xls/.xlsx).
3. Pipe commission years / ages (only Y-N has 1980).
4. Per-survey registration thresholds + contractor/methodology notes (contractor-effect modeling).
5. Decode of empty Character (SRTO-1717-2021, 37%) and 2025 weld-log tail (27km truncation).
