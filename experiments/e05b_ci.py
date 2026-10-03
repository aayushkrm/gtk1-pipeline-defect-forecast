"""E05b: reviewer's single number — 95% bootstrap CI on SRTO test lift (B1 AP minus base).
Frozen pipeline, no tuning. 2000 cell-resamples (cheap, n=1041). Read-only raw data.
"""
import json
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e05_srto import load_any, norm, SEC, W, KMAX
from e04b_robust import match_win
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent

def pair_labels(years):
    gs = {}
    for y in years:
        df, _ = load_any(y)
        gs[y] = norm(df)
    cells = {}
    for tag, a, b in (("train", years[0], years[1]), ("test", years[1], years[2])):
        gp, gf = gs[a], gs[b]
        m = match_win(gp, gf, 2)
        new = gf[~m]; new = new[new["corr"]]
        ck = lambda g: (g["dist"] // W).astype(int).clip(0, KMAX)
        y = (new.groupby(ck(new)).size().reindex(range(KMAX + 1), fill_value=0).values > 0).astype(int)
        past = (gp[gp["corr"]].groupby(ck(gp[gp["corr"]])).size()
                .reindex(range(KMAX + 1), fill_value=0).values.astype(float))
        cells[tag] = (y, past / max(past.max(), 1), float(m.mean()))
    return cells

def run():
    cells = pair_labels((2016, 2021, 2024))
    rng = np.random.default_rng(0)
    out = {}
    L = ["# E05b SRTO lift CIs (frozen, 2000 bootstraps)"]
    for tag, (y, s, mr) in cells.items():
        ap = float(average_precision_score(y, s))
        base = float(y.mean())
        bs = []
        for _ in range(2000):
            i = rng.integers(0, len(y), len(y))
            if y[i].sum() > 0:
                bs.append(average_precision_score(y[i], s[i]) - y[i].mean())
        lo, hi = float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
        out[tag] = {"AP": ap, "base": base, "lift": ap - base, "lift_CI95": [lo, hi], "n_pos": int(y.sum())}
        L.append(f"- {tag}: AP={ap:.3f} base={base:.3f} lift={ap-base:.3f} CI95=[{lo:.3f},{hi:.3f}] pos={y.sum()}")
    (OUT / "results_e05b.json").write_text(json.dumps(out, indent=2))
    (OUT / "results_e05b.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
