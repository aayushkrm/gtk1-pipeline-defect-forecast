# DATASET_NPK: the authoritative October 2026 archive

This card describes the dataset in `Датасет НПК.rar` only. The old six-section card
(`docs/DATASET.md`) describes a different object and stays frozen as history. Do not pool
rows, thresholds, or metrics across the two objects.

## Source and integrity

| Item | Value |
|---|---|
| Chat | «Газопровод. Предсказание дефектов» |
| Message | `12704`, posted 21.10.2026 17:50 |
| Document id | `5386680895254080196` |
| Archive | `Датасет НПК.rar` |
| Bytes | 73,762,132 |
| SHA-256 | `330ce420e9e75fff720705ebb7c4bf8773824ca691f7ce0ed281490299032933` |
| Extraction | `unar` → 37 files in 18 section folders |
| Openability | 37/37 files open in the repo readers; 0 fails (`experiments/results_openable_npk.json`) |

The archive is not on the partner Yandex Disk. The partner deleted the Tuesday archive and
named this file as the only authoritative source. The file is stored outside git.

## Year grid

| Year | Trunk sections (rows) | Branch sections (rows) | Files |
|---|---|---|---:|
| 2016 | 406–572 (66) | 0–94, 720 mm (1,900) | 2 |
| 2017 | 111.2–242 (1,440); 242–404 (423) | — | 2 |
| 2018 | — | 0–14, 530 mm (585) | 1 |
| 2019 | 0–110 (412) | 0–36.6, 325 mm (379); 0–71, 530 mm (70); 14–22, 426 mm (2,002) | 4 |
| 2020 | 0–110 (1,026); 242–404 (1,233) | 0–10, 530 mm (1,082) | 3 |
| 2021 | — | — | 0 |
| 2022 | 572–714 (10,739) | 0–3.8, 273 mm (143); 0–21.7, 720 mm (1,734); 3.8–5.4, 426 mm (78) | 4 |
| 2023 | — | — | 0 |
| 2024 | — | 0–91, 720 mm (8,808) | 1 |
| 2025 | 572–714 (21,763) | — | 1 |
| **Total** | | | **18** |

2021 and 2023 are absent for every section, as the partner stated. The archive holds
53,883 anomaly rows in total.

## Sections

Survey start is the first tool launch date from the «Общая информация» sheet. `d≥10` is
the count of rows with depth at or above 10%. `Pipes` is the count of distinct `Номер
трубы` values. `Dup dist` is the count of rows that share a distance with another row in
the same file.

