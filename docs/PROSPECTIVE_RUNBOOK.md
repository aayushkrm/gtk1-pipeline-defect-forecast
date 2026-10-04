# PROSPECTIVE RUNBOOK — running the watchlist on the NEXT survey

Partner-facing procedure for generating a ranked 100 m-segment watchlist from a
**newly arrived VTD anomaly file**. B1 past-count ranking only; no future labels
needed. Scope: ON + PK1 (December freeze; reviewer round 10).

B1 model: per-100 m cell count of past-survey corrosion rows with Depth ≥ 10%,
score = count / max-count. "New" everywhere below means
**newly-reported ≥ 10% row under pipe+2 m/0.5 m/1 h greedy match** — an
operational reporting definition, NOT physical corrosion prediction
(docs/GUARDRAILS.md).

---

## 1. Prerequisites

- Python 3 (`python3 --version`; runs on this machine's Python 3.9.6).
- Install deps from repo root `gtk1-forecast/`:
  ```bash
  pip install -r requirements.txt
  ```
  (`requirements.txt`: pandas≥2.0, numpy≥1.26, pyarrow≥14, openpyxl≥3.1,
  xlrd≥2.0, xlrd2≥1.3, scikit-learn≥1.3, scipy≥1.11, pyyaml≥6.0,
  matplotlib≥3.8.)
- Raw VTD files are **never committed** (`.gitignore`; `run_tests.sh` hygiene
  gate fails the run if any `.xls/.xlsx/.csv` is tracked). Data lives in the
  sibling directory:
  ```
  ../Данные для предварительного изучения/<section-dir>/<YEAR>/<anomaly file>
  ```
- Where to place the new anomaly file (Russian directory names are literal):

  | `--section` | section directory | year dir example | accepted filenames |
  |---|---|---|---|
  | `on` | `Омск-Новосибирск (392-526)` | `.../Омск-Новосибирск (392-526)/2026/` | `Аномалии.xlsx`, else `Аномалии_.xlsx` (first existing wins) |
  | `pk1` | `Парабель-Кузбасс-1 (572-714)` | `.../Парабель-Кузбасс-1 (572-714)/2026/` | first `Аномалии*.xls*` glob match |

  (Source of truth: `SECTIONS` dict in `triage/prospective.py:14-20`.)
- Expected schema: **44/45-col anomaly sheet, R4 header** (header row index 3;
  loader default `src/gtk1/io.py:55`). Required columns (matched by substring,
  case-insensitive):
  - Distance — contains `расстояние`
  - Pipe No — contains `номер` + `трубы`
  - Depth — contains `глубина`
  - Character — contains `характер` (**mandatory**; loader fails without it)
  - Optional: weld offset (`левого…`), orientation (`ориентация…`),
    character abbr (`характер` + `аббр`).
  - Corrosion flag = Character contains `оррози`; ranking uses corr-only rows
    with Depth ≥ 10% (`triage/prospective.py:37-38`).

## 2. Commands (run from repo root `gtk1-forecast/`)

### 2a. Regression gate FIRST (`--check`) — no new data needed

Verifies the harness still reproduces the shipped retrospective pages exactly:
top-20 cells + past_counts + scores (tolerance 1e-12) vs
`triage/triage_demo.json` → `top20` (ON) and `triage/triage_pk1.json` →
`top20` (PK1). Prints `regression_vs_shipped: IDENTICAL`; any mismatch raises
`SystemExit: REGRESSION MISMATCH`. Run **without** `--drop-last` (frozen pages
pre-date the edge guard).

```bash
python3 triage/prospective.py --section on --survey 2021 --check
python3 triage/prospective.py --section pk1 --survey 2022 --check
```

Do not proceed to a forward watchlist if either gate reports MISMATCH.

### 2b. Forward watchlist on the NEXT survey — always with `--drop-last`

`--drop-last` (E13 edge guard): excludes the boundary cell
(ON cell 1330 / PK1 cell 1400 — overrun rows accumulate there by construction),
renormalizes scores over the remaining cells, logs the dropped cell in
`edge_guard`. Adopted as DEFAULT for all prospective watchlists
(docs/GUARDRAILS.md); retrospective pages stay unchanged. Replace `YYYY` with
the new survey year:

```bash
python3 triage/prospective.py --section on --survey YYYY --drop-last
python3 triage/prospective.py --section pk1 --survey YYYY --drop-last
```

Concrete past examples (already in `triage/` + `outputs/`):

```bash
python3 triage/prospective.py --section on --survey 2025 --drop-last     # top cell 173 (unremarkable)
python3 triage/prospective.py --section pk1 --survey 2025 --drop-last    # drops cell 1400 (211 counts artifact); new top-1 = cell 438 (114)
```

Artefacts per run: committable summary
`triage/watchlist_<section>_<survey>_noedge.json` + full ranked list
`outputs/watchlist_<section>_<survey>_noedge.csv` (git-ignored).
Grid sizes: ON kmax 1330 → 1331 cells; PK1 kmax 1400 → 1401 cells.

## 3. Recalibration procedure (`configs/thresholds.yaml`)

Current content is **placeholder, uncalibrated** (`survey_basis` 2021 ON /
2022 PK1, `flag_top_k: 20`, `review_band_score: 0.10`). Recalibration is only
possible once the next survey's labels exist, i.e. a completed past→future
pair evaluated with the frozen pipeline (Depth ≥ 10%, pipe+2 m/0.5 m/1 h
greedy match, 100 m matched-new, same pattern as `experiments/e11_pk1.py`):

1. Build matched-new labels for the completed pair; compute B1 AP vs base AP
   + 2000-bootstrap lift CI, and P@K with base comparator.
2. Per section, set `flag_top_k` (how many top cells to flag for field review)
   and `review_band_score` (score down to which cells stay in the review band)
   from that section's own test numbers (e.g. keep P@K≈1.0 region flagged,
   band down to where precision falls to base rate).
