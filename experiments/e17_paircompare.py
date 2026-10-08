"""e17_paircompare: paired simple-model comparison (Ayush+Aleksei track).

Train ON 2016->2021, test ON 2021->2025 + SRTO-1608 2021->2024.
Frozen R1 machinery: src.gtk1.features.build (7 FEATS, cut=10,
kmax 1330/1040), B1 = X[:,0] normalized, AP vs base + lift CI and
paired_delta_ci vs B1 via src.gtk1.metrics (docs/EVAL_SPEC.md).
Models (CPU only, sklearn==1.6.1, no new deps):
  HGB = HistGradientBoostingClassifier(early_stopping=False, random_state=0)
  RF  = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1)
  NOTE: n_jobs=-1 thread scheduling can break bit-reproducibility across machines;
  reruns on THIS machine reproduce exactly, cross-machine equality is not claimed.
Read-only raw data. Writes experiments/results_e17.json (aggregates only).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.features import FEATS, build
from gtk1.io import load_anomalies, normalize
from gtk1 import metrics as MET
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier

DATA_ROOT = REPO.parent / "Данные для предварительного изучения"
CUT = 10
KMAX_ON = 1330
KMAX_SRTO = 1040


def load_one(sdir, year, cands=None):
    d = DATA_ROOT / sdir / str(year)
    if cands is None:
        cands = sorted(p.name for p in d.glob("Аномалии*.xls*"))
        assert cands, f"no anomaly file in {d}"
    if isinstance(cands, (list, tuple)):
        fp = next((d / n for n in cands if (d / n).exists()), None)
    else:
        fp = d / cands
    assert fp is not None and fp.exists(), f"no anomaly file in {d}"
    df, _ = load_anomalies(str(fp))
    return normalize(df)


def b1score(X):
    m = float(X[:, 0].max()) if len(X) else 1.0
    return X[:, 0] / max(m, 1.0)


def score_pair(y, s):
    r = MET.ap_lift_ci(y, s)
    return {"AP": r["AP"], "base": r["base"], "lift": r["lift"],
            "lift_CI": list(r["lift_CI"]), "n_pos": r["n_pos"], "n": r["n"]}


def clean(o):
    if isinstance(o, float) and o != o:
        return None
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def main():
    t0 = time.time()
    on16 = load_one("Омск-Новосибирск (392-526)", 2016, ("Аномалии.xlsx",))
    on21 = load_one("Омск-Новосибирск (392-526)", 2021, ("Аномалии.xlsx",))
    on25 = load_one("Омск-Новосибирск (392-526)", 2025,
                    ("Аномалии.xlsx", "Аномалии_.xlsx"))
    sr21 = load_one("СРТО-Омск_(1608 – 1717)", 2021, ("Аномалии.xls",))
    sr24 = load_one("СРТО-Омск_(1608 – 1717)", 2024,
                    ("Аномалии.xls", "Аномалии1.xls"))
    ytr, Xtr, mr_tr = build(on16, on21, CUT, KMAX_ON)
    y_on, X_on, mr_on = build(on21, on25, CUT, KMAX_ON)
    y_sr, X_sr, mr_sr = build(sr21, sr24, CUT, KMAX_SRTO)
    assert Xtr.shape[1] == 7 and list(FEATS) == [
        "n_past", "nlag", "maxd", "meand", "gwan", "mech", "npipes"]
    hgb = HistGradientBoostingClassifier(early_stopping=False, random_state=0)
    rf = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1)
    hgb.fit(Xtr, ytr)
    rf.fit(Xtr, ytr)
    out = {"train": "ON 2016->2021", "cut": CUT, "features": list(FEATS),
           "models": {"HGB": {"early_stopping": False, "random_state": 0},
                      "RF": {"n_estimators": 200, "random_state": 0, "n_jobs": -1}},
           "train_stats": {"n_pos": int(ytr.sum()), "n": len(ytr),
                           "prev": float(ytr.mean()), "match_rate": float(mr_tr)},
           "pairs": {}}
    for name, y, X, mr in (("ON 2021->2025", y_on, X_on, mr_on),
                           ("SRTO-1608 2021->2024", y_sr, X_sr, mr_sr)):
        sb = b1score(X)
        sh = hgb.predict_proba(X)[:, 1]
        sr = rf.predict_proba(X)[:, 1]
        rb, rh, rr = score_pair(y, sb), score_pair(y, sh), score_pair(y, sr)
        dh, lh, hh = MET.paired_delta_ci(y, sh, sb)
        dr, lr, hr = MET.paired_delta_ci(y, sr, sb)
        out["pairs"][name] = {
            "n_pos": int(y.sum()), "n": len(y), "prev": float(y.mean()),
            "match_rate": float(mr),
            "B1": {"AP": rb["AP"], "base": rb["base"], "lift_CI": rb["lift_CI"]},
            "HGB": {"AP": rh["AP"], "base": rh["base"], "lift_CI": rh["lift_CI"]},
            "RF": {"AP": rr["AP"], "base": rr["base"], "lift_CI": rr["lift_CI"]},
            "delta_HGB_minus_B1": [float(dh), float(lh), float(hh)],
            "delta_RF_minus_B1": [float(dr), float(lr), float(hr)],
        }
        p = out["pairs"][name]
        print(f"{name}: n_pos={p['n_pos']} base={p['B1']['base']:.4f} "
              f"B1={p['B1']['AP']:.4f} HGB={p['HGB']['AP']:.4f} RF={p['RF']['AP']:.4f} "
              f"dHGB={dh:+.4f} [{lh:+.4f},{hh:+.4f}] dRF={dr:+.4f} [{lr:+.4f},{hr:+.4f}]")
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    out["runtime_s"] = float(time.time() - t0)
    (Path(__file__).resolve().parent / "results_e17.json").write_text(
        json.dumps(clean(out), indent=2, ensure_ascii=False))
    print(f"runtime_s={out['runtime_s']:.1f}")


if __name__ == "__main__":
    main()
