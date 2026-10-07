# PK re-verification: Parabel-Kuzbass-1 (572-714) and Parabel-Kuzbass-2 (0-110)

Independent re-read of all 12 data files in the two PK folders. Read-only. No data files changed. No commits.
Repo claims checked against `docs/DATA.md`, `experiments/results_e15.json`, `experiments/results_e15.md`,
`experiments/results_e11.json`, `experiments/results_e11.md`, `experiments/results_e12.json`,
`README.md` PK rows, and `PROGRESS.md` PK entries.

Method per file: container check (ZIP CRC per sheet part for `.xlsx`, xlrd open for `.xls`),
sheet list, header-row detection (first row of 8 that holds a distance word), full strict parse,
tolerant-xlrd fallback for `.xls`, raw-deflate plus shared-string resolution for corrupt `.xlsx`
(the referenced `tolerant.py`/`salvage.py` no longer exist under `/tmp`; the patches were
re-implemented inline from `experiments/e11_pk1.py` and `src/gtk1/io.py`, same logic).
`strict_rows` in `results_e15.json` means physical sheet rows including header rows.
`data rows` below means rows under the detected header row.

Share `>=10` always states its denominator: all data rows, or measured-only (rows with a parsed depth).

## File 1: PK1 2019 anomalies (`Парабель-Кузбасс-1 (572-714)/2019/Аномалии.xlsx`, 1387569 B)

Sheets: `sheet3.xml` (anomaly table, CRC fail), `sheet2.xml` (7 row tags, rows 2-9), `sheet1.xml`
(18 row tags, rows 2-23 with gaps at 3, 5, 10, 12). Strict openpyxl parse fails on the workbook.
Header row: file row 4 (R4). Columns: 44, old layout without SSID (first header `Расстояние, м`).
Data rows: 2859 (file rows 5-2863, contiguous except the header slot).
Depth (`Глубина, %`): measured 2857 of 2859, median 12.0, rows `>=10` 2822, share 0.987 all-rows
and 0.988 measured-only.
Distance: 2859 of 2859 parsed, min 72.183 m, max 44967.212 m (0.07-44.97 km).
Pipe coverage (`Номер трубы`): 1017 distinct pipes, zero missing.
Character: Коррозия 2324, Аномалия кольцевого шва 380 (GWAN share 0.133), Механическое
повреждение 79, Вмятина 35, Заводской дефект 14, rest small.
Tail: max row number present is 2863. Rows 2864+ are absent from the file (never written,
not garbled). Garble: 6032 `<row>` tags exist but only 2867 carry row numbers; the surplus
untagged row fragments are the duplication garble.

## File 2: PK1 2019 welds (`Парабель-Кузбасс-1 (572-714)/2019/Поперечные сварные швы.xlsx`, 1578698 B)

Sheets: `Общая информация` (23 x 4), `Применяемые стандарты` (9 x 2),
`Поперечные сварные швы` (dimension A2:V14072, CRC fail on `sheet3.xml`). Header row 4.
Columns: 21 (weld-log layout: `Номер трубы`, `Расстояние, м`, `Длина трубы, м`, ... `Марка стали`).
Data rows: 11410 row elements under the header (dimension promises 14071, so about 19% never parsed
as rows at all). Distance valid (0-150000 m filter): 9060 rows, min 11.635 m, max 89805.129 m
(0.01-89.8 km). Pipe coverage over valid rows: 8521 distinct pipes.
Garble: row numbers run to 9047999914069066, one 13-character empty row repeats 768 times,
out-of-range shared-string indices leak as values near 9000000003.0. This sheet is the clearest
duplication-garble case of the set. No depth column exists in weld logs.

## File 3: PK1 2022 anomalies (`Парабель-Кузбасс-1 (572-714)/2022/Аномалии.xls`, 6195200 B)

