# Re-verification: SRTO claims (GTK1, independent)

Scope: all SRTO data files + every SRTO number in `README.md` table,
`docs/TRIAGE_SPEC.md` expected-numbers, `experiments/results_e05.json`,
`results_e10.json`, `results_e14.json`.
Method: read-only. Stock `xlrd` / `openpyxl` first (strict verdict),
repo tolerant reader (`src/gtk1/io.py`) fallback, raw zip/XML salvage
for the corrupt `.xlsx`. Experiment inputs re-ran with repo code
(`e05_srto`, `e10_srto1717`, `e07_ablation.raw`, `e07b_null.build`).
No data or repo files changed. No commits.

Verdicts: CONFIRMED / CORRECTED / UNVERIFIABLE / UNRECOMPUTED (AP figures:
inputs checked, AP math not re-run, per task) / OUT-OF-SCOPE (other sections).

Related docs read first: `docs/DATA.md`, `README.md`, `docs/TRIAGE_SPEC.md`,
`results_e05/e10/e14` (`.json` + `.md`), `experiments/e05_srto.py`,
`e10_srto1717.py`, `e14_1717pair2.py`, `src/gtk1/io.py`, `src/gtk1/features.py`,
`PROGRESS.md` salvage entries.

## 1. File inventory — CORRECTED (11, not 12)

Task states 12 data files. Both folders hold 11 data files + 2 `.DS_Store`.
No file missing: 1608 section 6 files (2016/2021/2024 anomaly + weld each),
1717 section 5 files (2016 KP-book, 2021 anomaly + weld, 2024 anomaly + weld).

## 2. Per-file results

Header convention: experiments use 0-based row 3 (R4). Detector scans rows 0–11
for distance keywords. Depth shares use two denominators: all data rows (A)
and measured (non-null depth) rows (M). Pipe coverage = non-empty Pipe No.

### 2.1 SRTO-Omsk 1608–1717 / 2016 / Аномалии.xls (473088 B, strict OK)

Sheets: Общая информация 19×4, Применяемые стандарты 9×2, Аномалии 581×45.
Header R4 (0-based 3). Data rows 577. Distance 22.09–103957.47 m, all valid.
Depth measured 462 (80.1%), median 12.0, ≥10%: 462 = 80.1% (A) / 100% (M).
Pipe 100%, 326 unique. SSID column present. Tail order: …Опасность, КБД,
Pd, MAOP, Psw, Pf, Срок НО. Info sheet: 18.04.2016, 0–104 km, D1220.

### 2.2 SRTO-Omsk 1608–1717 / 2016 / Поперечные сварные швы.xls (3847168 B, strict OK)

Sheets + Поперечные сварные швы 9419×20. Header R4. Data rows 9415.
Distance 0–104347.06 m. Pipe 100%, 9415 unique.

### 2.3 SRTO-Omsk 1608–1717 / 2021 / Аномалии.xls (2277376 B, strict OK)

Sheets: info 18×4, standards 9×2, Аномалии 3172×44. Header R4. Data rows 3168.
Distance 18.43–104337.99 m. Depth measured 1834 (57.9%), median 9.0,
≥10%: 786 = 24.8% (A) / 42.9% (M). Pipe 100%, 1750 unique. No SSID column.
Tail order flipped vs 2016: …Срок НО, КБД, Pd, MAOP, Psw, Pf, Опасность.
Info: 31.03.2021, 0–104 km, D1220.

### 2.4 SRTO-Omsk 1608–1717 / 2021 / Поперечные сварные швы.xls (2215424 B, strict OK)

Weld sheet 9422×21. Data rows 9418. Distance 0–104347.055 m. Pipe 100%.

### 2.5 SRTO-Omsk 1608–1717 / 2024 / Аномалии1.xls (2422272 B, strict OK)

Sheets: info 18×4, Аномалии 2348×45 (no standards sheet). Header R4.
Data rows 2344. Distance 18.43–104337.99 m. Depth measured 1452 (61.9%),
median 13.0, ≥10%: 1263 = 53.9% (A) / 87.0% (M). Pipe 100%, 1427 unique.
SSID present. Tail order same as 2021. Info: 06.03.2024, 0–104 km, D1220.
File glob `Аномалии*.xls*` resolves to `Аномалии1.xls`. Matches E05 loader.

