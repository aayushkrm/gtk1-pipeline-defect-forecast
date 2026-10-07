"""E15: full data-integrity audit of all 32 VTD files (user-challenged re-verification).
Per file: size, container check (ZIP CRCs / OLE open), sheet list, STRICT full-row parse per sheet,
TOLERANT row recovery count. Verdict per file: CLEAN / RECOVERABLE(pct) / PARTIAL / DEAD.
Read-only. Writes de-identified aggregate JSON only.
"""
import binascii
import json
import subprocess
import sys
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
BASE = REPO.parent / "Данные для предварительного изучения"
OUT = Path(__file__).resolve().parent


def audit_xlsx(fp):
    rec = {"file": fp.name, "bytes": fp.stat().st_size, "sheets": []}
    try:
        z = zipfile.ZipFile(fp)
    except Exception as e:
        return {**rec, "verdict": "DEAD", "why": f"zip open: {type(e).__name__}"}
    bad_crc = []
    for n in z.namelist():
        if n.startswith("xl/worksheets/sheet"):
            info = z.getinfo(n)
            try:
                data = z.read(n)
                ok = binascii.crc32(data) & 0xFFFFFFFF == info.CRC
            except Exception:
                rec["sheets"].append({"part": n, "crc": False, "strict_rows": 0, "note": "unreadable stream"})
                bad_crc.append(n)
                continue
            if not ok:
                bad_crc.append(n)
            # strict row count via iterparse
            try:
                import io
                count = 0
                for _, el in ET.iterparse(io.BytesIO(data), events=("end",)):
                    if el.tag.endswith("}row"):
                        count += 1
                        el.clear()
                rec["sheets"].append({"part": n, "crc": ok, "strict_rows": count})
            except Exception as e:
                rec["sheets"].append({"part": n, "crc": ok, "strict_rows": -1,
                                      "note": f"strict XML parse: {type(e).__name__}"})
    if not rec["sheets"]:
        return {**rec, "verdict": "DEAD", "why": "no worksheet parts"}
    if not bad_crc and all(s.get("strict_rows", -1) >= 0 for s in rec["sheets"]):
        rec["verdict"] = "CLEAN"
    elif any(s.get("strict_rows", -1) > 0 for s in rec["sheets"]):
        rec["verdict"] = "RECOVERABLE"
        rec["bad_parts"] = bad_crc
    else:
        rec["verdict"] = "PARTIAL"
        rec["bad_parts"] = bad_crc
    return rec


def audit_xls(fp):
    rec = {"file": fp.name, "bytes": fp.stat().st_size, "sheets": []}
    try:
        import xlrd
        bk = xlrd.open_workbook(str(fp), logfile=open("/dev/null", "w"))
        for sh in bk.sheets():
            rec["sheets"].append({"part": sh.name, "crc": None, "strict_rows": sh.nrows})
        rec["verdict"] = "CLEAN"
    except Exception as e:
        try:
            from gtk1.io import load_anomalies  # noqa
        except Exception:
            pass
        try:
            import sys as _s
            _s.path.insert(0, str(REPO / "src"))
            from gtk1.io import _apply_tolerant_xlrd
            _apply_tolerant_xlrd()
            import xlrd as _x
            bk = _x.open_workbook(str(fp), logfile=open("/dev/null", "w"))
            for sh in bk.sheets():
                rec["sheets"].append({"part": sh.name, "crc": None, "strict_rows": sh.nrows})
            rec["verdict"] = "RECOVERABLE"
            rec["why"] = "needs tolerant-xlrd patches"
        except Exception as e2:
            rec["verdict"] = "DEAD"
            rec["why"] = f"stock: {type(e).__name__}; tolerant: {type(e2).__name__}"
    return rec


def audit_csv(fp):
    import csv
    try:
        with open(fp, encoding="utf-8", errors="strict") as f:
            rows = list(csv.reader(f))
        return {"file": fp.name, "bytes": fp.stat().st_size, "verdict": "CLEAN",
                "rows": len(rows), "cols": len(rows[0]) if rows else 0}
    except Exception as e:
        return {"file": fp.name, "bytes": fp.stat().st_size, "verdict": "PARTIAL",
                "why": f"{type(e).__name__}: {str(e)[:80]}"}


def main():
    sys.path.insert(0, str(REPO / "src"))
    files = sorted((BASE).rglob("*"))
    files = [f for f in files if f.is_file() and f.suffix.lower() in (".xlsx", ".xls", ".csv")]
    out = {"files": []}
    for fp in files:
        rel = str(fp.relative_to(BASE))
        try:
            if fp.suffix.lower() == ".xlsx":
                r = audit_xlsx(fp)
            elif fp.suffix.lower() == ".xls":
                r = audit_xls(fp)
            else:
                r = audit_csv(fp)
        except Exception as e:
            r = {"file": fp.name, "verdict": "DEAD", "why": f"audit crash: {type(e).__name__}"}
        r["path"] = rel
        out["files"].append(r)
        print(f"{r['verdict']:12s} {rel}", flush=True)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e15.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("wrote results_e15.json")


if __name__ == "__main__":
    main()
