"""Row-level detail of the revised files in the October 2026 drop.

For every pair that compare_drop.py marked REVISED:
- per sheet: non-empty row count, max column, total non-empty cells (old -> new)
- for the first numeric column whose header looks like a distance/chainage column:
  min/max (m) old vs new
- total differing cell count (positions not stored)

Aggregates only. Raw values never stored. Writes experiments/results_drop_revisions.json.
"""
from __future__ import annotations

import json
import os
import sys
import unicodedata
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_ROOT = os.path.normpath(os.path.join(ROOT, "..", "Датасет ВТД"))
OLD_ROOT = os.path.normpath(os.path.join(ROOT, "..", "Данные для предварительного изучения"))
OUT = os.path.join(ROOT, "experiments", "results_drop_revisions.json")

sys.path.insert(0, os.path.join(ROOT, "src"))
import gtk1.io as g_io  # noqa: E402
import openpyxl  # noqa: E402
from xlrd import open_workbook  # noqa: E402


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


SECMAP = {
    "Омск-Новосибирск (392-526)": "ON",
    "Отчет ВТД_Ю-Н_0-154": "YN",
    "Парабель-Кузбасс-1 (572-714)": "PK1",
    "Парабель - Кузбасс 1 572-714 км": "PK1",
    "Парабель - Кузбасс 1 110-242": "PK1-110-242",
    "Парабель-Кузбасс-2 (0-110)": "PK2",
    "СРТО-Омск_(1608 – 1717)": "SRTO1608",
    "СРТО-Омск_(1717-1759)": "SRTO1717",
    "Нижневартовский ГПЗ-Парабель I (306-448 км) (КС Вертикос - КС Парабель)": "NVP",
    "Новосибирск - Барнаул 0 - 123 км": "NB",
    "Отвод ГРС-3 - Барнаул": "OGRS3",
    "СХВ_0-96": "SXV",
    "УКПГ2 - АГРС 216-388 км": "UKPG2",
}


def kind(fn: str) -> str:
    f = fn.lower()
    if "аномали" in f or "дефект" in f or "otchet" in f:
        return "anomaly"
    if "сварн" in f:
        return "weld"
    if "журнал" in f:
        return "pipejournal"
    if "линейн" in f:
        return "linearobj"
    if "трубны" in f:
        return "tubeelem"
    return "other"


def sheets_of(fp: str):
    if fp.lower().endswith(".xlsx") or open(fp, "rb").read(2) == b"PK":
        wb = openpyxl.load_workbook(fp, read_only=True, data_only=True)
        for ws in wb.worksheets:
            rows = [list(r) for r in ws.iter_rows(values_only=True)]
            yield ws.title, rows
        wb.close()
    else:
        g_io._apply_tolerant_xlrd()
        bk = open_workbook(fp, on_demand=False)
        for sh in bk.sheets():
            rows = [[sh.cell_value(rx, cx) for cx in range(sh.row_len(rx))] for rx in range(sh.nrows)]
            yield sh.name, rows