Stock xlrd opens it. Sheets: `Общая информация` (19 x 4), `Применяемые стандарты` (9 x 2),
`Аномалии` (10743 x 44). Header row index 3. Columns: 44.
Data rows: 10739. Distance: 10739 parsed, min 60.655 m, max 140772.959 m (0.06-140.8 km).
Depth: measured 10094 of 10739 (0.940), median 12.0, rows `>=10` 8982, share 0.836 all-rows
and 0.890 measured-only. Pipe coverage: 4333 distinct pipes, zero missing.
GWAN (`Характер особенности` holds `кольцевого`): 2580 rows, share 0.240.

## File 4: PK1 2022 welds (`Парабель-Кузбасс-1 (572-714)/2022/Поперечные сварные швы.xls`, 3715072 B)

Stock xlrd opens it. Weld sheet 14097 physical rows. Header row index 3. Columns: 22.
Data rows: 14093. Distance: all parsed, min 14.3 m, max 140852.334 m. Pipes: 14093 distinct,
one pipe per row, zero missing. No depth column.

## File 5: PK1 2025 anomalies (`Парабель-Кузбасс-1 (572-714)/2025/Аномалии.xls`, 21744640 B)

xlrd lists sheets (`Общая информация` 18 rows, `Аномалии` 21767 rows) but the anomaly sheet
parses only with tolerant-xlrd patches (ragged-cell asserts fire; the `put_cell` console noise
is expected). Header row index 3. Columns: 44. Data rows: 21763.
Distance: 21638 parsed (125 rows lack distance), min 60.655 m, max 140830.086 m.
Depth: measured 10554 of 21763 (0.485), median 11.0, rows `>=10` 8989 after the E11 dist-drop
(8990 before it; one `>=10` row has no distance), share 0.413 all-rows and 0.852 measured-only.
Pipe coverage: 7379 distinct pipes, 124 rows lack a pipe number.
GWAN: 10933 rows, share 0.502. Weld-class block: 11209 rows have NaN depth, 10929 have zero
length, 10428 sit at zero distance to the girth weld. Offsets are ordinary (max 11.719 m,
no huge values in the offset columns).

## File 6: PK1 2025 welds (`Парабель-Кузбасс-1 (572-714)/2025/Поперечные сварные швы.xls`, 8189952 B)

DEAD. Stock xlrd raises AssertionError; tolerant-xlrd patches raise AssertionError too.
No sheet list is readable. Nothing further recoverable by parser patches.

## File 7: PK2 2015 defect table (`Парабель-Кузбасс-2 (0-110)/2015/Таблица дефектов 2015.xlsx`, 2833901 B)

ZIP CRCs pass. Sheets: `Таблица дефектов` (18338 x 23), `Лист1` (152 x 20, support sheet).
Header row index 0 (R1). Columns: 23 (`№ в ТА`, `Труба`, `Тип особенности`, `Характер особенности`,
`Класс размера`, `Дистанция, м`, `От шва, м`, `Длина, м`, `Ширина, м`, `Mакс. глубина, %`,
`Угол, час`, `Тип дефекта`, `КБД`, `Срок обследования, годы`, `Примечание`, `№ дефекта на трубе`,
`Расстояние от(+)/до(-) реперной точки, м`, `Расстояние от(+)/до(-) поперечного шва, м`,
`Оценка макс. глубины, мм`, `Тип трубы`, `Длина трубы, м`, `Угловое расположение шва, ЧЧ:ММ`,
`Толщина стенки трубы, мм`). Data rows: 18337.
Comma decimals are real here and must be handled explicitly: `Дистанция, м` is stored as text
such as `100027,992` (object dtype; 194734 comma cells sheet-wide). After comma-to-dot
conversion: 18337 parsed, min 117.784 m, max 112148.197 m (0.1-112.1 km). The depth column is
stored integer (int64, no comma issue there), range 0-45. Depth: measured 18337 of 18337, median
5.0, rows `>=10` 1066, share 0.0581 on either denominator. KBD measured 17770 of 18337 (0.969).
Pipe coverage (`Труба`): 3782 distinct pipes (range 13-14213), zero missing.
Character: `Коррозия CORR` 17770, `Металл снаружи TMTM` 229, `Заводской дефект MIAN` 132,
`Технологический дефект TECH` 67, `Вмятина DENT` 55, rest small. No SSID column exists.

