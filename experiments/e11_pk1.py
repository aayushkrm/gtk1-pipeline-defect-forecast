"""E11: PK1 2022->2025 replication (frozen pipeline, densest generalization test).
2025A .xls needs BIFF-tolerant xlrd patches (vendored below from prior salvage work in
/tmp T/opencode tolerant.py — same utter_max + bad-SST patches, read-only use).
Frozen: Depth>=10%, match pipe+2m/0.5m/1h greedy, 100m matched-new (KMAX=1400),
B1/B2 + bootstrap lift CI. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd

# --- vendored tolerant-xlrd patches (prior salvage work, attributed) ---
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
    import xlrd.sheet as sheetmod
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

sys.path.insert(0, str(Path(__file__).resolve().parent))
from e04b_robust import match_win
from e07b_null import build
from e07_ablation import raw
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
SEC = REPO.parent / "Данные для предварительного изучения" / "Парабель-Кузбасс-1 (572-714)"
KMAX = 1400

def load(year):
    import glob
    fs = sorted(glob.glob(str(SEC / str(year) / "*.xls*")))
    cands = [f for f in fs if Path(f).name.startswith("Аномалии")]
    assert cands, f"no anomaly file in {SEC / str(year)}"
    fp = cands[0]
    eng = "openpyxl" if fp.endswith(".xlsx") else "xlrd"
    try:
        df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine=eng)
    except Exception:
        _apply_tolerant_xlrd()
        df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine="xlrd")
    df.columns = [str(c).strip() for c in df.columns]
    return df, {"name": Path(fp).name, "bytes": Path(fp).stat().st_size}

def run():
    raws, hashes = {}, []
    for y in (2022, 2025):
        df, h = load(y)
        raws[y] = raw(df)
        hashes.append(h)
    y, X, mr = build(raws[2022], raws[2025], 10, KMAX)
    b1 = X[:, 0] / max(X[:, 0].max(), 1)
    base = float(y.mean())
    ap = float(average_precision_score(y, b1)) if y.sum() else 0.0
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(y), len(y))
        if y[i].sum() > 0:
            bs.append(float(average_precision_score(y[i], b1[i]) - y[i].mean()))
    out = {"files": hashes,
           "counts": {str(y): int((raws[y]["depth"] >= 10).sum()) for y in (2022, 2025)},
           "match_rate": mr, "prev": base, "n_pos": int(y.sum()), "n_cells": KMAX + 1,
           "B1_AP": ap, "base": base,
           "lift_CI95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh, "loader": "tolerant-xlrd vendored for 2025A" if "2025" in str(hashes) else "xlrd"}
    (OUT / "results_e11.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E11 PK1 2022->2025 replication (frozen, Depth>=10, 100m matched-new)",
         f"counts d>=10: {out['counts']} match={mr:.3f} prev={base:.3f} pos={y.sum()}/{KMAX+1} "
         f"B1={ap:.3f} base={base:.3f} liftCI=[{out['lift_CI95'][0]:.3f},{out['lift_CI95'][1]:.3f}]"]
    (OUT / "results_e11.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
