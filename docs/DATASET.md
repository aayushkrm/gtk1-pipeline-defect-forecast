# DATASET: the ML dataset for training and validation (charter task 4)

Raw VTD files never enter git (32 files, sibling directory). This file defines the exact
derived dataset every model in this repo trains and tests on, so training is reproducible
from the raw room plus the commands below.

## Build chain (frozen R1)

`load_anomalies` → `normalize` (`src/gtk1/io.py`) → `match_win` (`src/gtk1/match.py`,
pipe+2m/0.5m/1h greedy) → `build` (`src/gtk1/features.py`, depth≥10% before matching,
100 m cells). Ranking score: past-count per cell normalized by section max (B1).

## Row schema (normalized frame)

dist (m), depth (%), pipe (id), off (m, NaN allowed), ori (clock string), char (type),
abbr, danger (Опасность string: (a)/(b)/(c) where assigned, else empty), kbd (numeric,
NaN where absent), corr (rust flag), h (clock hour, -99 unknown), cell (0..kmax).
Required columns raise explicit errors; optional columns default empty/NaN.

## Splits and labels (verified counts)

Label Y=1 iff a cell holds ≥1 UNMATCHED future corr row ≥10% (matched-new binary).

| Section | Train pair | Test pair | Cells | Test positives | Test prevalence |
|---|---|---|---|---|---|
| ON 392–526 | 2016→2021 | 2021→2025 | 1331 | 357 | 0.2682 |
| PK1 572–714 | — | 2022→2025 | 1401 | 562 | 0.4011 |
| SRTO-1608 | 2016→2021 | 2021→2024 | 1041 | 63 | 0.0605 |

Counts from `results_e11.json` (PK1), `results_e17.json` (ON/SRTO test positives),
`triage/*.json` (prevalence). E10 (13 positives) and E14 (void) never enter training.

## Known contaminations (labeled, not hidden)

- Vanished share 0.36–0.60 by definition: unmatched past rows mix repairs, misalignment,
  and sensitivity loss. Persistent-disappearance candidates: 406 ON, 121 SRTO-1608
  (`results_repair.json`); reappeared controls excluded (163/51).
- ABC regime break ~2022: ab-shares spike then collapse on all full sections
  (`results_danger.json`); per-class labels need Leonid's mapping before training use.
- Tool sensitivity jumps 2–5x between surveys: counts never compare across years without
  matched-pair labels. Thresholds stay per-section and uncalibrated (`configs/thresholds.yaml`).

## Rebuild commands

```bash
pip install -r requirements.txt
bash run_tests.sh                                            # offline gates
python3 triage/prospective.py --section on --survey 2021 --check   # IDENTICAL required
python3 experiments/evaluate_pair.py --section on --past 2021 --future 2025
python3 experiments/evaluate_pair.py --section pk1 --past 2022 --future 2025
```

## Class balance note

Dense sections carry 27–40% positive cells (learnable); SRTO-1608 carries 6% (wide CIs);
SRTO-1717 carries 13 positives (suggestive only, never training). Imbalance handling:
none at training time (bootstrap resampling serves uncertainty intervals only).
