"""E06: tuned-shrinkage control for the E03 count claim (reviewer round-2 item 3).
Question: is HGB-poisson MAE 8.52 vs mean 11.29 genuine discrimination or shrinkage?
Controls (all fit on TRAIN pair 16->21 only, evaluated on test 21->25, ON 1km matched-new counts):
 C1 tuned Poisson-GLM (alpha by 3-fold CV on train) — if it matches HGB, win was regularization.
 C2 log-linear Ridge (log1p, alpha CV on train).
 C3 residual-after-B1: HGB-poisson vs calibrated-B1 (linear map fit on train); report delta.
 C4 shuffle control: permuted Xtr -> HGB must fall to ~mean baseline (else pipeline bug).
 Seeds 0,1,2 for HGB. Metrics MAE/RMSE/Spearman on test. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom, norm, match, PARAMS
from e03_count import seg_new_counts, boot_spear
from sklearn.linear_model import PoissonRegressor, Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]

def cv_alpha_poisson(X, y, alphas=(0.01, 0.1, 1.0, 10.0)):
    kf = KFold(3, shuffle=True, random_state=0)
    best, bestm = alphas[0], 1e18
    for a in alphas:
        ms = []
        for tr, va in kf.split(X):
            m = PoissonRegressor(alpha=a, max_iter=1000).fit(X[tr], y[tr])
            p = np.clip(m.predict(X[va]), 0, None)
            ms.append(mean_absolute_error(y[va], p))
        if np.mean(ms) < bestm:
            best, bestm = a, float(np.mean(ms))
    return best

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    g16, g21, g25 = norm(d16), norm(d21), norm(d25)
    m_tr, _ = match(g16, g21); m_te, _ = match(g21, g25)
    ytr, ptr = seg_new_counts(g16, g21, m_tr, 1000)
    yte, pte = seg_new_counts(g21, g25, m_te, 1000)
    Xtr = np.stack([ptr, np.concatenate([[0], ptr[:-1]]), np.concatenate([ptr[1:], [0]])], 1).astype(float)
    Xte = np.stack([pte, np.concatenate([[0], pte[:-1]]), np.concatenate([pte[1:], [0]])], 1).astype(float)
    res = {}
    # C1 tuned Poisson-GLM
    a = cv_alpha_poisson(Xtr, ytr)
    m = PoissonRegressor(alpha=a, max_iter=1000).fit(Xtr, ytr)
    res["C1_tuned_poisson"] = {"alpha": a, "pred": m.predict(Xte)}
    # C2 log Ridge
    best, bestm = 1.0, 1e18
    for a2 in (0.1, 1.0, 10.0, 100.0):
        kf = KFold(3, shuffle=True, random_state=0)
        ms = [mean_absolute_error(y[va], np.expm1(Ridge(alpha=a2).fit(X[tr], np.log1p(y[tr])).predict(X[va])))
              for tr, va in kf.split(np.log1p(Xtr), ytr) for X, y in [(np.log1p(Xtr), ytr)]]
        if np.mean(ms) < bestm:
            best, bestm = a2, float(np.mean(ms))
    r = Ridge(alpha=best).fit(np.log1p(Xtr), np.log1p(ytr))
    res["C2_log_ridge"] = {"alpha": best, "pred": np.expm1(r.predict(np.log1p(Xte)))}
    # C3 calibrated B1 (linear map on train): pte scaled by train slope
    slope = float(np.polyfit(ptr, ytr, 1)[0]) if ptr.var() > 0 else 0.0
    icept = float(ytr.mean() - slope * ptr.mean())
    res["C3_calibrated_B1"] = {"slope": slope, "icept": icept, "pred": slope * pte + icept}
    # HGB seeds + C4 shuffle
    rng = np.random.default_rng(0)
    res["HGB"], res["C4_shuffle"] = [], []
    for seed in PARAMS["seeds"]:
        h = HistGradientBoostingRegressor(loss="poisson", random_state=seed).fit(Xtr, ytr)
        res["HGB"].append(h.predict(Xte))
        hs = HistGradientBoostingRegressor(loss="poisson", random_state=seed).fit(Xtr[rng.permutation(len(Xtr))], ytr)
        res["C4_shuffle"].append(hs.predict(Xte))
    res["mean_train"] = np.full_like(yte, float(ytr.mean()), dtype=float)
    out = {"controls": {}}
    for k, p in [("mean_train", res["mean_train"]), ("C1_tuned_poisson", res["C1_tuned_poisson"]["pred"]),
                 ("C2_log_ridge", res["C2_log_ridge"]["pred"]), ("C3_calibrated_B1", res["C3_calibrated_B1"]["pred"])]:
        p = np.clip(np.asarray(p, float), 0, None)
        sp = boot_spear(yte, p)
        out["controls"][k] = {"MAE": float(mean_absolute_error(yte, p)), "RMSE": float(mean_squared_error(yte, p) ** 0.5),
                              "spear": [sp[0], sp[1], sp[2]]}
    out["controls"]["C1_alpha"] = res["C1_tuned_poisson"]["alpha"]
    out["controls"]["C2_alpha"] = res["C2_log_ridge"]["alpha"]
    out["controls"]["C3_map"] = [res["C3_calibrated_B1"]["slope"], res["C3_calibrated_B1"]["icept"]]
    out["HGB"] = []
    for p in res["HGB"]:
        p = np.clip(p, 0, None)
        sp = boot_spear(yte, p)
        out["HGB"].append({"MAE": float(mean_absolute_error(yte, p)), "RMSE": float(mean_squared_error(yte, p) ** 0.5),
                           "spear": [sp[0], sp[1], sp[2]]})
    out["C4_shuffle"] = []
    for p in res["C4_shuffle"]:
        p = np.clip(p, 0, None)
        sp = boot_spear(yte, p)
        out["C4_shuffle"].append({"MAE": float(mean_absolute_error(yte, p)), "RMSE": float(mean_squared_error(yte, p) ** 0.5),
                                  "spear": [sp[0], sp[1], sp[2]]})
    # C3 residual: HGB MAE minus calibrated-B1 MAE (negative = HGB adds beyond B1)
    out["residual_HGB_minus_C3_MAE"] = [h["MAE"] - out["controls"]["C3_calibrated_B1"]["MAE"] for h in out["HGB"]]
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e06.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E06 tuned-shrinkage controls (ON 1km matched-new counts)"]
    for k in ("mean_train", "C1_tuned_poisson", "C2_log_ridge", "C3_calibrated_B1"):
        v = out["controls"][k]
        L.append(f"- {k}: MAE={v['MAE']:.2f} RMSE={v['RMSE']:.2f} spear={v['spear'][0]:.3f}")
    L.append(f"  alphas: C1={out['controls']['C1_alpha']} C2={out['controls']['C2_alpha']} C3map={out['controls']['C3_map']}")
    L.append(f"- HGB MAE={[round(h['MAE'],2) for h in out['HGB']]} spear={[round(h['spear'][0],3) for h in out['HGB']]}")
    L.append(f"- C4 shuffle MAE={[round(h['MAE'],2) for h in out['C4_shuffle']]} spear={[round(h['spear'][0],3) for h in out['C4_shuffle']]}")
    L.append(f"- residual HGB-C3 MAE={[round(x,2) for x in out['residual_HGB_minus_C3_MAE']]} (neg = HGB adds beyond B1)")
    (OUT / "results_e06.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