| Year | Folder | Pipeline / section | Diameter | km | Survey start | Rows | d≥10 | Pipes | Dup dist |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2016 | Основная труба (406-572 км) | 404 - 572 км | 1020 mm (40") | 406–572 | 20.10.2016 | 66 | 21 | 53 | 7 |
| 2016 | Отвод основной трубы (0 - 94 км) | ГАЗОПРОВОД-ОТВОД К ГРС-4 Г.ТОМСКА / 0 - 91 км | 720 mm (28") | 0–94 | 15.06.2016 | 1,900 | 1,431 | 961 | 9 |
| 2017 | Основная труба (111,2-242 км) | ПП Чажемтовская - ПП Володинская | 1020 mm (40") | 111.2–242 | 19.06.2017 | 1,440 | 1,190 | 775 | 6 |
| 2017 | Основная труба (242-404 км) | ПАРАБЕЛЬ - КУЗБАСС - 2 / ПП Володинская - КС Проскоково | 1020 mm (40") | 242–404 | 04.07.2017 | 423 | 228 | 280 | 17 |
| 2018 | Отвод (0-14 км) | ГАЗОПРОВОД-ОТВОД К ГРС-1 Г.КЕМЕРОВО / 0 - 14 км | 530 mm (21") | 0–14 | 25.10.2018 | 585 | 432 | 247 | 0 |
| 2019 | Основная труба (0-110 км) | 0 - 110 км | 1020 mm (40") | 0–110 | 11.06.2019 | 412 | 313 | 267 | 7 |
| 2019 | Отвод (0-36км) | 0 - 36,6 км | 325 mm (13") | 0–36 | 30.07.2019 | 379 | 213 | 255 | 0 |
| 2019 | Отвод (0-71 км) | 0 - 71 км | 530 mm (21") | 0–71 | 20.05.2019 | 70 | 15 | 48 | 8 |
| 2019 | Отвод (14-22 км) | 22 - 14 км | 426 mm (17") | 14–22 | 07.10.2019 | 2,002 | 1,961 | 337 | 8 |
| 2020 | Основная труба (0-110 км) | — | 1020 mm (40") | 0–110 | 16.06.2020 | 1,026 | 782 | 623 | 17 |
| 2020 | Основная труба (242-404 км) | — | 1020 mm (40") | 242–404 | 02.07.2020 | 1,233 | 891 | 716 | 41 |
| 2020 | Отвод (0-10 км) | 0-10 км, 0-5 км | 530 mm (21") | 0–10 | 22.09.2020 | 1,082 | 252 | 481 | 11 |
| 2022 | Основная труба (572-714 км) | 572 - 714 км | 1020 mm (40") | 572–714 | 21.03.2022 | 10,739 | 8,982 | 4,201 | 961 |
| 2022 | Отвод (0 - 3,8 км) | 0 - 3,8 км | 273 mm (11") | 0–3.8 | 31.10.2022 | 143 | 19 | 92 | 24 |
| 2022 | Отвод (0-21,7 км) | 0 - 21,7 км | 720 mm (28") | 0–21.7 | 27.09.2022 | 1,734 | 1,231 | 804 | 175 |
| 2022 | Отвод (3,8 - 5,4) | 4,2 - 5,4 км | 426 mm (17") | 3.8–5.4 | 26.08.2022 | 78 | 33 | 49 | 10 |
| 2024 | Отвод (0 - 91 км) | 0 - 91 км | 720 mm (28") | 0–91 | 05.06.2024 | 8,808 | 6,597 | 3,627 | 1,675 |
| 2025 | Основная труба (572-714) | 572 - 714 км | 1020 mm (40") | 572–714 | 11.03.2025 | 21,763 | 9,061 | 7,161 | 5,748 |

The 2016 branch sheet carries `Дата создания файла = 30.01.2023`. That date is a file
creation stamp, not a survey date. The tool table starts on 15.06.2016. The 2017
242–404 file names `ПАРАБЕЛЬ - КУЗБАСС - 2`; the 572–714 section matches the old PK1 card.

Three folder/sheet disagreements stay on record: the 2016 main folder says 406–572 but the
sheet says `404 - 572 км`; the 2019 14–22 km sheet says `22 - 14 км`; the 2022 3.8–5.4
folder says 3.8–5.4 but the sheet says `4,2 - 5,4 км`. Use the sheet value for joins and
keep the folder name for the file path.

Folder names are NFC-normalized in the tidy table. The 2016 branch folder is NFD on disk
(`й` = `и` + U+0306); the ingest normalizes it.

## Column schema

The anomaly sheet has 44 or 45 columns. The ingest maps these names:

| Tidy name | Source column |
|---|---|
| `dist` | `Расстояние, м` |
| `pipe_no` | `Номер трубы` |
| `pipe_len` | `Длина трубы, м` |
| `off` | `От левого шва до начала, м` |
| `off_mm` | `От продольного шва до центра, мм` |
| `h` | `Ориентация максимума, ч:мин`; fallback `Ориентация центра, ч:мин` |
| `depth_pct` | `Глубина, %` |
| `length_mm` | `Длина, мм` |
| `width_mm` | `Ширина, мм` |
| `wall_mm` | `Толщина, мм` |
| `char` | `Характер особенности` |
| `kind` | `Тип особенности` |
| `size_class` | `Класс размера` |
| `desc` | `Описание` |
| `danger` | `Опасность` |
| `kb` | `КБД` |
| `no_years` | `Срок НО, лет` |
| `pf` | `Pf, МПа` |
| `ssid` | `SSID` (present in some files; see Data quality) |

`off` is the weld-relative offset used by the frozen matcher. `h` is decimal hours; empty
becomes `-1`.

## Data quality

- Depth maximum is 85.0%. No row exceeds 100%. No mm-contaminated depth rows are present.
  The old archive had 1,600 such rows; this archive does not.
- Depth is missing on 15,161 of 53,883 rows (28.1%). Most missing rows are weld or other
  non-corrosion anomalies. In 2025, 10,655 of 10,984 ring-weld rows have no depth; in
  2022, 302 of 2,580 do. The d≥10 totals still balance (8,982 vs 9,061 raw; 8,782 vs
  8,791 after the frozen frame pipe filter), so the R3 ratio passes, but the composition
  differs by anomaly type.
- Orientation is missing on 49,652 of 53,883 rows (92.2%). The matcher treats missing
  orientation as `-99` (unknown), so it does not block a match.
- `Номер трубы` is a sequential pipe index along the section. A pipe spans at most about
  12 m. The index is stable in 2022→2025 (96.2% of 2022 pipes appear in 2025) and in
  2016→2024 (85.2%). It is not stable in 2017→2020 (8.9%) or 2019→2020 (3.4%). This is
  the join gate for those pairs.
- 8,724 rows share a distance with another row in the same file. These are multiple
  anomalies on one pipe or joint, not duplicate records.
- `SSID` is non-empty on 15,298 rows (28.4%). It is present in the 2016 main file, all
  2019 and 2020 files, the 2022 0–3.8 and 3.8–5.4 files, and the 2024 branch. It is
  absent from the 2016 branch, 2017, 2018, 2022 main, 2022 0–21.7, and 2025 files. The
  frozen matcher does not use it.
- `Опасность`: `(c)` 51,732, `(b)` 1,672, `(a)` 431. The ABC label is a present label,
  not a prediction.
- `Характер особенности` top values: Коррозия 27,540 (51.1%), Аномалия кольцевого шва
  18,583, Вмятина 2,403, Механическое повреждение 2,004, Технологический дефект 1,362,
  Заводской дефект 759.

## Join gate

The frozen matcher requires the same pipe number in both surveys. The table shows how many
past pipes survive into the future file.

| Pair | Past pipes | Future pipes | Past pipes in future | Match rate | Verdict |
|---|---:|---:|---:|---:|---|
| 2022→2025, 572–714 | 4,201 | 7,161 | 4,042 (96.2%) | 0.725 | join OK |
| 2016→2024, 720 mm branch | 961 | 3,627 | 819 (85.2%) | 0.170 | join OK, R3 fail |
| 2017→2020, 242–404 | 280 | 716 | 25 (8.9%) | 0.000 | join fail |
| 2019→2020, 0–110 | 267 | 623 | 9 (3.4%) | 0.000 | join fail |
| 2022→2024, 720 mm branch | 804 | 3,627 | 391 (48.6%) | 0.000 | join fail |

The 2022→2024 branch pair also changes extent: the past file covers 0–21.7 km, the future
file covers 0–91 km. Do not read it as a same-section pair.

## Pair inventory (frozen R1, cut ≥10%)

| Pair | Tier | Frame rows ≥10 past/future | Match | Ratio | AP | Base | Lift 95% CI | P@20 | P@50 | R3 | R4 | Verdict |
|---|---|---|---:|---:|---:|---:|---|---:|---:|---|---|---|
| `main572_2022_2025` | primary | 8,782/8,791 | 0.725 | 1.001 | 0.7778 | 0.3960 | +0.3517…+0.4109 | 20/20 | 48/50 | pass | pass | **clean** |
| `branch720_2016_2024` | primary | 1,431/6,542 | 0.170 | 4.572 | 0.6930 | 0.4978 | +0.1629…+0.2304 | 18/20 | 46/50 | fail | pass | suggestive only |
| `branch720_2022_2024` | sensitivity | 1,231/6,542 | 0.000 | 5.314 | 0.5705 | 0.5458 | +0.0077…+0.0472 | 13/20 | 34/50 | fail | pass | void |
| `main242_2017_2020` | primary | 221/891 | 0.000 | 4.032 | 0.1216 | 0.1218 | −0.0014…+0.0085 | 3/20 | 7/50 | fail | fail | void |
| `main110_2019_2020` | primary | 311/782 | 0.000 | 2.514 | 0.1352 | 0.1319 | −0.0024…+0.0200 | 2/20 | 9/50 | fail | fail | void |

Frame rows are the rows that survive the frozen `frame()` pipe filter and finite-distance
drop. The raw `d≥10` counts in the section table are 8,982/9,061 for the clean pair; the
frame keeps 8,782/8,791, so the density ratio is 1.001.

Only `main572_2022_2025` passes R1–R4. The branch pair is kept as suggestive evidence:
its lift is positive, but R3 fails because the future survey is 4.57× denser and the match
rate is below 0.20. The 2017→2020 and 2019→2020 pairs fail the join gate and have no lift.
The 2022→2024 branch pair fails the join gate and changes extent.

## Exclusions

- 2021 and 2023 are absent for every section. Do not interpolate them.
- `Выявленные особенности.xls` (2016 branch) is out of use by partner instruction. It is
  not ingested.
- `Аномалии_стар.xlsx` (2022, 0–3.8 km) is the only anomaly file in that folder. It is
  legacy-named and excluded from pairs. The 2022 0–21.7 km file covers the same ground and
  is the file used for the branch pair.
- The 2022 0–3.8 km and 3.8–5.4 km sub-files overlap the 0–21.7 km file. Do not sum them.
- The 2018 0–14 km, 2019 0–36.6/0–71/14–22 km, and 2020 0–10 km branches have no future
  survey in the archive. They are inventory only.
- PK2 sections (0–110, 111.2–242, 242–404, 406–572) have no clean pair. The 2017→2020 and
  2019→2020 pairs fail the join gate. PK2 stays deferred.
- Old-object rows are never pooled with this archive.

## Rebuild commands

```bash
python3 experiments/check_openable.py --root "/Users/akm/Tsu Project/Датасет НПК" --tag npk
python3 experiments/inventory_npk.py --root "/Users/akm/Tsu Project/Датасет НПК" --tag npk
python3 experiments/ingest_npk.py
python3 experiments/npk_pairs.py
python3 experiments/npk_sensitivity.py
```

`outputs/npk/anomalies.csv` is the tidy 53,883-row table. It is git-ignored. The committed
artifacts are `experiments/results_openable_npk.json`,
`experiments/results_inventory_npk.json` (structure only; previews stay in
`outputs/npk/inventory_preview_npk.json`), `experiments/results_npk_audit.json`,
`experiments/results_npk_pairs.json`, and `experiments/results_npk_sensitivity.json`.

## Disclaimer

> "New = unmatched future ≥10% row under pipe+2m/0.5m/1h match; includes re-detection.
> Absolute AP is cut- and survey-conditional."

For the clean pair: match-rate 0.725, vanished-frac (non-match share) 0.275. Cut
sensitivity: ≥10% AP 0.7778, P@20 20/20; ≥12% AP 0.5710, P@20 17/20; ≥15% AP 0.3551,
P@20 12/20. The vanished-frac here is the share of past ≥10% rows with no future ≥10%
match under the frozen greedy past→future matcher. It is not the E08 reverse-greedy
corr-only audit.
