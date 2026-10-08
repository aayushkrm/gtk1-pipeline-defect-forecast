# DATA: schemas, keys, QC (from read-only study of 32 files)

## Sections
ON covers 392–526 (D1220, 132km). It holds 2016/21/25.
Y-N covers 0–154 (D720, 151km). It holds 2020/23-new-format.
PK1 covers 572–714 (D1020 spiral, 140km). It holds 2019/22/25.
PK2 covers 0–110 (D1020, 113km). It holds 2015-23col/2020/25+csv.
SRTO covers 1608–1717 (D1220, 104km). It holds 2016/21/24.
SRTO covers 1717–1759 (D1220, 42km). It holds 2016-8sheet/21/24.

## Schemas
- Anomaly tables use 44/45 cols with R4 header (R2/R1 in damaged/new). They contain [SSID] + Distance + weld offsets + long-seam offsets + Pipe No + length + pipe Type + clocks + markers + feature/character/size/desc + abbrs + orientations + thickness/length/width/depth + location + comments + lat/lon/alt (empty) + Danger/KBD/Pd/MAOP/Psw/Pf/Service. Tail order flips 2016 vs 2021+.
- Pipe tables use 20→30 cols. They contain Pipe No + Distance + length + type + thickness + clocks + count + SMYS/Sy + SMTS/Su + category + factors + k1 + insulation + weld + [SSID/steel/temp/paspport kn,n,m,KCV,Pmaor].
- Special cases need separate handling. 2015 uses 23-col (No-in-TA, comma decimals, no SSID/passport). otchet-2023 uses 11 sheets (anomaly journal 20 + features 18 + pipe log 10, pipe rows mixed in). KP-2016 uses 42-col mixed.

## Keys
Pipe No covers 100%. ON16↔21 overlaps 11788/11858. Δ shows 0.000m. Type matches at 99.6%. Use weld log as primary join.
Odometer stays stable (~100m/132km). NN matches ±2m at 72.6% (25→21) and 53.4% (21→16) on raw
frames, pipe-agnostic (recomputed exact: 0.7263/0.5338; d10-filtered equivalents run 81.0/69.8, so
filtering inflates apparent persistence). Markers, offsets, and orientation stay stable.
SSID does not persist. Lat/Lon reads 0%. Depth covers 66–100% in typical clean files (SRTO-side
lows reach 12%). KBD covers 58–86% typically (SRTO-side lows reach 5%). Service in 2016 uses 100y fictive.

## Tool generations (supervisor list, 2026-10-07 — explains sensitivity jumps between surveys)
Calipers and geometry: СО-1200, ПМО-1200Б, ПМОБ-1200, ПРТН-1200-256. Metal loss: ДМТ-2-1200Б-2560,
ДМТ2Б-1200-2560, ДМТ2Б-1200-1024 (2560/1024 = sensor counts; higher counts resolve smaller defects).
Combined: ДМТП2Б-1200-768, ДМТП2Б-1200-1408, ДМТП-2-1200Б-768. Newer generations and denser sensor
arrays report more rows for the same pipe. Always record tool per survey before comparing counts
across years; a count jump after a tool upgrade is sensitivity, not growth, until matched-pair
analysis says otherwise.

## QC (must handle in ETL)
Treat these files as salvage-only: YN-20A (2,621 usable rows), PK1-19A/T (2,859 pristine rows,
tail absent), PK2-25A (2,162 rows recovered), otchet-23 (journals partial). SRTO-1717-24A reads fully
under strict parse (only its dimension tag is broken; sharedStrings CRC fails but sheets are clean —
see re-salvage, bit-identical re-derivation). PK1-25T weld log recovered via FAT-chain olefix
(12,927×28, 12,475 pipes to 128.8km; method in experiments/salvage_pk1_weld.py, CSV in outputs/).
They show bad CRC/XML, shifts, and `3.3e-307` garbage.
Treat these files as truncated: ON25-T weld log spans to 27,216.7 m (27.2 km, 3,471 rows,
committed distance-max read). PK1-25T loses −65KB. Empty tails drop.
Map renames by meaning: ARTD→GOUG (mech), TECH→ARTD (tech). Track Danger position. Map SMYS→Sy. Map Depth%→value+unit.
Fix units before use. Long-seam col labels m but holds mm values. Parse comma decimals in 2015 + markers and h:min strings. Split on `Pipe 1W` separators.
Check content skew. PK2-25 shows GWAN 78%. PK1-25 shows GWAN 50% (edge-offset ×10428, campaign?). SRTO-1717-24 shows Danger 82% empty.

## Normalization (mandatory)
Apply Depth≥10% and unified class map. Add year/contractor/standard covariate.
Match on same pipe + distance ±2m + offset ±0.5m + orient ±1h. Flag the rest as new/vanished with uncertainty flag.
Use ON 2016→2021→2025 as reference pair. Request 5 re-exports, pipe ages, and per-survey thresholds.
