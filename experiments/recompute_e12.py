"""Independent E12 recompute via src/gtk1 (not experiment copies): PK1 cuts >=12/>=15,
B1 AP + base + match + prev + lift CI. Compares against committed results_e12.json.
Read-only raw data.
"""
import json
import sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize
from gtk1.features import build
from gtk1.metrics import ap_lift_ci
import glob

OUT = Path(__file__).resolve().parent
SEC = REPO.parent / "Данные для предварительного изучения" / "Парабель-Кузбасс-1 (572-714)"
KMAX = 1400


def load(year):
    fs = sorted(glob.glob(str(SEC / str(year) / "*.xls*")))
    fp = next(f for f in fs if Path(f).name.startswith("Аномалии"))
    df, _ = load_anomalies(fp)
    return normalize(df)


def run():
    r22, r25 = load(2022), load(2025)
    out = {"cuts": {}}
    for cut in (12, 15):
        y, X, mr = build(r22, r25, cut, KMAX)
        b1 = X[:, 0] / max(X[:, 0].max(), 1)
        st = ap_lift_ci(y, b1, n=2000, seed=0)
        out["cuts"][str(cut)] = {"match": round(mr, 4), "prev": round(float(y.mean()), 4),
                                 "n_pos": int(y.sum()), "B1": round(st["AP"], 4),
                                 "base": round(st["base"], 4),
                                 "liftCI": [round(st["lift_CI"][0], 4), round(st["lift_CI"][1], 4)]}
    ref = json.loads((OUT / "results_e12.json").read_text())["cuts"]
    out["match_vs_committed"] = {
        c: {k: out["cuts"][c][k] == ref[c][k] for k in ("match", "prev", "B1", "base")} for c in ("12", "15")}
    out["verdict"] = ("IDENTICAL" if all(all(v.values()) for v in out["match_vs_committed"].values())
                      else "MISMATCH — investigate, do not overwrite")
    (OUT / "results_e12_recompute.json").write_text(json.dumps(out, indent=2))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    run()
