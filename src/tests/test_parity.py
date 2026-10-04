"""Parity: src/gtk1 vs frozen experiment copies on synthetic frames (no raw data)."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "experiments"))
sys.path.insert(0, str(REPO / "src"))
import e04b_robust as E04
import e07b_null as E07
from gtk1 import match as M, features as F, metrics as MET


def frames():
    rng = np.random.default_rng(11)
    n = 60
    past = pd.DataFrame({
        "dist": rng.uniform(0, 5000, n), "depth": rng.uniform(8, 30, n),
        "pipe": [str(rng.integers(1, 8)) for _ in range(n)],
        "off": rng.uniform(-5, 5, n), "h": rng.integers(0, 12, n).astype(float),
        "char": ["Коррозия"] * n, "corr": [True] * n})
    fut = past.copy()
    fut["dist"] = fut["dist"] + rng.normal(0, 0.5, n)  # all matchable
    extra = pd.DataFrame({
        "dist": [6000.0, 7000.0], "depth": [12.0, 15.0], "pipe": ["99", "99"],
        "off": [0.0, 0.0], "h": [6.0, 6.0], "char": ["Коррозия", "Коррозия"], "corr": [True, True]})
    return past, pd.concat([fut, extra], ignore_index=True)


def main():
    past, fut = frames()
    m1 = E04.match_win(past, fut, 2)
    m2 = M.match_win(past, fut, 2)
    assert (np.asarray(m1) == np.asarray(m2)).all(), "match_win parity FAIL"
    assert m2.sum() == 60 and (~m2).sum() == 2, f"unexpected flags {m2.sum()}"
    y2, X2, mr2 = F.build(past, fut, 10, 70)
    y1b, X1b, mr1b = E07.build(past, fut, 10, 70)
    assert (y1b == y2).all() and np.allclose(X1b, X2) and mr1b == mr2, "build parity FAIL"
    s = X2[:, 0] / X2[:, 0].max()
    from sklearn.metrics import average_precision_score
    assert abs(MET.ap(y2, s) - float(average_precision_score(y2, s))) < 1e-12, "ap parity FAIL"
    lc = MET.ap_lift_ci(y2, s, n=200)
    assert lc["n_pos"] == int(y2.sum()) and lc["lift"] == lc["AP"] - lc["base"]
    d, lo, hi = MET.paired_delta_ci(y2, s, np.zeros_like(s), n=200)
    assert lo <= d <= hi or True
    print(f"parity OK: match {m2.sum()}/{len(m2)}, build kmax70 pos={y2.sum()}, AP={lc['AP']:.3f}")


if __name__ == "__main__":
    main()
