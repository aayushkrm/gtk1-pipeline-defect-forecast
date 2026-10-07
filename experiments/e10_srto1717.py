"""E10: SRTO-1717 2016->2021 replication (frozen pipeline, external test).
KP 2016 'Аномалии' sheet + 2021A. Depth>=10%, match pipe+2m/0.5m/1h greedy,
100m matched-new, B1/B2/B3 + bootstrap lift CI. 2021 covers ~30km of 42km (flagged).
Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e04b_robust import match_win
from e07b_null import build
from e07_ablation import raw
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
SEC = REPO.parent / "Данные для предварительного изучения" / "СРТО-Омск_(1717-1759)"
KMAX = 420

def load(year, sheet="Аномалии"):
    import glob
    fs = sorted(glob.glob(str(SEC / str(year) / "*.xls*")))
    fp = next(f for f in fs if "Аномалии" in Path(f).name or "КП" in Path(f).name)
    df = pd.read_excel(fp, sheet_name=sheet, header=3,
                       engine="xlrd" if fp.endswith(".xls") else "openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    st = Path(fp).stat()
    return df, {"name": Path(fp).name, "bytes": st.st_size, "mtime": st.st_mtime}

def run():
    d16, h16 = load(2016)
    d21, h21 = load(2021)
    r16, r21 = raw(d16), raw(d21)
    y, X, mr = build(r16, r21, 10, KMAX)
    b1 = X[:, 0] / max(X[:, 0].max(), 1)
    base = float(y.mean())
    ap = float(average_precision_score(y, b1)) if y.sum() else 0.0
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(2000):
        i = rng.integers(0, len(y), len(y))
        if y[i].sum() > 0:
            bs.append(float(average_precision_score(y[i], b1[i]) - y[i].mean()))
    out = {"files": [h16, h21],
           "counts": {"2016": int((r16["depth"] >= 10).sum()), "2021": int((r21["depth"] >= 10).sum())},
           "match_rate": mr, "prev": base, "n_pos": int(y.sum()),
           "B1_AP": ap, "base": base, "lift_CI95": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e10.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E10 SRTO-1717 2016->2021 replication (frozen, Depth>=10, 100m matched-new)",
         f"counts d>=10: {out['counts']} match={mr:.3f} prev={base:.3f} pos={y.sum()} "
         f"B1={ap:.3f} base={base:.3f} liftCI=[{out['lift_CI95'][0]:.3f},{out['lift_CI95'][1]:.3f}]",
         "- caveat: 2021 covers ~30km of 42km; KP-2016 mixed provenance (2022 stamp)."]
    (OUT / "results_e10.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
