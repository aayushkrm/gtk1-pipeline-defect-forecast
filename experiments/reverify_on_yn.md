# Independent re-verification: ON 392–526 + YN 0–154 (read-only)

Date: 2026-10-07. Scope: 9 data files on disk (6 ON + 3 YN). Method: fresh
pandas/openpyxl/xlrd reads plus raw-inflate salvage (local-header parse, CRC
ignored, well-formed `<row>...</row>` pairing). No repo code was reused for
counts, except the vendored tolerant-xlrd patch for one file. No raw data
enters git. This file holds aggregates only.

Note on file count: the task brief says 12 data files. Only 9 exist in the
two folders. No other files are present. Verdict on "12": CORRECTED to 9.

## 1. Per-file results

Counts below use Distance-notna as the data-row definition. Header row is
1-based within the sheet.

### ON 2016/Аномалии.xlsx (523,729 bytes)
Sheets: `Общая информация` (14 strict rows), `Применяемые стандарты` (7),
`Аномалии` (1,909 strict `<row>` tags). All CRCs pass.
Anomaly sheet: header row 4 (R4), 44 columns. Data rows 1,907. Distance
3.3–132,222.6 m. Depth: n=1,650, median 12.0, 99.94% >=10 of measured.
Pipe coverage 100%.

### ON 2016/Поперечные сварные швы.xls (stock xlrd)
Sheets: `Общая информация` (19), `Применяемые стандарты` (9),
`Поперечные сварные швы` (11,862 incl header). Header 0-based row 3,
20 columns. Data rows 11,858. Distance 0–132,342.48 m. 11,858 unique pipes.

### ON 2021/Аномалии.xlsx (1,222,296 bytes)
Sheets: `Общая информация` (15), `Применяемые стандарты` (7), `Аномалии`
(4,457 strict tags), `Лист1` (61). All CRCs pass.
Anomaly sheet: header row 4 (R4), 45 columns. Data rows 4,455. Distance
3.3–132,339.2 m. Depth: n=3,513, median 11.0, 73.53% >=10 of measured.
Pipe coverage 100%.

### ON 2021/Поперечные сварные швы.xls (stock xlrd)
Sheets: info (20), standards (9), weld log (11,883 incl header). Header row 3,
21 columns (adds `Марка стали` vs 2016). Data rows 11,879. Distance
0–132,342.48 m, identical max to 2016. 11,879 unique pipes.

### ON 2025/Аномалии_.xlsx (1,444,827 bytes)
Sheets: `Общая информация` (13), `Аномалии` (6,600 strict tags). CRCs pass.
No standards sheet. Anomaly sheet: header row 4 (R4), 44 columns. Data rows
6,598. Distance 3.3–132,338.7 m. Depth: n=4,557, median 11.0, 82.31% >=10.
Pipe coverage 100%.

### ON 2025/Поперечные сварные швы.xls (tolerant-xlrd only)
Sheets: info (18), weld log (~3,471 parsed rows). Stock xlrd fails; tolerant
patch recovers it. BIFF ragged tail blows column count to 6,401 (garbage).
Usable rows: 2,461 Distance-notna, 2,462 pipe-nonempty. Distance 0–27,216.7 m.
The log ends at 27.2 km vs 132 km. Truncation CONFIRMED.

### YN 2020/Аномалии.xlsx (4,134,828 bytes, RECOVERABLE)
Sheets: `Общая информация` (14 strict, CRC ok), `Применяемые стандарты`
(7 strict, CRC ok), `Аномалии` (CRC fail, `BadZipFile`).
Salvage of sheet3: inflated 31,345,492 bytes; 2,629 `<row` starts; 2,624
well-formed rows. Header is row 2 (R2, not R4), 45 columns, SSID-first
schema close to the ON format. Title cell: `ЮРГА - НОВОСИБИРСК - 0 - 154,3`.
Data rows 2,622; Distance-notna 2,621, range 20.82–37,215.6 m. Depth:
n=2,620, median 30.0, 69.89% >=10. Pipe 2,621/2,622.
Coverage note: salvaged rows span only 0–37 km of the 0–154 km section.

### YN 2020/Поперечные сварные швы.xlsx (1,627,113 bytes, CLEAN)
Sheets: `Общая информация` (19), `Применяемые стандарты` (9),
`Поперечные сварные швы` (14,097 strict tags). All CRCs pass.
Weld sheet: header row 4 (R4), 22 columns (SSID + `Марка стали` included).
Data rows 14,095, all with Distance and pipe. Distance 0–151,492.155 m.
Pipe coverage 100%.