### 2.6 SRTO-Omsk 1608–1717 / 2024 / Поперечные сварные швы.xls (4315136 B, strict OK)

Weld sheet 6299×23. Data rows 6295. Distance 0–70541.24 m (70.5 km only;
pipes end at 6275). OBSERVATION: covers ~68% of the 104 km section while
2016/2021 weld logs reach 104.3 km. `DATA.md` truncated list does not name it.
No repo claim conflicts (E05 does not use weld logs). 23 columns (adds SSID,
Марка стали, Температурный перепад).

### 2.7 SRTO-Omsk 1717–1759 / 2016 / KP book (2674176 B, strict OK)

8 sheets. CONFIRMS "2016-8sheet" claim.
Общая информация 19×4 (file stamp 08.04.2022, survey tools March 2016 —
CONFIRMS E10 "2022 stamp / mixed provenance" note; section 0–42 km, D1220).
Сводка результатов 49×2. Выявленные особенности 4265×42 (data 4261;
dist 0–42018.5; depth measured 113 (2.7%), median 12.0, ≥10% 113 = 2.7% (A) /
100% (M)) — CONFIRMS "42-col mixed". Аномалии 355×44 (data 351;
dist 621.85–41444.0; depth measured 113 (32.2%), median 12.0, ≥10% 113;
pipe 100%, 223 unique). E10 loads this Аномалии sheet. Weld 3814×20
(data 3810; 0–42018.5). Реперы 18×11 (14 data). Обустройства 65×11 (61 data).
Отводы 152×14 (no distance header). Character empty 0%, Danger empty 0%,
KBD empty 68.1%, lat/lon 100% empty on the Аномалии sheet.

### 2.8 SRTO-Omsk 1717–1759 / 2021 / Аномалии.xls (820224 B, strict OK)

Sheets: info 20×4, standards 9×2, Аномалии 1455×44. Header R4.
1451 rows after header, of which 913 (62.9%) carry Distance; 538 rows are
fully empty in two blocks (237 + 301) and drop out via pipeline `dropna`.
Distance 19.6–29998.91 m. CONFIRMS "~30/42 km" coverage (weld log spans
full 42.0 km; anomaly survey stops at 30.0 km). Depth measured 168
(11.6% A / 18.4% of dist-valid), median 10.0, ≥10%: 93 rows total,
92 with Distance (exactly one depth≥10 row lacks Distance — explains E10 92).
Pipe 913 (100% of dist-valid). Character empty 37.08% — CONFIRMS TRIAGE_SPEC
"Decode empty Character (SRTO-1717-2021, 37%)". Danger empty 37.0%.
KBD empty 94.9%. Lat/lon 100% empty. Info: 08.04.2021, 0–42 km, D1220.

### 2.9 SRTO-Omsk 1717–1759 / 2021 / Поперечные сварные швы.xls (893952 B, strict OK)

Weld sheet 3815×21. Data rows 3811. Distance 0–42018.5 m. Pipe 100%.

### 2.10 SRTO-Omsk 1717–1759 / 2024 / Аномалии.xlsx (271654 B, strict FAIL)

`openpyxl` strict read fails (`ParseError`, invalid token).
`xl/sharedStrings.xml` has Bad CRC-32. Sheet parts inflate fine (CRC OK).
sheet1 = 13 rows (info). sheet2 = 1220 wellformed rows: title + one 44-cell
string row at 0-based 1 (R2 header — matches "R2 in damaged/new") + 1218 data
rows. Distance (col 0): 1218/1218 numeric, 19.6–42015.8 m (full 42 km).
Pipe-position column: 922/1218 with values (909 numeric + 13 string).
Depth column not name-identifiable (string table broken); positional candidate
col 30 (type-n, 0.2–90.0) gives 1076 ≥10, which does not map to any
repaired-copy figure — no conclusion drawn, artifact differs. No denormal
(`3.3e-307`-style) garbage cells found. CONFIRMS `DATA.md` corrupt listing
("bad CRC/XML"). Row counts + distance range verified from SOURCE only, per task.
Danger-82%-empty (DATA.md) is UNVERIFIABLE from source.