## File 8: PK2 2015 pipe log (`Парабель-Кузбасс-2 (0-110)/2015/Трубный журнал 2015.xls`, 2701824 B)

Stock xlrd opens it. Sheet `Трубный журнал` is 14244 x 18: row 0 is a year label (`2015`),
header row index 1 (`Труба`, `Тип трубы`, `Начало трубы, м`, `Длина трубы, м`,
`Окончание трубы, м`, `Продольный шов(1)`, `Продольный шов(2)`, `Толщина трубы, мм`,
`Категория участка`, plus 9 unnamed columns). Data rows: 14242. Pipe end reaches 112316.25 m.
Types: прямошовная 11914, спиральношовная 2328.
Sheet `для гришина` is 4984 x 9 with header row index 0 and the same 9 named columns.
Data rows: 4983. Pipe end reaches 35893.31 m. No depth column exists in either sheet.

## File 9: PK2 2020 anomalies (`Парабель-Кузбасс-2 (0-110)/2020/Аномалии.xlsx`, 295801 B)

ZIP CRCs pass. Sheets: `Общая информация`, `Применяемые стандарты`, `Аномалии`
(dimension max row 1030, 44 columns). Header row index 3. Columns: 44. Data rows: 1026.
Distance: all parsed, min 787.88 m, max 110680.136 m (0.8-110.7 km).
Depth: measured 814 of 1026 (0.793), median 11.0, rows `>=10` 782, share 0.762 all-rows
and 0.961 measured-only. Pipe coverage: 623 distinct pipes, zero missing.
GWAN: 91 rows, share 0.089.

## File 10: PK2 2020 welds (`Парабель-Кузбасс-2 (0-110)/2020/Поперечные сварные швы.xls`, 2967040 B)

Stock xlrd opens it. Weld sheet 12391 physical rows. Header row index 3. Columns: 21.
Data rows: 12387. Distance: all parsed, min 18.44 m, max 113027.095 m. Pipes: 12387 distinct,
one per row. No depth column.

## File 11: PK2 2025 anomalies (`Парабель-Кузбасс-2 (0-110)/2025/аномалии.xlsx`, 1162273 B)

ZIP CRCs fail on `sharedStrings.xml` and `sheet1.xml`; strict parsers fail. Byte-salvage
(raw deflate, regex row parse, shared-string resolution) recovers a 46-column new-format table.
Row 1 holds header-name indices 0-45 into the (partly readable, 23555-entry) string table,
which yields the full header map (`SSID`, `Расстояние, м`, offsets, `Номер трубы`,
`Характер особенности`, `Характер аббр.`, `Значение глубины`, `Единица измерения`, ...,
pressures). Data rows: 2161 (file rows 2-2162, no gaps; 2162 row slots including the header).
Distance (column B, index-encoded): 2155 parsed, min 10.0 m, max 70553.015 m, so coverage is
partial (0.01-70.6 km of the 113 km section). Depth (column AF) mixes units (`мм` 1600,
`% от t` 438, `% от t эквив.` 33, `INT` 8, `EXT` 65): numeric depths 2160, median 3.04,
rows `>=10` 547, share 0.253 of data rows. Depth `>=10` shares are not comparable across units.
Character: Аномалия кольцевого шва 1682 (GWAN share 0.778), Коррозия 406, Аномалия
продольного шва 21, Технологический дефект 18, Механическое повреждение 17, rest small.
Pipes: 1250 distinct.

## File 12: PK2 2025 pipe elements (`Парабель-Кузбасс-2 (0-110)/2025/трубные_элементы.csv`, 2721545 B)