### YN 2023/otchet_скорр.xlsx (8,527,088 bytes, RECOVERABLE)
Sheet names (all 11): `Информация о трубопроводе`, `Обобщенная
статистическая инфор`, `Журнал выявленных особенностей`, `Журнал выявленных
аномалий`, `Трубный журнал`, `Журнал элементов обустройства и`, `Журнал
реперных точек`, `Журнал совмещения продольных сп`, `Журнал отводов
(поворотов)`, `Журнал упругопластических изгиб`, `Журнал косых стыков `.
Info sheet confirms `МГ Юрга - Новосибирск`, `Участок 0 - 154 км`,
`Диаметр 720`.
Strict full-read row counts: 114 / 103 / CRC-fail / CRC-fail / 14,161 /
327 / 81 / 829 / 587 / 6,198 / 16. Exact match with results_e15.json.
Headers: R1 (row 1) on sheets 5–11 and both journals. Sheets 1–2 are
key-value lists, not tables.
Per-sheet data rows (Distance-notna), columns, ranges:
- Pipe log: 10 cols, 14,160 rows, 0–151,491.31 m, pipe 14,160/14,160.
- Elements: 10 cols, 326 rows, 0.67–151,492.04 m.
- Repers: 9 cols, 80 rows, 0.67–151,492.04 m.
- Seams: 5 cols, 828 rows, 1,822.01–150,841.49 m.
- Bends: 11 cols, 586 rows, 9.52–151,465.54 m.
- Flexures: 13 cols, 6,197 rows, 38.46–151,475.98 m.
- Skew joints: 5 cols, 15 rows, 25,165.28–136,006.58 m.
- Features journal (sheet3): 18 cols, R1. Salvage: 29,497 starts,
29,235 well-formed (header + 29,234 data). Distance-notna 12,295/29,234,
range 0–60,462 m. Depth `d,%`: n=12,055, median 20.0, 99.98% >=10. Pipe
14,121 nonempty. Content is mixed (7,293 `Аномалия`, 4,635 weld rows,
17,171 rows with empty type).
- Anomaly journal (sheet4): 20 cols, R1. Salvage: 28,717 starts, 4,405
well-formed (header + 4,404 data). Distance-notna 4,399/4,404, range
3.45–25,655.08 m. Depth `d,%`: n=4,397, median 13.0, 99.98% >=10. Pipe
4,400/4,404. Character mix includes 1,181 `Труба 1Ш` separator rows.

### Distance-monotonicity on salvaged rows (row order, non-decreasing steps)
- Sheet3 features: 12,289/12,294 = 0.99959.
- Sheet4 anomalies: 4,396/4,398 = 0.99955.
- Pipe log: 1.00000 (strictly monotonic, 14,160 unique pipe keys 1–14093
with suffix variants).

## 2. Verdicts on repo numbers

1. ON counts 1907/4455/6598 as "E01 normalized Depth>=10": CORRECTED.
1,907 / 4,455 / 6,598 are the RAW Distance-notna counts. Recomputed here
exactly. The normalized Depth>=10 counts are 1,649 / 2,583 / 3,751.
Recomputed here exactly. The repo itself states 1,649/2,583/3,751
(results_e01.json, results_e01.md, PROGRESS.md line 12). That repo claim
is CONFIRMED. Only the label in the check request is wrong, not the repo.
2. ON weld overlap 11788/11858: CONFIRMED. Pipe-key sets (normalized
`75.0`→`75`): 2016 n=11,858, 2021 n=11,879, intersection 11,788,
union 11,949. Type match on overlap 11,745/11,788 = 99.64% (repo: 99.6%).
Distance delta on overlap: max 0.005 m, mean ~0.00001 m (repo: 0.000 m
at mm precision). Weld odometer ranges are identical (0–132,342.48 m).
Off-by-set pipes show splits (`11254` → `11254а`+`11254б`), 70 vs 91.
3. YN salvage 2,624: CONFIRMED (2,624 well-formed tags; 2,622 data rows).
4. YN salvage 29,234: CONFIRMED (29,235 well-formed tags incl R1 header;
29,234 data rows; 29,497 starts). My count differs from PROGRESS by
exactly the header row. Same result.
5. YN salvage 4,405: CONFIRMED (4,405 well-formed tags incl header; 4,404
data rows; 28,717 starts). 15.3% well-formed rate matches.
6. YN pipe log 14,160: CONFIRMED (14,161 strict rows = R1 header + 14,160
data rows, all with odometer and pipe key).
7. Odometer ranges: CONFIRMED. ON files span 0–132.34 km (section-relative
chainage; matches the 392–526 / 132 km section). YN files span 0–151.49 km
(matches 0–154 km at D720). ON-2025 weld ends at 27.2 km (truncation
claim holds). Salvage coverage limits: YN-2020A 0.02–37.2 km, YN-2023
anomaly journal 0.003–25.7 km, features journal 0–60.5 km on populated
rows. No salvaged YN anomaly series covers the full section.
8. Schema claims in DATA.md: CONFIRMED. ON anomalies 44/45/44 cols, R4
header. YN-2020A 45 cols, R2, SSID format (like ON). YN-2023 journals are
new format (features 18, anomalies 20, R1). The 2020-vs-2023 schema break
stands, so pair comparability needs proof.
9. E15 strict row counts (results_e15.json): CONFIRMED where checkable.
1,909 / 4,457 / 6,600 (ON anomalies), 14/7 and 19/9/11,862 and 20/9/11,883
weld info rows, 14 / 7 (YN-2020A good sheets), 14,097 (YN-2020 weld),
114 / 103 / 14,161 / 327 / 81 / 829 / 587 / 6,198 / 16 (otchet good
sheets). All match exactly.
10. NN odometer match ±2 m at 72.6% / 53.4%: UNVERIFIABLE here. It needs a
cross-year row-matching run, which is outside this file-level check.
Related fact verified: weld-log chainage is near-identical across years.

## 3. Bottom line

Every checkable repo number for these two folders reproduces exactly.
Two corrections: (a) 1907/4455/6598 are raw counts, not E01-normalized;
the repo does not make that error, its E01 numbers are right; (b) 9 data
files exist, not 12. One limit: salvaged YN anomaly series cover only
0–37 km (2020), 0–26 km (2023 journal), 0–60 km (2023 features), so no
full-section YN pair exists from salvage alone.
