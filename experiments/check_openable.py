"""check_openable.py: per-file openability gate for partner drops (MONDAY_ACCEPTANCE step 2).

For every .xls/.xlsx/.csv under --root:
- magic-byte check (OLE D0CF11E0 / ZIP PK / text)
- Python reader open: openpyxl for zip content, tolerant xlrd for OLE (repo stack)
- optional LibreOffice headless round-trip (--libreoffice): convert-to-csv per file

Writes experiments/results_openable_<tag>.json (per-file status; raw values never stored).
Usage: python3 experiments/check_openable.py --root "/path/to/tree" [--libreoffice]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gtk1.io import _apply_tolerant_xlrd  # noqa: E402

SOFFICE = "/Applications/LibreOffice.app/Contents/MacOS/soffice"


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def reader_open(fp: Path) -> tuple[bool, str]:
    try:
        if fp.suffix.lower() == ".csv":
            for enc in ("utf-8", "utf-8-sig", "cp1251"):
                try:
                    open(fp, encoding=enc, errors="strict").read(4096)
                    return True, f"csv {enc}"
                except UnicodeDecodeError:
                    continue
            return False, "csv: no utf-8/cp1251 decode"
        is_zip = fp.suffix.lower() == ".xlsx" or open(fp, "rb").read(2) == b"PK"
        if is_zip:
            import openpyxl
            # Pass a file object: openpyxl rejects xlsx content under an .xls name
            # by extension before it ever looks inside.
            with open(fp, "rb") as fh:
                wb = openpyxl.load_workbook(fh, read_only=True, data_only=True)
                names = wb.sheetnames
                wb.close()
            return True, f"openpyxl sheets={len(names)}"
        import xlrd
        _apply_tolerant_xlrd()
        bk = xlrd.open_workbook(fp, on_demand=False)
        return True, f"xlrd sheets={len(bk.sheet_names())}"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def libreoffice_open(fp: Path, outdir: Path) -> tuple[bool, str]:
    try:
        r = subprocess.run(
            [SOFFICE, "--headless", "--norestore", "--nologo",
             "--convert-to", "csv", "--outdir", str(outdir), str(fp)],
            capture_output=True, text=True, timeout=300)
        if r.returncode != 0:
            return False, f"soffice rc={r.returncode}: {r.stderr.strip()[:120]}"
        return True, "soffice csv ok"
    except subprocess.TimeoutExpired:
        return False, "soffice timeout 300s"
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--libreoffice", action="store_true")
    ap.add_argument("--tag", default="drop")
    a = ap.parse_args()
    root = Path(a.root)
    entries = []
    for fp in sorted(root.rglob("*")):
        if not fp.is_file() or fp.suffix.lower() not in (".xls", ".xlsx", ".csv"):
            continue
        rel = nfc(str(fp.relative_to(root)))
        with open(fp, "rb") as fh:
            head = fh.read(4)
        ext = fp.suffix.lower()
        if ext == ".csv":
            magic = "text"
        elif ext == ".xlsx" or head[:2] == b"PK":
            magic = "zip"
        elif head == b"\xd0\xcf\x11\xe0":
            magic = "ole"
        else:
            magic = "BAD:" + head.hex()
        ok, note = reader_open(fp)
        rec = {"file": rel, "ext": ext, "magic": magic, "reader_ok": ok, "reader": note}
        if a.libreoffice:
            with tempfile.TemporaryDirectory() as td:
                lo_ok, lo_note = libreoffice_open(fp, Path(td))
            rec["libreoffice_ok"] = lo_ok
            rec["libreoffice"] = lo_note
        entries.append(rec)
        flag = "" if ok else "  <-- READER FAIL"
        print(f"{'OK ' if ok else 'FAIL'} {rel}{flag}")
    fails = [e for e in entries if not e["reader_ok"]]
    lo_fails = [e for e in entries if e.get("libreoffice_ok") is False]
    out = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"),
        "root": nfc(str(root)),
        "counts": {"files": len(entries), "reader_fail": len(fails),
                   "libreoffice_fail": len(lo_fails) if a.libreoffice else None},
        "entries": entries,
    }
    dest = ROOT / "experiments" / f"results_openable_{a.tag}.json"
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    print(f"-- {len(entries)} files, reader fails: {len(fails)}, libreoffice fails: {len(lo_fails) if a.libreoffice else 'n/a'} -> {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
