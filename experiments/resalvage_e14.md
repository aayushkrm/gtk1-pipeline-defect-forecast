# E14 re-salvage report (source re-derived, no /tmp copy)

## Salvage evidence
- raw-inflate: 153651/153826 bytes (tail 175B truncated)
- strict well-formed prefix: 2796/3158 entries; corruption at byte 134420
- SST[2884]='3321а' evidence at byte 138447: b'</si10 35>4>si><si><t xml:spa>3321\xd0\xb0si><t xml:space="preserve">\xd0\x9c9 510'
- pipe-token fragments in corrupt tail (char offsets): [(3707, '3321а'), (4952, '3321б'), (6617, '3372а')]
- tail rebuilt: 1 resolved (2884), 361 placeholder
- sheet2 parsed: 1218 data rows x 44 cols
- saved /Users/akm/Tsu Project/gtk1-forecast/outputs/srto1717_2024_salvaged.csv (459726 bytes)
- placeholder-pipe rows dropped: 5 (sheet rows [1092, 1093, 1104, 1105, 1106])

## Numbers (tolerance |diff|<=0.005 counts as match)

| metric | expected | re-derived | |diff| | verdict |
|---|---|---|---|---|
| 2021_d10 | 92 | 92 | 0.0000 | MATCH |
| match | 0.134 | 0.134 | 0.0000 | MATCH |
| prev | 0.1 | 0.1 | 0.0000 | MATCH |
| pos | 42 | 42 | 0.0000 | MATCH |
| B1 | 0.201 | 0.201 | 0.0000 | MATCH |
| base | 0.1 | 0.1 | 0.0000 | MATCH |
| lo | 0.019 | 0.019 | 0.0000 | MATCH |
| hi | 0.212 | 0.212 | 0.0000 | MATCH |
| 2024_d10 | 440 | 440 | 0 | MATCH |
| dropped | 5 | 5 | 0 | MATCH |

## Verdict: RE-DERIVED (numbers match within tolerance)

## Notes
- Full-precision check vs results_e14.json: match_rate, AP, base, lift, lift_CI, n_pos, n all diff 0.0 (bit-identical, incl. seed-0 bootstrap). Stronger than the tolerance verdict above.
- Dropped sheet rows 1092/1093 (SST 2900) + 1104/1105/1106 (SST 2928). Kept rows 1087-1091 carry resolved pipe '3321а'.
- Visible but unattributed tail fragments '3321б'/'3372а' stay placeholder (conservative rule, prior outcome same). Their distances (36789m/37343m) sit beyond 2021 coverage (~30km), so keeping them could only add unmatched-new rows, never matches.
- Side finding: results_e15.md 'CRCs pass' is wrong for this file; zip testzip names xl/sharedStrings.xml as the bad entry (sheet2 + all other streams CRC-clean).