### 2.11 SRTO-Omsk 1717–1759 / 2024 / Поперечные сварные швы.xlsx (331914 B, qualified OK)

`openpyxl` read-only mode fails (`TypeError`, engine artifact); default mode
reads cleanly: info 18×4, weld 3816×22, R4 header, 3812 data rows,
0–42018.5 m, pipes 3812 unique. Verdict: readable with standard parser.
Consistent with repo (not listed as corrupt). 22 columns.

## 3. Coverage checks

1608–1717 ~104 km: CONFIRMED. Info sheets state 0–104 km all surveys;
anomaly distances reach 103957–104338 m; 2016/2021 weld logs reach 104347 m.
Exception: 2024 weld log stops at 70541 m (section 2.6 observation).

1717–1759 2021 ~30/42 km: CONFIRMED. Anomaly max 29998.91 m; weld log 42018.5 m.

2024 repaired copy row counts: UNVERIFIABLE. Artifact
(`.../repair_spike/GTK1_2024_Anomalii_REPAIRED.xlsx`, 269882 B per E14 JSON)
absent from `/tmp` and scratch areas. Source row count: 1218 data rows.

## 4. results_e05.json — inputs CONFIRMED, AP UNRECOMPUTED

Re-ran `load_any` + `norm` + `match_win` with repo code. Identical values:
counts 2016/2021/2024 = 462/786/1263; train (2016→2021) match 0.367684,
prev 0.100865, n_pos 105; test (2021→2024) match 0.551069, prev 0.060519,
n_pos 63. File bytes 473088/2277376/2422272 match JSON (mtimes not checked).
B1/B2/B3 figures (0.530/0.101/0.381 train; 0.277/0.061/0.211 test):
UNRECOMPUTED per scope (inputs they rest on verified).

## 5. results_e10.json — inputs CONFIRMED, AP UNRECOMPUTED

Shapes (351,44)/(1451,44); raw rows 351/913; counts d≥10 = 113/92;
match 0.260870, prev 0.030879, n_pos 13; KMAX 420 → 421 cells. All match JSON.
Bytes 2674176 sole entry matches KP file. B1_AP 0.18073, base, lift CI
[0.0243, 0.4152]: UNRECOMPUTED (base/prev/pos inputs verified; CI lower > 0
as cited). The 93-vs-92 question resolved: 93 depth≥10 rows pre-`dropna`,
one lacks Distance → pipeline legitimately counts 92.

## 6. results_e14.json — split verdict

2021_d10 = 92: CONFIRMED from source file via `gtk1.io.normalize`.
2024_d10 = 440, dropped placeholders = 5, match 0.134, prev 0.0998, n_pos 42,
n = 421, AP 0.201, lift CI: UNVERIFIABLE (repaired artifact absent; per task
no re-derivation attempted). AP figures additionally UNRECOMPUTED per scope.
Arithmetic check only: 440/92 = 4.7826 → "4.8×" / "4.78" citations are
correct arithmetic on cited inputs (one side unverifiable).

## 7. README.md table (SRTO rows)

SRTO–Omsk 1608–1717, "2016→2021 / 2021→2024, 0.530 / 0.277 (test, 63
positives)": CONFIRMED. Train B1 0.53018 and test B1 0.27666 round as cited
(AP math UNRECOMPUTED); test n_pos 63 CONFIRMED by re-run.
SRTO–Omsk 1717–1759, "2016→2021, 0.181 / 0.031 (13 positives)": CONFIRMED
modulo AP scope (0.18073→0.181 UNRECOMPUTED; base 0.03088→0.031 and pos 13
CONFIRMED). "Second 1717 pair ... 4.8× methodology break ... stays out of
the tally": consistent with E14 JSON + PROGRESS void note; 2024-side inputs
UNVERIFIABLE. ON/PK1/PK2/YN table rows: OUT-OF-SCOPE (sibling tracks).

## 8. TRIAGE_SPEC expected-numbers (SRTO parts)

