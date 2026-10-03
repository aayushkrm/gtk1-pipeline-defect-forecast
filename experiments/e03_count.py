"""E03: P2 count + new-in-clean rare target + 100m-vs-1km ablation (cheap, ON only).
Reuses matching/labels from e02_matched (same pipe + |dd|<=2 + |doff|<=0.5 + |dh|<=1h).
Targets use PAST-ONLY features. No test tuning. Seeds fixed.
Read-only on raw data. Writes de-identified aggregates only.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom, norm, match, PARAMS
from sklearn.metrics import average_precision_score, mean_absolute_error, mean_squared_error
from sklearn.linear_model import PoissonRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from scipy.stats import spearmanr

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]

def seg_new_counts(g_past, g_fut, fut_m, width):
    kmax = 133 if width == 1000 else 1330
    idx = range(kmax + 1)
    new_f = g_fut[~np.asarray(fut_m)]
    new_f = new_f[new_f["corr"]]
    key = (new_f["dist"] // width).astype(int).clip(0, kmax)
    cnt = new_f.groupby(key).size().reindex(idx, fill_value=0).values
    past = g_past[g_past["corr"]].groupby((g_past[g_past["corr"]]["dist"] // width).astype(int)
          ).size().reindex(idx, fill_value=0).values
    return cnt, past

def boot_spear(a, b, n=500, seed=0):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if len(np.unique(a)) < 2 or len(np.unique(b)) < 2:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    obs = float(spearmanr(a, b).statistic)
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(a), len(a))
        if len(np.unique(a[i])) > 1 and len(np.unique(b[i])) > 1:
            bs.append(float(spearmanr(a[i], b[i]).statistic))
    if not bs:
        return obs, float("nan"), float("nan")
    return obs, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    g16, g21, g25 = norm(d16), norm(d21), norm(d25)
    m_tr, s_tr = match(g16, g21)
    m_te, s_te = match(g21, g25)
    out = {"params": {**PARAMS, "note": "E03 count/rare/grid"}}
    # --- P2 count at 1km ---
    ytr_c, ptr_c = seg_new_counts(g16, g21, m_tr, 1000)
    yte_c, pte_c = seg_new_counts(g21, g25, m_te, 1000)
    Xtr = np.stack([ptr_c, np.concatenate([[0], ptr_c[:-1]]), np.concatenate([ptr_c[1:], [0]])], 1)
    Xte = np.stack([pte_c, np.concatenate([[0], pte_c[:-1]]), np.concatenate([pte_c[1:], [0]])], 1)
    glob = float(ytr_c.mean())
    preds = {"mean_train": np.full_like(yte_c, glob, dtype=float), "persistence": pte_c.astype(float)}
    try:
        pr = PoissonRegressor(max_iter=500).fit(Xtr, ytr_c)
        preds["poisson_glm"] = pr.predict(Xte)
    except Exception as e:
        preds["poisson_glm"] = np.full_like(yte_c, glob, dtype=float)
        out["poisson_error"] = str(e)
    hgb = {}
    for seed in PARAMS["seeds"]:
        m = HistGradientBoostingRegressor(loss="poisson", random_state=seed).fit(Xtr, ytr_c)
        preds[f"hgb_poisson_s{seed}"] = m.predict(Xte)
    c = {}
    for k, p in preds.items():
        p = np.clip(p, 0, None)
        c[k] = {"MAE": float(mean_absolute_error(yte_c, p)),
                "RMSE": float(mean_squared_error(yte_c, p) ** 0.5),
                "spearman": boot_spear(yte_c, p)}
    c["target_stats"] = {"mean_tr": float(ytr_c.mean()), "mean_te": float(yte_c.mean()),
                         "max_te": int(yte_c.max()), "zero_frac_te": float((yte_c == 0).mean())}
    out["P2_count_1km"] = c
    # --- new-in-clean rare target (past corr == 0 -> any new) ---
    mask_tr, mask_te = ptr_c == 0, pte_c == 0
    out["new_in_clean"] = {
        "n_clean_tr": int(mask_tr.sum()), "n_clean_te": int(mask_te.sum()),
        "prev_tr": float((ytr_c[mask_tr] > 0).mean()) if mask_tr.sum() else 0.0,
        "prev_te": float((yte_c[mask_te] > 0).mean()) if mask_te.sum() else 0.0}
    yc = (yte_c[mask_te] > 0).astype(int) if mask_te.sum() else np.array([0])
    # B1 can't score clean (past=0 everywhere) -> uniform; report AP vs base only
    if mask_te.sum() and yc.sum() > 0:
        ap = float(average_precision_score(yc, np.zeros_like(yc, dtype=float)))
        out["new_in_clean"]["AP_uniform"] = ap
    # --- 100m ablation: presence + growth AP of B1 vs base ---
    for width, kmax in ((100, 1330), (1000, 133)):
        def pres(g, w, k):
            return (g[g["corr"]].groupby((g[g["corr"]]["dist"] // w).astype(int)
                    ).size().reindex(range(k + 1), fill_value=0).values > 0).astype(int)
        if width == 100:
            p16, p21, p25 = pres(g16, 100, 1330), pres(g21, 100, 1330), pres(g25, 100, 1330)
            y, s = p25, p21.astype(float)
        else:
            p16, p21 = pres(g16, 1000, 133), pres(g21, 1000, 133)
            p25 = pres(g25, 1000, 133)
            y, s = p25, p21.astype(float)
        ap = float(average_precision_score(y, s)) if y.sum() > 0 else 0.0
        out[f"grid_{width}m_presence"] = {"AP_B1": ap, "base": float(y.mean()),
            "n": len(y), "positives": int(y.sum())}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh, "versions": {"pandas": __import__("pandas").__version__,
                     "sklearn": __import__("sklearn").__version__, "python": sys.version.split()[0]}}
    (OUT / "results_e03.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    p2 = out["P2_count_1km"]
    L = ["# E03 count + rare-target + grid ablation (ON, matched-new counts)",
         f"count target: mean tr/te {p2['target_stats']['mean_tr']:.2f}/{p2['target_stats']['mean_te']:.2f} "
         f"max_te {p2['target_stats']['max_te']} zero_frac {p2['target_stats']['zero_frac_te']:.2f}"]
    for k in ("mean_train", "persistence", "poisson_glm", "hgb_poisson_s0"):
        v = p2[k]
        L.append(f"- {k}: MAE={v['MAE']:.2f} RMSE={v['RMSE']:.2f} spear={v['spearman'][0]:.3f} [{v['spearman'][1]:.3f},{v['spearman'][2]:.3f}]")
    nc = out["new_in_clean"]
    L.append(f"- new-in-clean: n tr/te {nc['n_clean_tr']}/{nc['n_clean_te']} prev tr/te {nc['prev_tr']:.3f}/{nc['prev_te']:.3f}")
    for w in (100, 1000):
        g = out[f"grid_{w}m_presence"]
        L.append(f"- grid {w}m presence: AP_B1={g['AP_B1']:.3f} base={g['base']:.3f} n={g['n']} pos={g['positives']}")
    (OUT / "results_e03.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
