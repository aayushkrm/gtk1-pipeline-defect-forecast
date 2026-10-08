"""Tuesday partner-drop ingestion stub (schema-tolerant, CPU only, read-only raw data).

Covers unknown-schema Tuesday files: pipe characteristics + per-section tool info.
Frozen R1 pipeline untouched (import from src.gtk1.io only, no edits there).

Steps:
  1. Generic table reader: CSV (comma/semicolon) then Excel (sheet list logged,
     first non-empty sheet with a pipe hit, header rows 0..3 auto-pick).
  2. Pipe-key discovery via imported src.gtk1.io._find (not copied).
  3. Join-coverage report: share of new pipe keys in reference frame + vice versa.
  4. Column inventory + per-column non-empty shares (aggregates only).
  5. Tool-info normalizer: free-form lines into {section, tool, role} rows.

Self-test uses existing files as proxies (read-only):
  ON-2021 weld log vs ON-2021 anomalies; PK1-2025 weld log vs PK1-2025 anomalies.
Writes experiments/results_ingest_selftest.json (aggregates only, NaN->null).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
OUT = Path(__file__).resolve().parent
BASE = REPO.parent / "Данные для предварительного изучения"

sys.path.insert(0, str(REPO / "src"))
from gtk1.io import _apply_tolerant_xlrd, _find  # noqa: E402  (reuse, do not copy)

EXCEL_SUFFIX = (".xls", ".xlsx")


# --- (1) generic table reader ------------------------------------------------
def _looks_mojibake(cols):
    """True when headers show double-decoding artifacts (cp1251 read of UTF-8 bytes)."""
    return any("Рќ" in str(c) or "Ð" in str(c) or "Ã" in str(c) for c in cols)


def _read_csv(path):
    last = None
    for enc in ("utf-8-sig", "cp1251"):
        for sep in (",", ";"):
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, engine="python")
                if len(df.columns) > 1 or sep == ";":
                    if enc == "cp1251":
                        df.columns = [str(c).strip() for c in df.columns]
                        if _looks_mojibake(df.columns):
                            last = ValueError("cp1251 decode looks like mojibake; retrying tolerant utf-8")
                            break  # out of sep loop -> tolerant fallback below
                    return df, {"loader": f"csv/{enc}/sep={sep!r}"}
                last = (df, {"loader": f"csv/{enc}/sep={sep!r}"})
            except Exception as e:  # try next encoding/sep
                last = e
        else:
            continue
        break
    if isinstance(last, tuple):
        return last
    # Final tier: single bad bytes (RedOS flash corruption) must not sink the file.
    import io as _io
    import warnings
    raw = Path(path).read_bytes()
    for sep in (",", ";"):
        try:
            text = raw.decode("utf-8-sig", errors="replace")
            df = pd.read_csv(_io.StringIO(text), sep=sep, engine="python")
            if len(df.columns) > 1 or sep == ";":
                warnings.warn(f"csv tolerated bad bytes via utf-8/replace: {path.name}",
                              UserWarning, stacklevel=2)
                return df, {"loader": f"csv/utf-8-sig-replace/sep={sep!r}",
                            "warning": "tolerated-bad-bytes"}
        except Exception as e:
            last = e
    raise ValueError(f"csv unreadable: {Path(path).name}: {last}")


def _apply_fat_salvage():
    """Last-resort retry tier for truncated OLE (.xls with short FAT chain).

    Technique adapted from experiments/salvage_pk1_weld.py (same idea, local
    form). Joins surviving FAT slices instead of raising CompDocError.
    Read-only use. Idempotent.
    """
    import xlrd.compdoc as C
    if getattr(C.CompDoc._locate_stream, "_tuesday_salvage", False):
        return
    _orig = C.CompDoc._locate_stream

    def tolerant_locate(self, mem, base, sat, sec_size, start_sid,
                        expected_stream_size, qname, seen_id):
        from xlrd.compdoc import CompDocError
        try:
            return _orig(self, mem, base, sat, sec_size, start_sid,
                         expected_stream_size, qname, seen_id)
        except (CompDocError, AssertionError):
            pass
        s, p, slices, tot = start_sid, -99, [], 0
        if s < 0:
            raise CompDocError("start_sid -ve")
        limit = (expected_stream_size + sec_size - 1) // sec_size
        start_pos, end_pos = -9999, -8888
        while s >= 0:
            self.seen[s] = seen_id
            tot += 1
            if tot > limit:
                raise CompDocError("size exceeds expected")
            if s == p + 1:
                end_pos += sec_size
            else:
                if p >= 0:
                    slices.append((start_pos, end_pos))
                start_pos = base + s * sec_size
                end_pos = start_pos + sec_size
            p = s
            s = sat[s] if s < len(sat) else -2
        if not slices:
            return (mem, start_pos, tot * sec_size)
        slices.append((start_pos, end_pos))
        return (b"".join(mem[a:b] for a, b in slices), 0, tot * sec_size)

    tolerant_locate._tuesday_salvage = True
    C.CompDoc._locate_stream = tolerant_locate


def _sheet_names(path, engine):
    xl = pd.ExcelFile(path, engine=engine)
    names = list(xl.sheet_names)
    xl.close()
    return names


def _sheet_empty(path, sheet, engine):
    try:
        probe = pd.read_excel(path, sheet_name=sheet, header=None,
                              nrows=20, engine=engine)
    except Exception:
        return True
    if probe.empty:
        return True
    return bool(probe.dropna(how="all").empty)


def _score_header(df):
    """Hit score: pipe column found (1/0). Uses imported _find rules."""
    col, _ = discover_pipe_key(df)
    return 1 if col is not None else 0


def _read_excel(path):
    engine = "openpyxl" if path.suffix.lower() == ".xlsx" else "xlrd"
    tiers = ["stock", "tolerant-xlrd", "fat-salvage"]
    last = None
    for tier in tiers:
        try:
            if tier == "tolerant-xlrd":
                _apply_tolerant_xlrd()
            elif tier == "fat-salvage":
                _apply_tolerant_xlrd()
                _apply_fat_salvage()
            sheets = _sheet_names(path, engine)
            best = None  # (hit, sheet, header, df_probe)
            first_nonempty = None
            for sh in sheets:
                if _sheet_empty(path, sh, engine):
                    continue
                if first_nonempty is None:
                    first_nonempty = sh
                for h in range(4):
                    try:
                        probe = pd.read_excel(path, sheet_name=sh, header=h,
                                              nrows=8, engine=engine)
                    except Exception:
                        continue
                    probe.columns = [str(c).strip() for c in probe.columns]
                    hit = _score_header(probe)
                    if best is None or hit > best[0]:
                        best = (hit, sh, h, None)
                    if hit:
                        break
                if best is not None and best[0] == 1 and best[1] != sh:
                    pass
                if best is not None and best[0] == 1:
                    break
            if best is not None and best[0] == 1:
                _, sh, h, _ = best
            elif first_nonempty is not None:
                sh, h = first_nonempty, 0
            else:
                raise ValueError("no non-empty sheet")
            df = pd.read_excel(path, sheet_name=sh, header=h, engine=engine)
            df.columns = [str(c).strip() for c in df.columns]
            return df, {"loader": f"excel/{engine}/{tier}",
                        "sheets": sheets, "sheet": sh, "header": h,
                        "pipe_hit": bool(best is not None and best[0] == 1)}
        except Exception as e:
            last = f"{tier}: {type(e).__name__}: {str(e)[:120]}"
    raise ValueError(f"excel unreadable: {path.name}: {last}")


def read_generic_table(path):
    """Read CSV or Excel with unknown schema. Returns (df, meta). Read-only."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"read_generic_table: not a file: {path}")
    if path.suffix.lower() == ".csv":
        df, meta = _read_csv(path)
    elif path.suffix.lower() in EXCEL_SUFFIX:
        df, meta = _read_excel(path)
    else:
        raise ValueError(f"read_generic_table: unsupported suffix: {path.suffix}")
    df.columns = [str(c).strip() for c in df.columns]
    meta = {"file": path.name, "bytes": path.stat().st_size, **meta,
            "shape": [int(df.shape[0]), int(df.shape[1])]}
    return df, meta


