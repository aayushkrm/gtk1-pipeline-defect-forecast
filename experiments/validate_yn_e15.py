"""YN E15 phase 2: tier salvage + header map + validation + CSVs.

Tiers per sheet stream:
  A clean  = one valid <row r="N">...</row>, unique N, cells parse
  B dup    = valid open but repeated N (duplication-garble marker rows)
  C mangled= </row> with destroyed open tag (un-numbered, cells smashed)
  D multi  = several opens in one chunk (duplication runs)
Only tier A (+ deduped B-identical) can form records. C/D counted, not parsed.
Writes: yn2020_anom_salvaged.csv, yn2023_feat_salvaged.csv,
        yn2023_anom_salvaged.csv + yn_e15_summary.json into outputs/.
"""
import json
import re
import sys
import csv
import zipfile
import collections
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs"
sys.path.insert(0, str(REPO / "experiments"))
from salvage_yn_e15 import (inflate, load_strings, salvage_rows, parse_cells,
                            F20, F23)

CELL_RE = re.compile(r'<c r="([A-Z]+)\d+"[^>]*>(.*?)</c>', re.S)
V_RE = re.compile(r"<v>(.*?)</v>", re.S)
RO = re.compile(r'<row r="(\d+)"')


def tier_split(xml_text):
    chunks = xml_text.split("</row>")
    A, C, D = [], 0, []
    for pos, ch in enumerate(chunks):
        opens = RO.findall(ch)
        if not opens:
            if "<c " in ch:
                C += 1
            continue
        if len(opens) == 1:
            A.append((pos, int(opens[0]), ch))
        else:
            D.append((pos, opens))
    return A, C, D


def resolve_row(chunk, ss):
    """Parse cells; return (cells, ngarbage). Garbage = s-cell with non-int v."""
    cells, ng = {}, 0
    for m in CELL_RE.finditer(chunk):
        col_letters = m.group(1)
        n = 0
        for ch in col_letters:
            n = n * 26 + (ord(ch) - 64)
        col = n - 1
        b = m.group(2)
        vm = V_RE.search(b)
        v = vm.group(1).strip() if vm else ""
        if 't="s"' in m.group(0)[:80] and v != "":
            try:
                v = ss[int(v)] if "." not in v and "e" not in v.lower() else ss[int(float(v))]
            except (ValueError, IndexError):
                ng += 1
                v = f"GARBAGE:{v[:30]}"
        cells[col] = v
    return cells, ng


def headers_of(A, ss):
    for pos, r, ch in A:
        if r == 1 or r == 4:
            cells, ng = resolve_row(ch, ss)
            if len(cells) >= 8:
                return r, cells, ng
    return None, {}, 0


def analyze(name, xlsx, part, cache, header_row):
    ss = load_strings(xlsx)
    print(f"{name}: strings={len(ss)}", flush=True)
    txt = inflate(xlsx, part, cache)
    A, C, D = tier_split(txt)
    hdr_r, hdr, hng = headers_of(A, ss)
    print(f"{name}: tierA={len(A)} tierC(mangled)={C} tierD(multi)={len(D)} "
          f"hdr_row={hdr_r} hdr_cols={len(hdr)}", flush=True)
    for i in sorted(hdr):
        print(f"  H{i}={hdr[i][:44]!r}")
    # resolve all tier-A rows
    rows = []
    for pos, r, ch in A:
        cells, ng = resolve_row(ch, ss)
        rows.append((pos, r, cells, ng))
    rows.sort()
    # dup r numbers
    cnt = collections.Counter(r for _, r, _, _ in rows)
    dups = {k: v for k, v in cnt.items() if v > 1}
    print(f"{name}: dup_r={len(dups)} dup_rows={sum(dups.values())}", flush=True)
    # data rows below header
    data = [(p, r, c, ng) for p, r, c, ng in rows if r > header_row]
    print(f"{name}: data_rows={len(data)} row_span="
          f"{min(r for _,r,_,_ in data)}..{max(r for _,r,_,_ in data)}", flush=True)
    return ss, hdr, rows, data, dups, C, D


def num(x):
    try:
        return float(str(x).replace(",", "."))
    except (ValueError, TypeError):
        return None


def col_stats(data, col, name):
    vals = [c.get(col, "") for _, _, c, _ in data]
    nums = [num(v) for v in vals]
    ok = [v for v in nums if v is not None]
    mono_viol = sum(1 for a, b in zip(ok, ok[1:]) if b < a)
    empt = sum(1 for v in vals if v == "")
    print(f"  col{col} {name}: n={len(vals)} empty={empt} numeric={len(ok)} "
          f"min={min(ok) if ok else None} max={max(ok) if ok else None} "
          f"mono_viol={mono_viol}")
    return {"n": len(vals), "empty": empt, "numeric": len(ok),
            "min": min(ok) if ok else None, "max": max(ok) if ok else None,
            "mono_viol": mono_viol}


