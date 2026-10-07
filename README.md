# GTK1: inspection-report triage for main gas pipelines

[Читать на русском](README_RU.md)

Private R&D repo. Status: scope frozen, awaiting partner data. Raw VTD data is never committed.

## What this is

Past inspection (VTD/ILI) anomaly tables feed a ranking of 100 m pipeline cells by
P(newly-reported defect at depth ≥ 10%). Engineers use the ranking to plan digs and surveys.
The tool predicts reporting, not physical corrosion. No ≥ 80% reliability claim is supportable
on current data. That position is documented with evidence, not hedged.

## Work done so far

Parsed 6 sections × 2 to 3 surveys (2015–2025): anomaly tables plus weld and pipe logs.
Mapped the 44/45-column schema, quantified threshold drift (PK2 counts ran 164 → 9 → 55 per km),
and salvaged 5 corrupt files. Built matched-new labels (same pipe, ±2 m, ±0.5 m offset, ±1 h
orientation) on 100 m grids with Depth ≥ 10% normalization.

Ran experiments E01–E14 with baselines everywhere. Ranking B1 (past-count persistence) beats base
rate on 4 of 6 studied sections, each with lift-CI lower bound above zero. The other two cannot
form a valid pair: PK2 mixes a 23-column 2015 schema with 44-column later surveys at 6% vs 96%
≥10% share (different instruments, not growth); Yu-N has zero readable anomaly surveys (both corrupt,
re-export requested). Details: docs/DATA.md and the scoping entries in PROGRESS.md.

| Section | Pair | B1 AP / base |
|---|---|---|
| Omsk–Novosibirsk 392–526 | 2016→2021 / 2021→2025 | 0.644 / 0.268 (cut triple 0.546 / 0.364 at ≥12 / ≥15%) |
| Parabel–Kuzbass-1 572–714 | 2022→2025 | 0.779 / 0.574 / 0.375 (562 positives, stable method) |
| SRTO–Omsk 1608–1717 | 2016→2021 / 2021→2024 | 0.530 / 0.277 (test, 63 positives) |
| SRTO–Omsk 1717–1759 | 2016→2021 | 0.181 / 0.031 (13 positives) |
| Parabel–Kuzbass-2 0–110 | no valid pair (deferred) | 2015 schema has 23 columns vs 44 later; ≥10% in 5.8% of 18,337 rows (2015) vs 96% of measured depths (2020) |
| Yurga–Novosibirsk 0–154 | no valid pair (salvage pending validation) | anomaly sheets fail strict parsers (truncated streams); salvaged so far: 2,624 rows (2020), 29,234 + 4,405 rows (2023 journals) |

Tested and quarantined what did not hold: HGB ties persistence, log-linear wins counts
(MAE 6.5 vs 11.3), LR-nlag overlay adds +0.032 on ON data only and zero off-site (archived OFF).
A second 1717 pair on a repaired copy exposed a 4.8× methodology break, so it stays out of
the tally (rules R1–R4 in docs/GUARDRAILS.md). Twelve reviewer rounds gated the work.
24 research tracks back the methods.

Shipped: 3 retrospective triage pages (ON, PK1, SRTO-1608) with heatmaps, audit tables, and
disclaimers; a prospective harness with IDENTICAL regression gates plus forward watchlists;
`src/gtk1/` package with byte-identical migration proofs; green test runner; partner runbook.

## How the data is organized

Raw files live outside the repo in `../Данные для предварительного изучения/`, one folder
per section, one subfolder per survey year. Each survey pairs an anomaly file with a weld or
pipe log. Formats vary (`.xls`, `.xlsx`, `.csv`; comma decimals in 2015 tables; R4 headers
mostly, R1/R2 in newer files). Coordinates are empty everywhere, so joins run on pipe number
plus odometer distance. Nothing raw enters git (hygiene gate in `run_tests.sh` enforces this).

## How the data is used

```
load (tolerant .xls/.xlsx reader) → normalize (Depth ≥ 10%, corr flag, pipe keys)
→ match past↔future per pipe → 100 m grid labels (matched-new binary)
→ B1 rank → watchlist + heatmap + audit columns
```

Reproduce:

```bash
pip install -r requirements.txt
bash run_tests.sh
python3 triage/prospective.py --section on --survey 2021 --check
python3 triage/prospective.py --section pk1 --survey 2025 --drop-last
```

## Progress and what is pending

Done: tasks 1, 2, 4, 6 fully; 3 and 5 partially (weak pipe-trait signals, no model near target);
7 as an honest below-target estimate. Frozen: B1-only triage, per-section thresholds, overlay OFF,
PK2 deferred, no new modeling on current surveys.

Pending (all external): repair logs, 5 file re-exports, pipe ages, per-survey thresholds and
methodology notes, two decodes (SRTO-1717-2021 Character, ON-2025 weld tail). Thresholds in
`configs/thresholds.yaml` stay placeholder until next-survey labels arrive. Then: calibrate
per section, validate the forward watchlists, revisit the overlay promotion rule.

## Map

`src/gtk1/` (io, match, features, metrics) · `src/research_tools/` (Exa/Firecrawl/Parallel/
TinyFish clients + quad fan-out) · `src/tests/` · `experiments/` (E01–E14 frozen) ·
`triage/` (pages, harness, watchlists) · `configs/` · `docs/` (PROBLEM, DATA, VALIDATION,
GUARDRAILS, TRIAGE_SPEC, RUNBOOK, OVERLAY_STATUS, research) · `outputs/` (ignored CSVs).

Rules: past-only features, no test tuning, negatives reported, single committer.
Details live in PROGRESS.md (append-only log) and AGENTS.md (project writing law).