# --- (2) pipe-key discovery ---------------------------------------------------
def discover_pipe_key(df):
    """Find pipe-id column via substring rules. Returns (col, rule).
    Rule order is precision-first: Cyrillic номер+трубы, Latin-N variant
    (salvage sheets use 'N\\nтрубы'), then bare fallbacks."""
    col = _find(df, "номер", "трубы")
    if col is not None:
        return col, "номер+трубы"
    col = _find(df, "n", "трубы")
    if col is not None:
        return col, "n+трубы(latin-N)"
    for key in ("труба", "pipe"):
        col = _find(df, key)
        if col is not None:
            return col, key
    return None, None


def pipe_key_set(df, col):
    """Normalized pipe-key set. Drops empties (aggregates only downstream)."""
    s = df[col].astype(str).str.strip().str.replace(r"\.0$", "", regex=True)
    s = s.str.strip()
    s = s[(s != "") & (s.str.lower() != "nan")]
    return set(s.tolist())


# --- (3) join-coverage report --------------------------------------------------
def join_coverage(new_keys, ref_keys):
    inter = set(new_keys) & set(ref_keys)
    n_new, n_ref = len(new_keys), len(ref_keys)
    return {"n_new": n_new, "n_ref": n_ref, "n_both": len(inter),
            "new_in_ref": (len(inter) / n_new) if n_new else None,
            "ref_in_new": (len(inter) / n_ref) if n_ref else None}


