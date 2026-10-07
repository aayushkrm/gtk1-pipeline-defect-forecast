"""Recompute pass: (a) NN odometer match rates ON 25->21, 21->16 at ±1/2/5m, raw + Depth>=10;
(b) E05 test-pair B1 AP recompute (frozen); (c) E10 B1 AP recompute (frozen).
E14 skipped honestly (repaired source lost to /tmp purge). Read-only raw data.
"""
import json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "experiments"))
sys.path.insert(0, str(REPO / "src"))
from e02_matched import load_anom, norm
from e05_srto import load_any, norm as norm_s, SEC as SEC58, KMAX as KMAX58
from e10_srto1717 import load as load17
from gtk1.features import build as _b  # noqa (documents src parity; runs use frozen module fns below)
from e07b_null import build
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent


def nn_rate(fut_d, past_d, win):
    p = np.sort(np.asarray(past_d, float))
    f = np.asarray(fut_d, float)
    idx = np.searchsorted(p, f)
    best = np.full(len(f), np.inf)
    m = idx < len(p)
    best[m] = np.abs(p[idx[m]] - f[m])
    m2 = idx > 0
    best[m2] = np.minimum(best[m2], np.abs(p[idx[m2] - 1] - f[m2]))
    return float((best <= win).mean())


def run():
    out = {"nn_rates": {}, "ap_recompute": {}}
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    g16, g21, g25 = norm(d16), norm(d21), norm(d25)
    for tag, gf, gp in (("25->21", g25, g21), ("21->16", g21, g16)):
        for win in (1, 2, 5):
            out["nn_rates"][f"{tag}_raw_pm{win}m"] = round(nn_rate(gf["dist"], gp["dist"], win), 4)
    for cutnm, gf, gp in (("25->21_d10", g25[g25["depth"] >= 10], g21[g21["depth"] >= 10]),
                          ("21->16_d10", g21[g21["depth"] >= 10], g16[g16["depth"] >= 10])):
        for win in (1, 2, 5):
            out["nn_rates"][f"{cutnm}_pm{win}m"] = round(nn_rate(gf["dist"], gp["dist"], win), 4)
    # E05 test recompute via frozen e05 pipeline pieces
    from e05_srto import match_win as _m58
    import e05_srto as E05
    f21, f24 = {}, {}
    for y in (2016, 2021, 2024):
        df, _ = load_any(y)
        f21[y] = norm_s(df)
    for tag, gp, gf, kmax in (("E05_train16-21", f21[2016], f21[2021], KMAX58),
                              ("E05_test21-24", f21[2021], f21[2024], KMAX58)):
        y, X, mr = build(gp, gf, 10, kmax)
        b1 = X[:, 0] / max(X[:, 0].max(), 1)
        ap = float(average_precision_score(y, b1)) if y.sum() else 0.0
        out["ap_recompute"][tag] = {"AP": round(ap, 4), "base": round(float(y.mean()), 4),
                                    "match": round(mr, 4), "pos": int(y.sum())}
    # E10 recompute
    d16x, _ = load17(2016); d21x, _ = load17(2021)
    from e07_ablation import raw
    r16, r21 = raw(d16x), raw(d21x)
    y, X, mr = build(r16, r21, 10, 420)
    b1 = X[:, 0] / max(X[:, 0].max(), 1)
    ap = float(average_precision_score(y, b1)) if y.sum() else 0.0
    out["ap_recompute"]["E10_16-21"] = {"AP": round(ap, 4), "base": round(float(y.mean()), 4),
                                       "match": round(mr, 4), "pos": int(y.sum())}
    (OUT / "results_recompute.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    run()