def valcounts(data, col, name, top=12):
    cnt = collections.Counter(c.get(col, "") for _, _, c, _ in data)
    print(f"  col{col} {name}: distinct={len(cnt)}")
    for k, v in cnt.most_common(top):
        print(f"    {v:6d} {str(k)[:50]!r}")
    return {str(k)[:50]: v for k, v in cnt.most_common(top)}


def write_csv(path, hdr, data, maxcol):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["_row", "_garbage_cells"] +
                   [hdr.get(i, f"C{i}") for i in range(maxcol + 1)])
        for _, r, c, ng in data:
            w.writerow([r, ng] + [c.get(i, "") for i in range(maxcol + 1)])


def main():
    summary = {}
    # ---- 2020 anomalies: header row 4, 45 cols ----
    ss, hdr, rows, data, dups, C, D = analyze("YN2020", F20,
                                             "xl/worksheets/sheet3.xml",
                                             "_yn20_sheet3.xml", 4)
    s = summary["yn2020_anom"] = {"tierA": len(rows), "mangled": C,
                                  "multi": len(D), "dups": len(dups),
                                  "data_rows": len(data)}
    s["distance"] = col_stats(data, 1, "Distance")
    s["pipe"] = col_stats(data, 11, "PipeNo")
    s["depth"] = col_stats(data, 31, "Depth%")
    s["character"] = valcounts(data, 19, "Character")
    s["type"] = valcounts(data, 18, "Type")
    depths = [num(c.get(31, "")) for _, _, c, _ in data]
    okd = [v for v in depths if v is not None]
    s["depth_ge10_share"] = (sum(1 for v in okd if v >= 10) / len(okd)
                             if okd else None)
    print(f"  depth>=10 share_of_measured = {s['depth_ge10_share']}")
    pipes = [c.get(11, "") for _, _, c, _ in data]
    print(f"  pipe sample: {pipes[:5]} .. {pipes[-3:]} distinct="
          f"{len(set(pipes))}")
    s["pipe_sample"] = pipes[:5]
    write_csv(OUT / "yn2020_anom_salvaged.csv", hdr, data, 44)
    # garbage-cell histogram
    gh = collections.Counter(ng for _, _, _, ng in data)
    print(f"  garbage_cells/row hist: {sorted(gh.items())[:10]}")
    s["garbage_hist"] = {str(k): v for k, v in sorted(gh.items())}

    # ---- 2023 features: header row 1, 18 cols ----
    ss3, hdr3, rows3, data3, dups3, C3, D3 = analyze("YN2023-FEAT", F23,
                                                    "xl/worksheets/sheet3.xml",
                                                    "_yn23_feat.xml", 1)
    s = summary["yn2023_feat"] = {"tierA": len(rows3), "mangled": C3,
                                  "multi": len(D3), "dups": len(dups3),
                                  "data_rows": len(data3)}
    s["pipe"] = col_stats(data3, 1, "Npipe")
    s["distance"] = col_stats(data3, 2, "Distance")
    feat_type = 6
    s["type"] = valcounts(data3, feat_type, "Type")
    write_csv(OUT / "yn2023_feat_salvaged.csv", hdr3, data3, 17)
    gh = collections.Counter(ng for _, _, _, ng in data3)
    print(f"  garbage_cells/row hist: {sorted(gh.items())[:10]}")
    s["garbage_hist"] = {str(k): v for k, v in sorted(gh.items())}

    # ---- 2023 anomalies: header row 1, 20 cols ----
    ss4, hdr4, rows4, data4, dups4, C4, D4 = analyze("YN2023-ANOM", F23,
                                                    "xl/worksheets/sheet4.xml",
                                                    "_yn23_anom.xml", 1)
    s = summary["yn2023_anom"] = {"tierA": len(rows4), "mangled": C4,
                                  "multi": len(D4), "dups": len(dups4),
                                  "data_rows": len(data4)}
    s["pipe"] = col_stats(data4, 1, "Npipe")
    s["distance"] = col_stats(data4, 2, "Distance")
    write_csv(OUT / "yn2023_anom_salvaged.csv", hdr4, data4,
              max(len(hdr4) - 1, 19))
    gh = collections.Counter(ng for _, _, _, ng in data4)
    print(f"  garbage_cells/row hist: {sorted(gh.items())[:10]}")
    s["garbage_hist"] = {str(k): v for k, v in sorted(gh.items())}

    (OUT / "yn_e15_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    print("wrote CSVs + yn_e15_summary.json")


if __name__ == "__main__":
    main()
