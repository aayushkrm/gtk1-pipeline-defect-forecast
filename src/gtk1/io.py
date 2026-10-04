"""io: VTD anomaly loaders + row normalizer (consolidated from e05/e07/e11; behavior identical).
Supports .xlsx (openpyxl) + .xls (xlrd, with vendored tolerant patches for BIFF asserts).
"""
import re
import pandas as pd


def _apply_tolerant_xlrd():
    import xlrd
    from xlrd.sheet import Sheet
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

    Sheet.put_cell_unragged = tolerant_unragged
    _orig_read = Sheet.read

    def tolerant_read(self, bk):
        orig_ss = bk._sharedstrings

        class SafeList(list):
            def __getitem__(self, i):
                try:
                    return super().__getitem__(i)
                except IndexError:
                    return f"<BAD_SST_{i}>"

        bk._sharedstrings = SafeList(orig_ss)
        return _orig_read(self, bk)

    Sheet.read = tolerant_read


def load_anomalies(path, sheet="Аномалии", header=3):
    """Read one anomaly sheet. Returns (df, meta). Tries stock engine, then tolerant-xlrd."""
    from pathlib import Path
    p = Path(path)
    eng = "openpyxl" if p.suffix == ".xlsx" else "xlrd"
    try:
        df = pd.read_excel(p, sheet_name=sheet, header=header, engine=eng)
    except Exception:
        _apply_tolerant_xlrd()
        df = pd.read_excel(p, sheet_name=sheet, header=header, engine="xlrd")
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
    ch = [c for c in df.columns if "характер" in c.lower()][0]
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
    o["corr"] = o["char"].str.contains("оррози", na=False)
    o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    if kmax is not None:
        o["cell"] = (o["dist"] // width_m).astype(int).clip(0, kmax)
    return o
