"""E09: spatial-block CV within ON (reviewer round-5 killer control).
Leave-contiguous-third-out on 1331 100m cells, cut>=10, frozen 7 feats, C frozen=1.0.
Per fold: fit LR on train-pair rows of 2/3 cells, eval Δ-vs-B1 on test-pair rows of held-out 1/3.
If nlag Δ collapses to <=0, the +0.03 is proximity/survey-streak leakage — dead even ON-only.
Boundary-cell neighbor leakage is conservative (inflates, so collapse = real death).
Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom
from e07b_null import build
from e07_ablation import raw
from sklearn.metrics import average_precision_score
from sklearn.linear_model import LogisticRegression

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    ytr, Xtr, _ = build(r16, r21, 10, 1330)
    yte, Xte, _ = build(r21, r25, 10, 1330)
    thirds = [np.arange(0, 443), np.arange(443, 887), np.arange(887, 1331)]
    rng = np.random.default_rng(3)
    folds = []
    for k, ho in enumerate(thirds):
        tr = np.setdiff1d(np.arange(1331), ho)
        lr = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr[tr], ytr[tr])
        s = lr.predict_proba(Xte[ho])[:, 1]
        b = Xte[ho][:, 0] / max(Xte[ho][:, 0].max(), 1)
        d0 = float(average_precision_score(yte[ho], s) - average_precision_score(yte[ho], b)) if yte[ho].sum() else 0.0
        bs = []
        for _ in range(500):
            i = rng.integers(0, len(ho), len(ho))
            if yte[ho][i].sum() > 0:
                bs.append(float(average_precision_score(yte[ho][i], s[i]) - average_precision_score(yte[ho][i], b[i])))
        folds.append({"held": [int(ho[0]), int(ho[-1])], "n_pos": int(yte[ho].sum()),
                      "LR_AP": float(average_precision_score(yte[ho], s)),
                      "B1_AP": float(average_precision_score(yte[ho], b)),
                      "delta": d0, "CI": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]})
    out = {"folds": folds}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e09.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E09 spatial-block CV (ON @100m, leave-contiguous-third-out, C=1.0 frozen)"]
    for f in folds:
        L.append(f"- cells {f['held']}: pos={f['n_pos']} LR={f['LR_AP']:.3f} B1={f['B1_AP']:.3f} "
                 f"d={f['delta']:+.3f}[{f['CI'][0]:+.3f},{f['CI'][1]:+.3f}]")
    (OUT / "results_e09.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