# --- (4) column inventory ------------------------------------------------------
def column_inventory(df):
    """Per-column non-empty shares. Aggregates only, no row data."""
    n = len(df)
    inv = {"n_rows": int(n), "n_cols": int(df.shape[1]), "columns": {}}
    for c in df.columns:
        col = df[c]
        if col.dtype == object:
            nonempty = col.notna() & (col.astype(str).str.strip() != "")
        else:
            nonempty = col.notna()
        k = int(nonempty.sum())
        inv["columns"][str(c)] = {"n_non_empty": k,
                                  "non_empty_share": (k / n) if n else None}
    return inv


# --- (5) tool-info normalizer ---------------------------------------------------
_TOOL_RE = re.compile(
    r"^\s*(?P<fam>[A-Za-zА-Яа-яЁё]+[0-9]*[A-Za-zА-Яа-яЁё]*)"
    r"[\s\-_./]+(?P<dn>\d{3,4})[\s\-_./xх]+(?P<ns>\d{2,5})\s*$"
)
_TOOL_SEARCH_RE = re.compile(
    r"(?P<fam>[A-Za-zА-Яа-яЁё]+[0-9]*[A-Za-zА-Яа-яЁё]*)"
    r"[\s\-_./]+(?P<dn>\d{3,4})[\s\-_./xх]+(?P<ns>\d{2,5})"
)


def normalize_tool_info(lines, section):
    """Free-form per-section tool lines into {section, tool, role} rows.

    Regex reads family letters + diameter digits + sensor digits
    (e.g. 'ДМТ2Б-1200-2560' -> fam=ДМТ2Б dn=1200 ns=2560).
    role = family slug when matched, else 'unresolved' bucket. Best-effort.
    """
    rows = []
    for raw in lines:
        tool = "" if raw is None else str(raw).strip()
        m = _TOOL_RE.match(tool) if tool else None
        if m is None and tool:
            # Section-prefixed or tabular lines ("Омск 2021: ДМТ2Б-1200-2560"):
            # scan for the tool token anywhere, store the token itself.
            m = _TOOL_SEARCH_RE.search(tool)
        if m:
            tok = m.group(0).strip()
            rows.append({"section": str(section), "tool": tok,
                         "role": m.group("fam").lower(),
                         "dn_mm": int(m.group("dn")),
                         "n_sensors": int(m.group("ns"))})
        else:
            rows.append({"section": str(section), "tool": tool,
                         "role": "unresolved", "dn_mm": None,
                         "n_sensors": None})
    return rows