"SRTO B1 0.277, LR 0.281, Δ +0.004 [−0.032,+0.039]": B1 CONFIRMED by re-run
(0.27666). LR 0.28114, Δ 0.00448, CI [−0.0317,+0.0395] match
`results_e07b.json` SRTO_holdout exactly (E07b out of scope: values
JSON-consistent, UNRECOMPUTED). Rounding as cited checks out.
"~0.28 SRTO at 6% prevalence": CONFIRMED (prev 0.06052).
"SRTO-1717 0.181/0.031 (13 pos, liftCI lower>0; 2021 covers ~30/42km)":
CONFIRMED modulo AP scope (pos/base/coverage re-verified; liftCI lower
0.0243 > 0 from JSON, UNRECOMPUTED).
ON headline, PK1 0.779/0.574/0.375 + 562 pos, count MAE, task-definition
60%/39% and 0.27→0.08: OUT-OF-SCOPE.

## 9. DATA.md (SRTO parts)

Section lines (ranges, D1220, survey years, 8-sheet 2016 book): CONFIRMED.
"Anomaly tables 44/45 cols, R4 (R2/R1 damaged/new)": CONFIRMED
(45/44/45 R4; 44/44 R4; 2024 44-col R2).
"Pipe tables 20→30 cols": QUALIFIED — SRTO shows 20/21/23/20/21/22
(max 23; global upper bound needs other sections).
"KP-2016 42-col mixed": CONFIRMED.
QC corrupt list naming SRTO-1717-24A: CONFIRMED. Other files OUT-OF-SCOPE.
"Tail order flips 2016 vs 2021+": CONFIRMED (headers transcribed in 2.1/2.3).
"SSID does not persist": CONFIRMED structurally (present 2016/2024, absent 2021).
"Lat/Lon 0%": CONFIRMED (100% empty in all five readable SRTO anomaly sheets).
"Depth covers 66–100%": CORRECTED for SRTO subset — measured 80.1/57.9/61.9/
32.2/11.6% (only 1608-2016 inside range).
"KBD covers 58–86%": CORRECTED for SRTO subset — non-empty 79.9/47.2/30.2/
31.9 (KP-Anom)/5.1%.
"Pipe No covers 100%": QUALIFIED — 100% in 1608 anomalies, KP-Anom sheet,
all weld logs; 1717-2021 100% of dist-valid rows (62.9% of raw sheet
including 538 empty rows the pipeline drops).
"Service 2016 100y fictive": CONSISTENT (21.3% of 1608-2016 Срок НО exactly 100;
0% in 2021/2024).
"SRTO-1717-24 Danger 82% empty": UNVERIFIABLE from source (sst broken;
artifact absent). For reference 1717-2021 Danger empty = 37.0%.
Long-seam m-vs-mm mislabel: not observed in SRTO anomaly files (columns
already labeled мм) — remainder OUT-OF-SCOPE.

## 10. Verdict summary

CONFIRMED: per-file sheets/headers/columns/row counts (except repaired copy);
E05 + E10 counts/match/prev/pos; E14 2021_d10; README SRTO rows; TRIAGE_SPEC
SRTO B1/base/pos/CI-sign/coverage/Character-37%; DATA.md section lines,
schemas, KP-2016 mixed sheet, corrupt listing, SSID/LatLon/tail-flip claims.
CORRECTED: file count 12→11; Depth/KBD global ranges do not describe SRTO
subset (values tabulated). QUALIFIED: pipe-table 20→30 (SRTO max 23);
Pipe-No 100% (1717-2021 raw sheet has empty-row blocks); 2024 weld xlsx
needs default (non-read-only) openpyxl mode.
UNVERIFIABLE: all E14 2024-side numbers, dropped-5, Danger-82%,
repaired-copy row counts (artifact absent; no re-derivation per task).
UNRECOMPUTED (per scope, inputs verified): all AP/B1/B2/B3/LR/lift-CI math.
OUT-OF-SCOPE: ON/PK1/PK2/YN files and numbers.
OBSERVATION (no claim conflict): 1608-2024 weld log covers 0–70.5 km only.