def numeric(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        t = v.replace(",", ".").strip()
        try:
            return float(t)
        except ValueError:
            return None
    return None


def sheet_stats(rows) -> dict:
    n_rows = 0
    maxw = 0
    n_cells = 0
    for r in rows:
        vals = [v for v in r if v is not None and str(v).strip() != ""]
        if vals:
            n_rows += 1
            n_cells += len(vals)
            maxw = max(maxw, len(r))
    return {"rows_nonempty": n_rows, "max_cols": maxw, "cells_nonempty": n_cells}


def distance_span(rows) -> dict | None:
    """Find a header cell containing расстояние/дистанция within the first 6 rows,
    then min/max of the numeric column below it."""
    for hi, r in enumerate(rows[:6]):
        for ci, v in enumerate(r):
            if v is None:
                continue
            s = str(v).lower()
            if ("расстоян" in s or "дистанц" in s) and ("м" in s):
                vals = []
                for rr in rows[hi + 1:]:
                    if ci < len(rr):
                        x = numeric(rr[ci])
                        if x is not None:
                            vals.append(x)
                if vals:
                    return {"header_row": hi, "col": ci, "min": min(vals), "max": max(vals),
                            "n_numeric": len(vals)}
    return None


def grid(rows_per_sheet: dict) -> dict:
    # join all sheets with row lists for the cell diff
    return {name: rows for name, rows in rows_per_sheet.items()}


def cell_diff(a: dict, b: dict) -> dict:
    keys = sorted(set(a) | set(b))
    total = 0
    for k in keys:
        ra, rb = a.get(k, []), b.get(k, [])
        for i in range(max(len(ra), len(rb))):
            xa = ra[i] if i < len(ra) else []
            xb = rb[i] if i < len(rb) else []
            w = max(len(xa), len(xb))
            for j in range(w):
                va = xa[j] if j < len(xa) else None
                vb = xb[j] if j < len(xb) else None
                sa = "" if va is None else str(va).strip()
                sb = "" if vb is None else str(vb).strip()
                if sa != sb:
                    total += 1
    return {"diff_cells": total}


def file_detail(fp: str) -> dict:
    if fp.lower().endswith(".csv"):
        last = None
        for enc in ("utf-8", "utf-8-sig", "cp1251"):
            try:
                text = open(fp, encoding=enc).read()
                return {"csv": {"encoding": enc, "lines": text.count("\n") + 1}}
            except UnicodeDecodeError as exc:  # noqa: PERF203
                last = exc
        raise ValueError(f"csv decode failed: {last}")
    per_sheet = {}
    grids = {}
    spans = {}
    for name, rows in sheets_of(fp):
        per_sheet[name] = sheet_stats(rows)
        grids[nfc(name)] = rows
        sp = distance_span(rows)
        if sp:
            spans[nfc(name)] = sp
    return {"per_sheet": per_sheet, "spans": spans, "_grid": grids}


def main() -> None:
    new_files = []
    seen = set()
    for dp, _, fn in os.walk(NEW_ROOT):
        for f in fn:
            fp = os.path.join(dp, f)
            rel = nfc(os.path.relpath(fp, NEW_ROOT))
            parts = rel.split("/")
            if len(parts) < 3:
                continue
            k = SECMAP.get(parts[0])
            if not k:
                continue
            key = (k, parts[1], kind(parts[2]))
            if key in seen:
                continue
            seen.add(key)
            new_files.append({"key": k, "year": parts[1], "kind": kind(parts[2]), "path": fp, "name": parts[2]})

    old_files = []
    for dp, _, fn in os.walk(OLD_ROOT):
        for f in fn:
            fp = os.path.join(dp, f)
            rel = nfc(os.path.relpath(fp, OLD_ROOT))
            parts = rel.split("/")
            if len(parts) < 3:
                continue
            k = SECMAP.get(parts[0])
            old_files.append({"key": k, "year": parts[1], "kind": kind(parts[2]), "path": fp, "name": parts[2]})

    out = []
    for n in sorted(new_files, key=lambda x: (x["key"], x["year"], x["kind"])):
        o = next((o for o in old_files if o["key"] == n["key"] and o["year"] == n["year"] and o["kind"] == n["kind"]), None)
        if o is None:
            continue
        if os.path.getsize(o["path"]) != os.path.getsize(n["path"]):
            pass  # still compare
        import hashlib

        def m5(p):
            h = hashlib.md5()
            with open(p, "rb") as fh:
                for c in iter(lambda: fh.read(1 << 20), b""):
                    h.update(c)
            return h.hexdigest()
        if m5(o["path"]) == m5(n["path"]):
            continue
        rec = {
            "section": n["key"], "year": n["year"], "kind": n["kind"], "name": nfc(n["name"]),
        }
        do = dn = None
        try:
            do = file_detail(o["path"])
        except Exception as exc:  # noqa: BLE001
            rec["old_error"] = f"{type(exc).__name__}: {exc}"
        try:
            dn = file_detail(n["path"])
        except Exception as exc:  # noqa: BLE001
            rec["new_error"] = f"{type(exc).__name__}: {exc}"
        if do and dn:
            rec.update({
                "old_per_sheet": do.get("per_sheet", {}), "new_per_sheet": dn.get("per_sheet", {}),
                "old_spans": do.get("spans", {}), "new_spans": dn.get("spans", {}),
                "cell_diff": cell_diff(do.get("_grid", {}), dn.get("_grid", {})),
            })
            if "csv" in dn:
                rec["csv"] = {"old": do.get("csv"), "new": dn.get("csv")}
        out.append(rec)

    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "entries": out,
    }
    with open(OUT, "w") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, allow_nan=False)
    print(f"revised pairs detailed: {len(out)}")
    for rec in out:
        if "old_error" in rec or "new_error" in rec:
            side = "OLD" if "old_error" in rec else "NEW"
            err = rec.get("old_error") or rec.get("new_error")
            print(f"  {rec['section']:<12} {rec['year']} {rec['kind']:<11} {side}-UNREADABLE {err[:90]}")
            continue
        if "csv" in rec:
            print(f"  {rec['section']:<12} {rec['year']} {rec['kind']:<11} csv {rec['csv']['old']} -> {rec['csv']['new']}")
            continue
        oldc = sum(s["cells_nonempty"] for s in rec["old_per_sheet"].values())
        newc = sum(s["cells_nonempty"] for s in rec["new_per_sheet"].values())
        sp_o = {k: (v["min"], v["max"]) for k, v in rec["old_spans"].items()}
        sp_n = {k: (v["min"], v["max"]) for k, v in rec["new_spans"].items()}
        print(f"  {rec['section']:<12} {rec['year']} {rec['kind']:<11} cells {oldc}->{newc} diff={rec['cell_diff']['diff_cells']}")
        if sp_o or sp_n:
            print(f"      spans old={sp_o} new={sp_n}")
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    main()
