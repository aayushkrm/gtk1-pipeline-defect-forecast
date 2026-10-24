#!/usr/bin/env python3
"""inventory_npk.py: structure inventory for the new partner drop (Датасет НПК).

For every table under --root: sheet names, row/column counts, and the first
rows as text (truncated). Writes experiments/results_inventory_<tag>.json.
Raw cell values are kept only as short header previews, never full data.

Usage: python3 experiments/inventory_npk.py --root "/path/to/Датасет НПК" --tag npk
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gtk1.io import _apply_tolerant_xlrd  # noqa: E402

PREVIEW_ROWS = 6
PREVIEW_COLS = 14


def read_sheets(fp: Path):
    """Yield (sheet_name, rows) for xls/xlsx, tolerant of broken OLE files."""
    is_zip = fp.suffix.lower() == ".xlsx" or open(fp, "rb").read(2) == b"PK"
    if is_zip:
        import openpyxl

        with open(fp, "rb") as fh:
            wb = openpyxl.load_workbook(fh, read_only=True, data_only=True)
            for name in wb.sheetnames:
                ws = wb[name]
                rows = []
                for i, row in enumerate(ws.iter_rows(values_only=True)):
                    if i >= PREVIEW_ROWS:
                        break
                    rows.append(list(row[:PREVIEW_COLS]))
                yield name, ws.max_row, ws.max_column, rows
            wb.close()
        return

    import xlrd

    _apply_tolerant_xlrd()
    bk = xlrd.open_workbook(fp, on_demand=False)
    for name in bk.sheet_names():
        sh = bk.sheet_by_name(name)
        rows = []
        for r in range(min(PREVIEW_ROWS, sh.nrows)):
            rows.append([sh.cell_value(r, c) for c in range(min(PREVIEW_COLS, sh.ncols))])
        yield name, sh.nrows, sh.ncols, rows


def cell(v):
    if v is None:
        return ""
    s = str(v).strip().replace("\n", " ")
    return s[:40]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--tag", default="npk")
    args = ap.parse_args()

    root = Path(args.root)
    out = []
    for fp in sorted(root.rglob("*")):
        if fp.suffix.lower() not in (".xls", ".xlsx", ".xlsm", ".csv"):
            continue
        rec = {"file": str(fp.relative_to(root)), "bytes": fp.stat().st_size, "sheets": []}
        try:
            for name, nrows, ncols, rows in read_sheets(fp):
                rec["sheets"].append({
                    "name": name,
                    "rows": nrows,
                    "cols": ncols,
                    "preview": [[cell(v) for v in row] for row in rows],
                })
        except Exception as exc:  # noqa: BLE001
            rec["error"] = f"{type(exc).__name__}: {exc}"
        out.append(rec)
        print(f"{rec['file']}\n    sheets={[(s['name'], s['rows'], s['cols']) for s in rec['sheets']]}")

    dest = ROOT / "experiments" / f"results_inventory_{args.tag}.json"
    preview_dest = ROOT / "outputs" / "npk" / f"inventory_preview_{args.tag}.json"
    preview_dest.parent.mkdir(parents=True, exist_ok=True)
    preview_dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    # Committed inventory keeps structure only; raw previews stay in git-ignored outputs/.
    slim = []
    for rec in out:
        s = {k: v for k, v in rec.items() if k != "sheets"}
        s["sheets"] = [{k: v for k, v in sh.items() if k != "preview"} for sh in rec["sheets"]]
        slim.append(s)
    dest.write_text(json.dumps(slim, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(out)} files -> {dest} (structure only)")
    print(f"previews -> {preview_dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