UTF-8 decode fails at byte 149512: one bad byte inside a `Неизвест...` cell. cp1251 decodes
but leaves headers as mojibake, so it is the wrong read despite decoding without error.
UTF-8 with errors=replace reads clean Russian headers. Rows: 12420. Columns: 30 (SSID,
`Номер трубы`, `Расстояние, м`, pipe traits, pressures, empty lat/lon/alt). Pipes: 12420
distinct, one per row. Distance: all parsed, min 18.44 m, max 113027.745 m.

## Verdicts on repo numbers touching these folders

PK1-2022 10739 data rows: CONFIRMED (10743 physical minus 4 header rows; all 10739 carry distance).
PK1-2025 21763 data rows: CONFIRMED (21767 physical minus 4 header rows).
E11 counts 8982 vs 8989: CONFIRMED by exact independent recompute (E11 dist-drop applied:
2022 10739 with dist and 8982 at depth `>=10`; 2025 21638 with dist and 8989 at depth `>=10`).
E11 match 0.715: CONFIRMED by recompute (0.71476, rounds to 0.715; full output bit-identical to
`results_e11.json`: n_pos 562, n_cells 1401, B1 AP 0.77947, base 0.40114, lift CI [0.348, 0.409],
29 s runtime). E12 cut numbers (0.574/0.375) were not recomputed; the stored E12 match 0.71504
is consistent with the same pipeline at cut `>=12`.
PK2-2015 18337 rows, median 5.0, share 0.058: CONFIRMED (1066/18337 = 0.0581; same on either
denominator since all depths are measured).
PK2-2020 1026 rows: CONFIRMED (1030 physical rows minus 4 header rows).
PK2-2025 salvage 2162 rows: CONFIRMED with note (2162 row slots rows 1-2162; row 1 is the header,
so 2161 data rows; 2155 with distance, 2160 with numeric depth).
PK2-2025 csv 12420 pipes: CONFIRMED (12420 rows, 12420 distinct pipes; correct read is
UTF-8/errors=replace, not cp1251).
PK1-2019 2859 clean rows km 0-45 plus absent tail: CONFIRMED exactly (2859 data rows, distance
0.07-44.97 km; max row number 2863; rows 2864+ absent, never written).
GWAN ON era numbers (128/590/1506): UNVERIFIABLE here (out of scope; ON folders were not read).
README PK1 pair row (0.779/0.574/0.375, 562 positives): 0.779 and 562 CONFIRMED by recompute;
0.574/0.375 stand as reported (E12 files present, not recomputed).
README PK2 row (5.8% of 18337 in 2015 vs 96% of measured depths in 2020): CONFIRMED
(0.0581 and 782/814 = 0.9606).
README/DATA PK2 drift (164 to 9 to 55 per km): 164 and 9 CONFIRMED as total rows per km
(18337/113 = 162.3, 163.7 at 112 km; 1026/113 = 9.1). 55 CORRECTED to 19.1 (2161/113 km);
no denominator (113, 112, 110 km, covered span 70.6 km, depth `>=10` rows) reproduces 55.
DATA.md PK1-2025 GWAN 50%: CONFIRMED (10933/21763 = 0.502). DATA.md PK2-2025 GWAN 78%:
CONFIRMED (1682/2161 = 0.778). The parenthetical edge-offset x10057 is close but not exact:
10428 rows sit at zero distance to the girth weld.
PROGRESS PK2-2020 medians (11.0, 96.1% measured, 76.2% of rows): CONFIRMED.
PROGRESS PK1-2025A 99.4% tolerant recovery: CONFIRMED (21638/21763 = 0.9943 rows with distance).
results_e15.json PK strict_rows: match physical counts (10743, 14097, 21767, 18338, 14244/4984,
12391, DEAD weld) except PK2-2020 anomalies (1028 vs 1030 physical rows; data rows agree at 1026)
and PK1-2019 sheet1 (14 vs 18 row tags rows 2-23); data-row claims are unaffected.
results_e15.md PK corrections: upheld (PK2-2025A recoverable with 2161 data rows; csv is an
encoding flag with the UTF-8/replace correction above; PK1-2025 weld DEAD under both engines;
PK1-2019 tail absent, not garbled).
