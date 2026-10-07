"""io: VTD anomaly loaders + row normalizer (consolidated from e05/e07/e11; behavior identical).
Supports .xlsx (openpyxl) + .xls (xlrd, with vendored tolerant patches for BIFF asserts).
"""
import logging
import warnings

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _apply_tolerant_xlrd():
    import xlrd
    from xlrd.sheet import Sheet
    if not getattr(Sheet.put_cell_unragged, "_gtk1_tolerant", False):
        _orig = Sheet.put_cell_unragged

        def tolerant_unragged(self, rowx, colx, ctype, value, xf_index):
            if ctype is None:
                try:
                    ctype = self._xf_index_to_xl_type_map[xf_index]
                except (KeyError, IndexError):
                    from xlrd.sheet import XL_CELL_NUMBER
                    ctype = XL_CELL_NUMBER
            try:
                return _orig(self, rowx, colx, ctype, value, xf_index)
            except AssertionError:
                if colx + 1 > self.utter_max_cols:
                    self.utter_max_cols = colx + 1
                if rowx + 1 > self.utter_max_rows:
                    self.utter_max_rows = rowx + 1
                return _orig(self, rowx, colx, ctype, value, xf_index)
            except (KeyError, IndexError):
                of = self.formatting_info
                self.formatting_info = False
                try:
                    return _orig(self, rowx, colx, ctype, value, 0)
                finally:
                    self.formatting_info = of

        tolerant_unragged._gtk1_tolerant = True  # idempotency guard: never double-wrap
        tolerant_unragged._gtk1_orig = _orig
        Sheet.put_cell_unragged = tolerant_unragged
    if getattr(Sheet.read, "_gtk1_tolerant", False):
        return
    _orig_read = Sheet.read

    def tolerant_read(self, bk):
        orig_ss = bk._sharedstrings

        class SafeList(list):
            def __init__(self, *a, **kw):
                super().__init__(*a, **kw)
                self.bad_sst_hits = 0

            def __getitem__(self, i):
                try:
                    return super().__getitem__(i)
                except IndexError:
                    try:
                        key = int(i)
                    except Exception:
                        raise
                    self.bad_sst_hits += 1
                    return f"<BAD_SST_{key}>"

        safe = SafeList(orig_ss if orig_ss is not None else [])
        bk._sharedstrings = safe
        try:
            return _orig_read(self, bk)
        finally:
            n_bad = int(getattr(safe, "bad_sst_hits", 0))
            if n_bad:
                logger.warning("tolerant xlrd: %d <BAD_SST_*> hits", n_bad)
                warnings.warn(f"tolerant xlrd: {n_bad} <BAD_SST_*> hits",
                              UserWarning, stacklevel=2)

    tolerant_read._gtk1_tolerant = True  # idempotency guard: never double-wrap
    tolerant_read._gtk1_orig = _orig_read
    Sheet.read = tolerant_read


def load_anomalies(path, sheet="Аномалии", header=3):
    """Read one anomaly sheet. Returns (df, meta). Tries stock engine, then tolerant-xlrd."""
    from pathlib import Path
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"load_anomalies: file not found: {p}")
    if not p.is_file():
        raise FileNotFoundError(f"load_anomalies: not a file: {p}")
    eng = "openpyxl" if p.suffix == ".xlsx" else "xlrd"
    try:
        df = pd.read_excel(p, sheet_name=sheet, header=header, engine=eng)
    except (FileNotFoundError, OSError) as e:
        raise FileNotFoundError(f"load_anomalies: file not found or unreadable: {p}: {e}") from e
    except ValueError as e:
        raise ValueError(
            f"load_anomalies: missing sheet/header — sheet={sheet!r} header={header} in {p.name}: {e}"
        ) from e
    except Exception:
        # BIFF/assert path only: retry once with tolerant xlrd patches.
        _apply_tolerant_xlrd()
        try:
            df = pd.read_excel(p, sheet_name=sheet, header=header, engine="xlrd")
        except (FileNotFoundError, OSError) as e:
            raise FileNotFoundError(f"load_anomalies: file not found or unreadable: {p}: {e}") from e
        except ValueError as e:
            raise ValueError(
                f"load_anomalies: missing sheet/header — sheet={sheet!r} header={header} in {p.name}: {e}"
            ) from e
    df.columns = [str(c).strip() for c in df.columns]
    return df, {"name": p.name, "bytes": p.stat().st_size, "mtime": p.stat().st_mtime}


