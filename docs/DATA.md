# DATA — schemas, keys, QC (from read-only study of 32 files)

## Sections
ON 392–526 (D1220, 132km): 2016/21/25. Y-N 0–154 (D720, 151km): 2020/23-new-format.
PK1 572–714 (D1020 spiral, 140km): 2019/22/25. PK2 0–110 (D1020, 113km): 2015-23col/2020/25+csv.
SRTO 1608–1717 (D1220, 104km): 2016/21/24. SRTO 1717–1759 (D1220, 42km): 2016-8sheet/21/24.

## Schemas
- Anomalies 44/45 cols, R4 header (R2/R1 in damaged/new): [SSID] + Distance + weld offsets +
  long-seam offsets + Pipe No + length + pipe Type + clocks + markers + feature/character/size/desc +
  abbrs + orientations + thickness/length/width/depth + location + comments + lat/lon/alt (empty) +
  Danger/KBD/Pd/MAOP/Psw/Pf/Service (tail order flips 2016 vs 2021+).
- Pipes 20→30 cols: Pipe No + Distance + length + type + thickness + clocks + count + SMYS/Sy +
  SMTS/Su + category + factors + k1 + insulation + weld + [SSID/steel/temp/paspport kn,n,m,KCV,Pmaor].
- Special: 2015 23-col (No-in-TA, comma decimals, no SSID/passport); otchet-2023 11 sheets
  (anomaly journal 20 + features 18 + pipe log 10, pipe rows mixed in); KP-2016 42-col mixed.

## Keys
Pipe No 100%, 11788/11858 overlap ON16↔21, Δ0.000m, type 99.6% → primary join via weld log.
Odometer stable (~100m/132km); NN ±2m 72.6% (25→21), 53.4% (21→16). Markers/offsets/orientation stable.
SSID not persistent. Lat/Lon 0%. Depth 66–100%, KBD 58–86%, Service 2016=100y fictive.

## QC (must handle in ETL)
Corrupt: YN-20A, PK1-19A/T, PK2-25A, SRTO-1717-24A, otchet-23, PK1-25T (bad CRC/XML, salvage only,
shifts, `3.3e-307` garbage). Truncated: ON25-T 27km vs 132km anomalies; PK1-25T −65KB; tails of empties.
Renames: ARTD→GOUG (mech), TECH→ARTD (tech) — map by meaning; Danger position; SMYS→Sy; Depth%→value+unit.
Units: m vs mm typo (long-seam col labelled m, values mm); comma decimals 2015 + markers; h:min strings;
`Pipe 1W` separators. Content: PK2-25 GWAN 78%, PK1-25 GWAN 50% (edge-offset ×10057 — campaign?),
SRTO-1717-24 Danger 82% empty.

## Normalization (mandatory)
Depth≥10% + unified class map + year/contractor/standard covariate. Match: same pipe +
distance ±2m + offset ±0.5m + orient ±1h; else new/vanished with uncertainty flag.
Reference pair: ON 2016→2021→2025. Requests: 5 re-exports, pipe ages, per-survey thresholds.
