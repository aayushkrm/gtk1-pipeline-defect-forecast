# Supervisor brief — GTK1 status (evidence as of E11, PK1 page v0, E12 running)

## One-line verdict
Inspection-report triage works and replicates 4/4 sections; physical-corrosion forecasting
at ≥80% reliability is not supportable on current data (survey-conditional reporting
predictability ≠ physical predictability — see risk below).

## Task mapping (project tasks 1–7)
1. Sources systematized: 6 sections × 2–3 surveys (2015–2025), anomaly + weld/pipe logs; formats/failures catalogued (docs/DATA.md).
2. Data QC done: 44/45-col schema, R4 headers, threshold drift quantified (PK2 164→9→55/km), 5 corrupt files, code-reuse TECH/ARTD/GOUG, 2016 Service-life fictive 100y.
3. Dependencies: past density → future reporting dominates (Spearman 0.78–0.90); pipe type/coating signals noted, age missing (only Y-N 1980).
4. Dataset: pipe-joined + 100m/1km grids, Depth≥10% normalized, matched-new labels (pipe+2m/0.5m/1h), longitudinal pairs.
5. Models: B1/persistence-family frozen primary (AP 0.64 ON / 0.28 SRTO-1608 / 0.18 SRTO-1717 / 0.78 PK1);
   log-linear best count model (MAE 6.5 vs 11.3); HGB quarantined; LR-nlag overlay ON-only experimental OFF by default.
6. Comparison: 12 experiments E01–E12 with baselines everywhere, negatives reported (HGB≈B1, shuffle anomaly, SRTO non-transfer, cut-fragility).
7. Historical validation: train-past→test-future on 4 sections + block-CV + 100-shuffle null + repair-agnostic audit.

## Numbers (section-conditional, operational framing "newly-reported ≥10% @100m")
- ON: B1 0.644/base 0.268; LR 0.676 (+0.032 ON-only). SRTO-1608 test: 0.277/0.061.
- SRTO-1717: 0.181/0.031 (13 pos). PK1: 0.779/0.401 (562 pos, stable methodology).
- Triage pages v0 (ON, PK1) ship ranked lists + heatmaps + audit columns + disclaimers.

## Residual ≥80% risk (one sentence, fourth confirmation)
The "new" label conflates true initiation with re-detected misaligned old defects and
survey-sensitivity gain (vanished 60%/39%, prevalence 0.27→0.08 across cuts), so any ≥80%
reliability framing mistakes survey-conditional reporting predictability for physical
corrosion predictability.

## Needed from partner (blockers for stronger claims)
Repair logs; 5 file re-exports; pipe ages; per-survey thresholds/methodology; SRTO-1717-2021
Character decode; 2025 weld-log tail. Work continues without them on ranking triage.