# --- self-test -----------------------------------------------------------------
def _sanitize(o):
    if isinstance(o, dict):
        return {k: _sanitize(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_sanitize(v) for v in o]
    if isinstance(o, float) and (np.isnan(o) or np.isinf(o)):
        return None
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    return o


def _selftest_pair(new_path, ref_path):
    rec = {"new_file": Path(new_path).name, "ref_file": Path(ref_path).name,
           "load_error": None}
    try:
        new_df, new_meta = read_generic_table(new_path)
        ref_df, ref_meta = read_generic_table(ref_path)
        rec["new_meta"] = new_meta
        rec["ref_meta"] = ref_meta
        print(f"sheets new {new_path.name}: {new_meta.get('sheets')}")
        print(f"sheets ref {ref_path.name}: {ref_meta.get('sheets')}")
        new_col, new_rule = discover_pipe_key(new_df)
        ref_col, ref_rule = discover_pipe_key(ref_df)
        rec["new_pipe_col"], rec["new_pipe_rule"] = new_col, new_rule
        rec["ref_pipe_col"], rec["ref_pipe_rule"] = ref_col, ref_rule
        if new_col is None or ref_col is None:
            rec["load_error"] = (
                f"no pipe key: new={new_col} ref={ref_col}")
            rec.update({"n_new": None, "n_ref": None, "n_both": None,
                        "new_in_ref": None, "ref_in_new": None})
            return rec, None
        cov = join_coverage(pipe_key_set(new_df, new_col),
                            pipe_key_set(ref_df, ref_col))
        rec.update(cov)
        return rec, column_inventory(new_df)
    except Exception as e:
        rec["load_error"] = f"{type(e).__name__}: {str(e)[:200]}"
        rec.update({"n_new": None, "n_ref": None, "n_both": None,
                    "new_in_ref": None, "ref_in_new": None})
        return rec, None


def main():
    pairs = {
        "on2021": (BASE / "Омск-Новосибирск (392-526)" / "2021"
                   / "Поперечные сварные швы.xls",
                   BASE / "Омск-Новосибирск (392-526)" / "2021" / "Аномалии.xlsx"),
        "pk1_2025": (BASE / "Парабель-Кузбасс-1 (572-714)" / "2025"
                     / "Поперечные сварные швы.xls",
                     BASE / "Парабель-Кузбасс-1 (572-714)" / "2025" / "Аномалии.xls"),
    }
    out = {"pairs": {}, "inventories": {}, "tool_normalizer_selftest": {}}
    for name, (new_p, ref_p) in pairs.items():
        rec, inv = _selftest_pair(new_p, ref_p)
        out["pairs"][name] = rec
        if inv is not None:
            out["inventories"][f"{name}_new"] = inv
        print(f"[{name}] new_in_ref={rec.get('new_in_ref')} "
              f"ref_in_new={rec.get('ref_in_new')} "
              f"n_new={rec.get('n_new')} n_ref={rec.get('n_ref')} "
              f"err={rec.get('load_error')}")
    demo_lines = ["ДМТ2Б-1200-2560", "ДКК-1400-512", "  дмт-1200-1024 ",
                  "калибр 1200", "", "???"]
    rows = normalize_tool_info(demo_lines, "SELFTEST")
    n_ok = sum(1 for r in rows if r["role"] != "unresolved")
    out["tool_normalizer_selftest"] = {
        "n_lines": len(rows), "n_matched": n_ok,
        "n_unresolved": len(rows) - n_ok, "rows": rows}
    print(f"[tool] matched={n_ok}/{len(rows)} "
          f"unresolved={len(rows) - n_ok}/{len(rows)}")
    assert n_ok >= 2, "tool normalizer must match digit-coded lines"
    assert (len(rows) - n_ok) >= 1, "tool normalizer must keep unresolved bucket"
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short",
                             "HEAD"], capture_output=True, text=True)
        gh = gh.stdout.strip() or "nogit"
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh, "cpu_only": True,
                    "reader": "csv(sep ,/;) then excel(stock/tolerant/fat-salvage)",
                    "note": "tolerant/fat patches are process-global once applied; "
                            "a later file can succeed on its 'stock' attempt "
                            "via an earlier file's patch (loader tier = attempt order)"}
    out = _sanitize(out)
    (OUT / "results_ingest_selftest.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print("wrote results_ingest_selftest.json")


if __name__ == "__main__":
    main()
