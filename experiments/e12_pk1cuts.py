"""E12: PK1 cut-sensitivity >=12/>=15 (unblocks PK1 quantitative headline; reviewer round 8).
Frozen pipeline, B1 AP + base + match + prev + 2000-bootstrap lift CI per cut.
De-identified aggregates only. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e11_pk1 import load
from e07b_null import build
from e07_ablation import raw
from sklearn.metrics import average_precision_score

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
KMAX = 1400

def run():
    d22, _ = load(2022); d25, _ = load(2025)
    r22, r25 = raw(d22), raw(d25)
    out = {"cuts": {}}
    rng = np.random.default_rng(0)
    for cut in (12, 15):
        y, X, mr = build(r22, r25, cut, KMAX)
        b1 = X[:, 0] / max(X[:, 0].max(), 1)
        base = float(y.mean())
        ap = float(average_precision_score(y, b1)) if y.sum() else 0.0
        bs = []
        for _ in range(2000):
            i = rng.integers(0, len(y), len(y))
            if y[i].sum() > 0:
                bs.append(float(average_precision_score(y[i], b1[i]) - y[i].mean()))
        out["cuts"][str(cut)] = {"match": mr, "prev": base, "n_pos": int(y.sum()),
                                  "B1": ap, "base": base,
                                  "liftCI": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e12.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E12 PK1 cut-sensitivity (frozen, 100m matched-new)"]
    for cut in ("12", "15"):
        v = out["cuts"][cut]
        L.append(f"- cut>={cut}%: match={v['match']:.3f} prev={v['prev']:.3f} pos={v['n_pos']} "
                 f"B1={v['B1']:.3f} base={v['base']:.3f} liftCI=[{v['liftCI'][0]:.3f},{v['liftCI'][1]:.3f}]")
    (OUT / "results_e12.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
