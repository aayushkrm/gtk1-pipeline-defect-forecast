# E15 full integrity audit — 32 files, strict + tolerant (user-challenged re-verification)

Method: per file — container check (ZIP CRCs / OLE open), sheet list, strict full-row parse per
sheet, tolerant fallback. Read-only. Tally: 24 CLEAN, 5 RECOVERABLE, 1 DEAD, 2 PARTIAL
(both PARTIALs are audit-strictness artifacts, corrected below).

## Corrections to prior claims (auditor overstatements fixed)
- SRTO-1717-2024A "corrupt" was WRONG: 1,220 + 3,814 sheet rows strict-parse. Correction to the
  correction (E14 re-salvage): its sharedStrings.xml CRC FAILS (tail ~175B truncated); only the sheet
  streams are clean. Salvage re-derived E14 bit-identical (diff 0.0 all 8 metrics incl. seed-0
  bootstrap); repaired CSV + script now durable (outputs/ + experiments/resalvage_e14.py). Only the
  dimension tag issue was cosmetic; the CRC issue is real but worked around.
- PK2-2025 anomalies: strict parsers fail, but byte-salvage recovers 2,162 rows (proven earlier).
  RECOVERABLE, not dead.
- PK2-2025 CSV: single bad byte is an encoding flag (cp1251 / errors=replace reads it).
  RECOVERABLE, not partial.
- PK1-2025 weld .xls: DEAD under stock + tolerant xlrd (AssertionError both). olefix attempt queued;
  not yet final. ON-2025 and PK1-2019T need tolerant patches (known, working).

## Genuinely absent data (unrecoverable at any cost — not corruption, never written)
- PK1-2019 rows 2864+ (~54% of expected): absent from the file, not garbled.
- ON-2025 weld tail beyond 27 km + PK1-2025 weld tail (~65 KB): missing vs truncation unclear.
- YN-2023 anomaly journal majority: garbled repeats, only ~4,405 clean rows.

## Standing conclusion (sharpened, not reversed)
User is more right than the old table suggested: 24/32 files are fully clean and almost everything
else has a working recovery path. What remains is absent data (re-export only) plus one DEAD file
pending olefix. Pair verdicts stand: PK2 blocked on comparability (not readability), Yu-N pair
pending E15 validation, E14 void. No valid pair was ever lost to strict-parser failure alone.