def _find(df, *keys):
    return next((c for c in df.columns if all(k.lower() in c.lower() for k in keys)), None)


def normalize(df, width_m=100, kmax=None):
    """Row filter prep: dist/pipe/depth/off/orient/char + corr flag + hour + cell. No depth cut here."""
    cd = _find(df, "расстояние")
    cc = _find(df, "глубина")
    cp = _find(df, "номер", "трубы")
    co = _find(df, "левого", "начала") or _find(df, "левого")
    cr = _find(df, "ориентация", "максимума") or _find(df, "ориентация", "центра")
    ch_cands = [c for c in df.columns if "характер" in c.lower()]
    if cd is None:
        raise ValueError(f"normalize: missing required column containing 'расстояние' (have {list(df.columns)})")
    if cc is None:
        raise ValueError(f"normalize: missing required column containing 'глубина' (have {list(df.columns)})")
    if cp is None:
        raise ValueError(f"normalize: missing required column containing 'номер'+'трубы' (have {list(df.columns)})")
    if not ch_cands:
        raise ValueError(f"normalize: missing required column containing 'характер' (have {list(df.columns)})")
    ch = ch_cands[0]
    ca = [c for c in df.columns if "характер" in c.lower() and "аббр" in c.lower()]
    ca = ca[0] if ca else None
    o = pd.DataFrame({
        "dist": pd.to_numeric(df[cd], errors="coerce"),
        "depth": pd.to_numeric(df[cc], errors="coerce"),
        "pipe": df[cp].astype(str).str.strip().str.replace(r"\.0$", "", regex=True),
        "off": pd.to_numeric(df[co], errors="coerce") if co else float("nan"),
        "ori": df[cr].astype(str) if cr else "",
        "char": df[ch].astype(str),
        "abbr": df[ca].astype(str) if ca else "",
    }).dropna(subset=["dist"]).copy()
    if len(o):
        arr = o["dist"].to_numpy(dtype=float)
        bad_fin = ~np.isfinite(arr)
        n_bad = int(bad_fin.sum())
        if n_bad:
            share = n_bad / len(arr)
            logger.warning("normalize: %d/%d non-finite dist dropped (share=%.4f)", n_bad, len(arr), share)
            warnings.warn(f"normalize: {n_bad}/{len(arr)} non-finite dist dropped (share={share:.4f})",
                          UserWarning, stacklevel=2)
            o = o.loc[~bad_fin].copy()
            arr = o["dist"].to_numpy(dtype=float) if len(o) else np.array([], dtype=float)
        if len(arr):
            n_neg = int((arr < 0).sum())
            if n_neg:
                share = n_neg / len(arr)
                logger.warning("normalize: %d/%d negative dist kept (share=%.4f); will clip to cell 0",
                               n_neg, len(arr), share)
                warnings.warn(f"normalize: {n_neg}/{len(arr)} negative dist (share={share:.4f})",
                              UserWarning, stacklevel=2)
            if kmax is not None:
                n_over = int(((arr // width_m) > kmax).sum())
                if n_over or n_neg:
                    logger.warning("normalize: clipped cells: negative=%d overrun(>%d)=%d n=%d",
                                   n_neg, kmax, n_over, len(arr))
    o["corr"] = o["char"].str.contains("оррози", na=False)
    o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    if kmax is not None:
        o["cell"] = (o["dist"] // width_m).astype(int).clip(0, kmax)
    return o
