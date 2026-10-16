"""Compare the October 2026 partner drop against the previous raw room.

Read-only over both raw trees (never committed). Pair = (section, year, kind).

Statuses:
- IDENTICAL          bytes match
- CONTENT-IDENTICAL  bytes differ, data is equal (metadata-only re-save)
- REVISED            data differs (row/col counts or cell content)
- READABLE-ONESIDE / UNREADABLE-BOTHS for damaged files
- NEW-FILE           no counterpart in the old room

.xlsx: zip member hash diff first (fast, no parse); only differing members listed.
       Parse via openpyxl read_only when sheet XML itself differs.
.xls:  tolerant xlrd patches from src.gtk1.io; raw grid (header=None, all sheets).
.csv:  utf-8 -> utf-8-sig -> cp1251 tiers.

Writes experiments/results_drop_compare.json (aggregates; no raw values).
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import unicodedata
import zipfile
from datetime import datetime, timezone

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
import gtk1.io as g_io  # noqa: E402

NEW_ROOT = os.path.normpath(os.path.join(ROOT, "..", "Датасет ВТД"))
OLD_ROOT = os.path.normpath(os.path.join(ROOT, "..", "Данные для предварительного изучения"))
OUT = os.path.join(ROOT, "experiments", "results_drop_compare.json")


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


def md5(fp: str) -> str:
    h = hashlib.md5()
    with open(fp, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(root: str) -> list[dict]:
    out = []
    for dp, _, fn in os.walk(root):
        for f in fn:
            fp = os.path.join(dp, f)
            rel = nfc(os.path.relpath(fp, root))
            parts = rel.split("/")
            if len(parts) >= 3:
                out.append({
                    "key": SECMAP.get(parts[0], parts[0]),
                    "year": parts[1],
                    "kind": kind(parts[2]),
                    "name": parts[2],
                    "md5": md5(fp),
                    "size": os.path.getsize(fp),
                    "path": fp,
                })
    return out


def zip_members(fp: str) -> dict[str, str]:
    out = {}
    with zipfile.ZipFile(fp) as zf:
        for info in zf.infolist():
            try:
                out[info.filename] = hashlib.md5(zf.read(info.filename)).hexdigest()
            except Exception:  # noqa: BLE001
                out[info.filename] = "READ-FAIL"
    return out


def grid_digest(path: str) -> dict:
    """Raw grid digest for xls/xlsx: all sheets, no header assumption."""
    h = hashlib.sha256()
    sheets = 0
    cells = 0
    if path.lower().endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            sheets += 1
            h.update(f"[{ws.title}]".encode())
            for row in ws.iter_rows(values_only=True):
                cells += len(row)
                h.update("\x1f".join("" if v is None else str(v) for v in row).encode())
                h.update(b"\n")
        wb.close()
    else:
        from xlrd import open_workbook
        g_io._apply_tolerant_xlrd()
        bk = open_workbook(path, on_demand=False)
        for sh in bk.sheets():
            sheets += 1
            h.update(f"[{sh.name}]".encode())
            for rx in range(sh.nrows):
                cells += sh.row_len(rx)
                h.update("\x1f".join(str(sh.cell_value(rx, cx)) for cx in range(sh.row_len(rx))).encode())
                h.update(b"\n")
    return {"sheets": sheets, "cells": cells, "digest": h.hexdigest()[:16]}


def csv_digest(fp: str) -> dict:
    last = None
    for enc in ("utf-8", "utf-8-sig", "cp1251"):
        try:
            text = open(fp, encoding=enc).read()
            return {"encoding": enc, "sha": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
                    "lines": text.count("\n") + 1}
        except UnicodeDecodeError as exc:  # noqa: PERF203
            last = exc
    raise ValueError(f"csv decode failed: {last}")


def compare(o: dict, n: dict) -> dict:
    rec = {"section": n["key"], "year": n["year"], "kind": n["kind"], "name": nfc(n["name"]),
           "old_size": o["size"], "new_size": n["size"]}
    ext = os.path.splitext(n["name"])[1].lower()
    if ext == ".xlsx":
        try:
            mo, mn = zip_members(o["path"]), zip_members(n["path"])
            only_old = sorted(set(mo) - set(mn))
            only_new = sorted(set(mn) - set(mo))
            changed = sorted(k for k in set(mo) & set(mn) if mo[k] != mn[k])
            rec["changed_members"] = changed
            if not only_old and not only_new and not changed:
                rec["status"] = "CONTENT-IDENTICAL"
                return rec
            parse_members = [m for m in changed + only_old + only_new if m.startswith("xl/") and (m.endswith(".xml") or m.endswith(".bin"))]
            if not parse_members:
                rec["status"] = "CONTENT-IDENTICAL"
                rec["note"] = "only metadata members differ"
                return rec
            rec["status"] = "REVISED"
            rec["parse_members"] = parse_members
            return rec
        except Exception as exc:  # noqa: BLE001
            rec["status"] = "READ-ERROR"
            rec["error"] = f"{type(exc).__name__}: {exc}"
            return rec
    if ext == ".csv":
        try:
            do, dn = csv_digest(o["path"]), csv_digest(n["path"])
            rec["old_lines"], rec["new_lines"] = do["lines"], dn["lines"]
            rec["status"] = "CONTENT-IDENTICAL" if do["sha"] == dn["sha"] else "REVISED"
            if do["encoding"] != dn["encoding"]:
                rec["note"] = f"encoding {do['encoding']} -> {dn['encoding']}"
                if do["sha"] == dn["sha"]:
                    rec["status"] = "CONTENT-IDENTICAL"
            return rec
        except Exception as exc:  # noqa: BLE001
            rec["status"] = "READ-ERROR"
            rec["error"] = f"{type(exc).__name__}: {exc}"
            return rec
    # .xls raw grid
    o_dig = o_read = n_dig = n_read = None
    try:
        o_dig = grid_digest(o["path"])
        o_read = True
    except Exception as exc:  # noqa: BLE001
        rec["old_error"] = f"{type(exc).__name__}: {exc}"
    try:
        n_dig = grid_digest(n["path"])
        n_read = True
    except Exception as exc:  # noqa: BLE001
        rec["new_error"] = f"{type(exc).__name__}: {exc}"
    if o_read and n_read:
        rec["old_cells"], rec["new_cells"] = o_dig["cells"], n_dig["cells"]
        rec["status"] = "CONTENT-IDENTICAL" if o_dig["digest"] == n_dig["digest"] else "REVISED"
        if o_dig["digest"] != n_dig["digest"]:
            rec["old_sheets"], rec["new_sheets"] = o_dig["sheets"], n_dig["sheets"]
    elif o_read or n_read:
        rec["status"] = "READABLE-ONESIDE"
    else:
        rec["status"] = "UNREADABLE-BOTHS"
    return rec


def main() -> None:
    new = scan(NEW_ROOT)
    old = scan(OLD_ROOT)
    used_old: set[str] = set()
    entries = []
    # dedupe identical new-tree copies first (PK1 appears under two folder spellings)
    by_md5: dict[str, str] = {}
    for n in sorted(new, key=lambda x: (x["key"], x["year"], x["kind"], x["path"])):
        if n["md5"] in by_md5:
            entries.append({"section": n["key"], "year": n["year"], "kind": n["kind"],
                            "name": nfc(n["name"]), "status": "DUPLICATE-OF-ANOTHER-NEW-FOLDER",
                            "same_as": nfc(by_md5[n["md5"]])})
            continue
        by_md5[n["md5"]] = os.path.relpath(n["path"], NEW_ROOT)
        o = next((o for o in old if o["key"] == n["key"] and o["year"] == n["year"]
                  and o["kind"] == n["kind"] and o["md5"] not in used_old), None)
        if o is None:
            o2 = next((o for o in old if o["key"] == n["key"] and o["year"] == n["year"]
                       and o["kind"] == n["kind"]), None)
            if o2 is None:
                entries.append({"section": n["key"], "year": n["year"], "kind": n["kind"],
                                "name": nfc(n["name"]), "status": "NEW-FILE", "new_size": n["size"]})
            else:
                entries.append({"section": n["key"], "year": n["year"], "kind": n["kind"],
                                "name": nfc(n["name"]), "status": "DUPLICATE-OF-ANOTHER-NEW-FOLDER",
                                "same_as": nfc(os.path.relpath(o2["path"], OLD_ROOT))})
            continue
        used_old.add(o["md5"])
        if o["md5"] == n["md5"]:
            entries.append({"section": n["key"], "year": n["year"], "kind": n["kind"],
                            "name": nfc(n["name"]), "status": "IDENTICAL", "size": n["size"]})
        else:
            entries.append(compare(o, n))
    counts: dict[str, int] = {}
    for e in entries:
        counts[e["status"]] = counts.get(e["status"], 0) + 1
    payload = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "counts": counts,
        "entries": entries,
        "repro": subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT,
                                capture_output=True, text=True).stdout.strip(),
    }
    with open(OUT, "w") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, allow_nan=False)
    print(json.dumps(counts, ensure_ascii=False))
    for e in entries:
        if e["status"] not in ("NEW-FILE", "IDENTICAL"):
            detail = e.get("note") or e.get("error") or (f"cells {e.get('old_cells')}->{e.get('new_cells')}"
                      if "old_cells" in e else "") or ",".join(e.get("changed_members", [])[:3])
            print(f"  {e['status']:<28} {e['section']:<12} {e['year']} {e['kind']:<11} {detail}")
    print("wrote", os.path.relpath(OUT, ROOT))


if __name__ == "__main__":
    sys.exit(main())