3. Update `survey_basis` to the new past-survey year, set `status: calibrated`,
   keep a one-line provenance note (experiment result file + git hash).
4. **Rule: never pool thresholds across sections.** AP spread is 0.18–0.78
   across sections (ON 0.644, PK1 0.779, SRTO-1608 0.277, SRTO-1717 0.181);
   one section's operating point does not transfer (reviewer round 8,
   docs/GUARDRAILS.md). ON and PK1 entries are edited independently.

## 4. How to read outputs

### Top-20 JSON (`triage/watchlist_<section>_<survey>[_noedge].json`)

| field | meaning |
|---|---|
| `section` / `survey` / `file` | what was ranked, incl. source filename |
| `model` | always `B1 past-count only (prospective, no future labels)` |
| `recalibration` | `placeholder — per-section thresholds uncalibrated until next survey` until §3 is done |
| `edge_guard` | `null` without `--drop-last`; else `{"cell": <boundary>, "past_count": N}` — the excluded artifact cell |
| `top20[]` | `{"rank": 1..20, "cell": <100 m cell id>, "past_count": <corr ≥10% rows in cell>, "score": <0..1>}`; `score = past_count / max past_count` (post-guard renormalization); ties keep stable input order |
| `score_deciles` | `[p0, p25, p50, p75, p90, p99, p100]` of the full score vector — use to see how flat/peaked the ranking is |
| `nonzero_cells` / `n_cells` | cells with ≥1 past corr-≥10% row, over total (e.g. PK1-2025: 830/1401) |
| `regression_vs_shipped` | present only with `--check`: `IDENTICAL` or run aborts |

### Full CSV (`outputs/watchlist_<section>_<survey>[_noedge].csv`)

Columns: `cell,km,past_count,score` — one row per cell, rank order
(`km = cell / 10`, `score` to 4 dp). This is the inspectable watchlist; the
JSON top-20 is its head. CSVs are git-ignored by design.

## 5. Limitations — read before acting on a watchlist

- **Thresholds are placeholders.** `flag_top_k: 20` / `review_band_score: 0.10`
  are display defaults, not validated operating points (see §3).
- **Repair exclusion pending.** ~2.8% deep-vanished tail is repair-suspect;
  repair logs were never delivered, so vanished rows cannot be excluded —
  absolute AP is conditional on this contamination (E08, docs/TRIAGE_SPEC.md).
- **AP is cut-conditional.** Primary cut ≥ 10%; sensitivity cuts ≥ 12%/≥ 15%
  change prevalence and AP (ON 0.644/0.546/0.364; PK1 0.779/0.574/0.375).
  Always quote the triple, plus match-rate and vanished-frac (GUARDRAILS
  disclaimer, mandatory on every handover).
- **Operational framing only.** The tool predicts *newly-reported* defects
  (initiation + re-detected misaligned old + sensitivity gain), NOT physical
  corrosion. No ≥ 80% reliability claim is supportable.
- **When NOT to use:** do not pool one section's thresholds onto another; do
  not use the LR-nlag overlay (archived OFF, docs/OVERLAY_STATUS.md); do not
  attach red/green pass-fail badges or reliability meters; do not run without
  `--drop-last` on new surveys (boundary-cell artifact); do not apply to
  sections without a same-section validated pair (PK2/Y-N are out of scope).

## 6. Troubleshooting

- **BIFF / corrupt `.xls` read errors** (`Unsupported format`, assert or
  struct errors from xlrd): the loader (`src/gtk1/io.py:55-64`) tries the
  stock engine first, then re-reads with vendored tolerant-xlrd patches
  (`_apply_tolerant_xlrd`: ragged-cell asserts, XF-index fallback,
  shared-string-index guard). No action needed if the second attempt succeeds —
  this is the expected path for CRC-truncated files (e.g. PK1-2025A, 99.4%
  recovered). `put_cell` console chatter is xlrd debug noise, harmless (E11).
  If both attempts fail, the file is unrecoverable in this harness (cf.
  PK1-2019A: rows 2864+ absent) — request a re-export from source
  (docs/TRIAGE_SPEC.md § Partner data requests).
- **Wrong / empty columns after load** (Distance/Pipe/Depth not found):
  intact files use the R4 header (`header=3`, the harness default). Damaged or
  new-format files use R2/R1 header rows (docs/DATA.md). Diagnose with plain
  pandas before touching the harness:
  ```bash
  python3 -c "import pandas as pd; [print(i, list(pd.read_excel('FILENAME', sheet_name='Аномалии', header=h, engine='openpyxl', nrows=0).columns)[:6]) for h in (1,2,3)]"
  ```
  then re-export with the intact R4 layout; the harness accepts only R4.
- **Comma decimals** (2015-era 23-col schema: `3,3`-style depths, comma
  markers): `normalize` (`src/gtk1/io.py:83-85`) parses with
  `pd.to_numeric(errors="coerce")` and does NOT convert commas — mass-NaN
  depth/distance means comma decimals. Pre-convert commas to dots in a copy of
  the file before running. (PK2-2015 schema is out of December scope
  regardless.)
- **All-zero / tiny `nonzero_cells`**: check you pointed at the anomaly sheet
  named `Аномалии` and that Depth values are percent (a unit or column variant
  silently drops every row at the ≥ 10% filter).
- **PK1-2025-style top-1 outlier** (top cell ≫ #2, last cell id 1400): you
  forgot `--drop-last`. Re-run with the flag.
