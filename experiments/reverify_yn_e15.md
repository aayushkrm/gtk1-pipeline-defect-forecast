# YN E15 validation: salvage parse and schema verdict

Date: 2026-10-07. Sources read-only. No matching ran. No training ran.

## Method

Stock zip reads fail on CRC for all three target sheets. I extracted each
sheet stream raw (local file header parse, CRC ignored) and inflated it with
tolerant zlib. All three streams inflate to the end. The damage sits inside
the XML: smashed tags, duplicated row fragments, repeated string-index
values. Shared strings read intact through the stock path.

I split each stream on `</row>` and kept the text after the last `<row r="N"`.
Tiers: A = one valid open, numbered, cells parse; B = valid open but repeated
row number; C = close with destroyed open tag (row un-numbered, cells
smashed); D = several opens in one chunk (duplication runs). Only tier A
forms records. Tiers C and D are counted, not parsed. Cells with `t="s"`
resolve through shared strings. A numeric cell that holds a non-integer
string index is flagged as a garbage cell.

## Recovery counts

| Sheet | Prior well-formed | Tier A rows | Tier B (dup r) | Tier C mangled | Tier D chunks |
|---|---|---|---|---|---|
| 2020 sheet3 anomalies | 2,624 | 2,623 | 0 | 1 | 1 |
| 2023 sheet3 features | 29,234 | 21,037 | 290 numbers / 794 rows | 8,193 | 5 |
| 2023 sheet4 anomalies | 4,405 | 4,401 | 2 numbers / 5 rows | 3 | 2 |

The prior counts counted `</row>` closings. That overcounts sheet3 of 2023:
8,193 closings pair with destroyed opens, and 483 duplicated rows carry
different content under the same row number (0 identical). Usable tier-A
data rows: 2020 = 2,621 (rows 5-2625); features = 21,015 (rows 2-36887,
sparse); anomalies = 4,400 (rows 2-4398, contiguous).

## 2020 anomalies (45-col SSID format, header row 4)

Distance: 2,621/2,621 numeric, monotonic with 0 violations, span
20.82-37,215.645 m. The workbook filter claims A4:AS18069 (18,065 data
rows). Rows 2626-18069 are absent. Recovery covers 0-37.2 km of 151 km
(14.5% of expected rows).

Pipe No: 2,620/2,621 numeric, values 10-3681, monotonic. The last row (2625)
is tail-garbled and holds 2 garbage cells, including a destroyed pipe value.
All 2,620 checkable rows fall within 12 m of the same pipe in the 2020 weld
log (median 2.88 m). The 2020 weld log reads clean: 14,098 rows, pipes
1-14094, span 0-151,492.155 m.

