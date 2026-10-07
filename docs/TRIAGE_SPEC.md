# TRIAGE-SPEC — honest December deliverable (reviewer rounds 4c–10; evidence as of E13 + prospective harness)

## What ships
Ship a calibrated **inspection-report triage tool**. Do not ship a reliability guarantee.
Rank 100m segments by P(newly-reported ≥10% defect). Add linear heatmap with uncertainty bands.
Add audit columns (B1 score, model score, match/vanished flags). Show no red/green pass-fail badges.
Show no ≥80% meter. Apply per-section recalibration control. Show GUARDRAILS disclaimer on every page.

## Expected numbers (honest, section-conditional)
- Report ON @100m cut≥10% as B1 0.644. Report LR 0.676. Report Δ-vs-B1 +0.032 [+0.011,+0.053] **ON-only experimental**. Note driver nlag −0.039 vs full. Note cut≥12 replicates +0.040. Note cut≥15 fails −0.024.
  Report SRTO as B1 0.277, LR 0.281, Δ +0.004 [−0.032,+0.039] — **overlay adds zero off-site; ship B1 only there.**
  Keep headline at AP ~0.65±0.05 ON (~2.4× base), ~0.28 SRTO at 6% prevalence.
- Report SRTO absolute AP as substantially lower (~0.28 at 6% prevalence). Confirm rank-order replicates.
  Report SRTO-1717 as 0.181/0.031 (13 pos, liftCI lower>0; 2021 covers ~30/42km).
- Report PK1 as B1 0.779/0.574/0.375 at ≥10/12/15% (562 pos, all lift-CIs lower>0; stable 8982-vs-8989 methodology; match cut-invariant 0.715/0.715/0.690). Use two-section triage demo set (ON + PK1).
- Report count as MAE ~6.5 via log-linear vs 11.3 mean baseline (HGB quarantined).

## Task definition (operational, never physical)
Define "Newly-reported ≥10% @100m" as unmatched future ≥10% row under pipe+2m/0.5m/1h greedy match.
Include initiation + re-detected misaligned old + sensitivity gain. Support this scope with 60%/39% vanished-frac and cut-driven prevalence 0.27→0.08.
Ship every number with match-rate, vanished-frac, and cut-sensitivity triple (≥10% primary; ≥12%/≥15% sensitivity).

## Partner data requests (blockers for stronger claims)
1. Provide repair logs per section/year. Use them as exclusion for vanished-deep rows. Note currently 2.8% suspect tail train.
2. Provide re-export of 5 damaged files from source (CRC-truncated .xls/.xlsx).
3. Provide pipe commission years / ages (only Y-N has 1980).
4. Provide per-survey registration thresholds + contractor/methodology notes. Use them for contractor-effect modeling.
5. Decode empty Character (SRTO-1717-2021, 37%) and 2025 weld-log tail (27km truncation).