Depth: 1,464/2,621 numeric (55.9%), range 0.1-76.0%. The 1,156 non-numeric
cells are not shifts. They hold wall-position codes: EXT 668, INT 486,
MID 2. Weld-anomaly classes store position in the depth column and state the
metal-loss equivalent in free-text comments (example: comment "metal loss
equivalent 11%" with depth cell EXT). Depth >= 10% of measured = 675/1,464
(46.1%). Corrosion median is 9.0%.

Character: 10 classes. Corrosion 839, weld-seam anomalies 1,008, plant
defects 352, dents 189, mechanical damage 128, technological defects 98,
crack zones 4, corrugation 2, other 1. Clocks (in/out seam, start/max/
center) are 100% filled. KBD and danger columns are filled on 843/2,621
rows (32.2%). Marker columns are empty (0/2,621).

## 2023 features journal (18-col, header row 1)

Usable tier-A data: 21,015 rows. Columns hold N pipe, odometer distance,
wall h, weld-offset pair, marker offsets, type, character, size class,
orientation, length, width, d%, d mm, position type, KBD, rating, note.

Numeric columns carry contamination. Depth d%: measured 11,616/21,015;
6,949 within (0,100] (59.8% of measured, 33.1% of rows); 4,667 above
10,000, up to 137,609. Pipe: 11,963/21,015 numeric, 7,053 empty; 110 rows
hold the placeholder 60462 in pipe or distance (a shared-string index
leaking as a literal, seen repeated as `<v>60462</v>` in garble runs).
Distance: 12,108/21,015 numeric, 8,272 empty. Sane-distance span is
0-47,515.603 m (12,057 rows).

Type mixes pipe records with anomaly records in one journal: empty 8,960,
anomaly 7,293, ring weld 4,635, plus metal patches, markers, tees, ballasts,
taps. All 6,949 sane-depth rows sit inside the 7,293 anomaly-type rows.
Orientation is filled on 11,979/21,015 rows (57.0%).

The offset column is text pairs ("0.00 / -11.63"), never a single number,
and empty on 13,680/21,015 rows (65.1%). KBD mixes numbers with the rating
letter C. Rating mixes letters with garbage cells. Duplicated row numbers
(290 numbers, 794 rows; 289 numbers and 772 rows inside data) hold
differing content in all 483 repeated data rows (0 identical). These rows
are quarantined.

## 2023 anomalies journal (20-col, header row 1)

Usable tier-A data: 4,400 rows, contiguous rows 2-4398. Same 18 columns as
features plus allowed pressure, service life, and rank. Distance:
4,397/4,400 numeric, monotonic with 1 violation, span 3.45-25,655.079 m.
Pipe: 4,395/4,400 numeric, values 5-2647. All 4,395 checkable rows fall
within 12 m of the same pipe in the 2023 pipe log.

Depth d%: measured 4,266/4,400 (97.0%); 3,084 within (0,100] (72.3% of
measured); 930 above 10,000, up to 72,259. Orientation is filled on
4,395/4,400 rows. The offset column uses the same text-pair format, empty
on 1,184/4,400 rows (26.9%). Character mixes 1,181 pipe-type rows
("pipe 1S") into anomaly records. Size class uses PITT/GENE/CIGR/AXGR codes.

Rows past 4398 are destroyed: 2 duplication chunks hold 1,268 repeated row
opens across advertised rows 4399-29603.

## Column mappability

Pipe No maps. 2020 anomaly pipes match the 2020 weld log 2,620/2,620
within 12 m. 2023 anomaly pipes match the 2023 pipe log 4,395/4,395
within 12 m. Cross-survey numbering holds: 13,420 common pipe numbers
between the 2020 weld log and the 2023 pipe log agree at median 4.23 m
(max 30.8 m). 2020 anomaly pipes match 2023 pipe-log positions 2,563/2,563
within 12 m.

Distance maps. Numeric and monotonic on both sides over the shared span.

Depth does not map cleanly. Three breaks: 2020 stores position codes
(EXT/INT) in the depth column for weld classes with the loss equivalent in
comment text; 2023 stores up to 40% out-of-range values in the same column;
2023 reports nothing below 1.9% while 2020 reports from 0.1%.

Character maps with a code table. 2020 uses 10 Russian classes; 2023 uses
character plus PITT/GENE/CIGR size codes, and both 2023 journals mix pipe
rows into anomaly records. A mapping needs pipe-row exclusion first.

Offsets do not map. 2020 holds four numeric weld-offset columns at 100%
fill. 2023 holds one text-pair column at 35-73% fill. Orientations map in
form (clock strings both sides) at unequal fill (100% vs 57-100%).

## Threshold comparability

Depth >= 10% selects different populations per side. In 2020 it keeps
675/1,464 measured rows (46.1%) and drops all weld-class rows by
construction (position codes are unmeasurable). In 2023 it keeps 6,949
sane-depth feature rows and 3,084 sane-depth anomaly rows, but only after
a (0,100] sanity gate that the frozen pipeline does not define. The sane
medians sit close (2020 corrosion 9.0; 2023 features 12.0; 2023 anomalies
10.0), yet the reporting floors differ (0.1 vs 1.9) and the contamination
is one-sided. Cut sensitivity would confound method drift with growth.

## Verdict: PAIR-BLOCKED

R1. 2023 depth columns are contaminated on 27.7% (anomalies) and 40.2%
(features) of measured cells, plus placeholder 60462 leaks and code-letter
leaks. The quarantine is non-random and not repairable inside the files.
R2. Threshold regimes differ across surveys: reporting floor 0.1 vs 1.9,
position codes vs numbers for weld classes, sane-only-after-gating on one
side. The frozen Depth >= 10% filter cannot select comparable populations.
R3. The frozen offset term (+-0.5 m) has no defined 2023 input: text pairs,
not numbers, with 26.9-65.1% empty.
R4. Both sides end at corruption edges, not survey edges: 2020 keeps
0-37.2 km of 151 km; 2023 anomalies keep 0-25.7 km; 2023 features keep a
sparse 0-47.5 km with 8,193 destroyed chunks. Overlap exists but neither
side represents its survey.
R5. Character coding mixes pipe rows into anomaly records on the 2023 side
(1,181 in the anomalies journal), so class-filtered matching needs new
exclusion rules the frozen pipeline does not hold.

What unlocks the pair: a clean re-export of the 2023 journals over 0-154 km
and of the 2020 anomalies tail (rows 2626-18069). Pipe numbering already
joins across surveys (median 4.23 m), so no new method work is needed once
clean files land. The re-export request stands.

## Artifacts (outputs/, gitignored)

yn2020_anom_salvaged.csv (2,621 rows, 45 cols plus _row and _garbage_cells).
yn2023_feat_salvaged.csv (21,015 rows, 18 cols plus flags).
yn2023_anom_salvaged.csv (4,400 rows, 20 cols plus flags).
yn_e15_summary.json, yn_e15_phase3.json, yn_e15_phase4.json (counts in this
report derive from these files). Scripts: experiments/salvage_yn_e15.py,
experiments/validate_yn_e15.py, experiments/validate_yn_e15b.py,
experiments/validate_yn_e15c.py. Sources untouched. No commits made.
