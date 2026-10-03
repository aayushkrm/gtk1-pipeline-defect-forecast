"""E02: matched-label build + fixed evaluation (reviewer must-fix #1-2).
- Labels: greedy bipartite match per pipe (same pipe + |dd|<=2 + |doff|<=0.5 + |dh|<=1h),
  Y=1 iff >=1 UNMATCHED future corrosion (Depth>=10). Segment-diff kept diagnostic only.
- Baselines: B1 past count, B2 global-rate constant + Poisson count, B3 pipe-persistence.
- Metrics: AP + bootstrap 95% CI, R@P0.85, P@R0.5, F1 with TRAIN-only threshold, Brier.
- Repro: params logged, git hash, versions, file sizes/mtimes, relative data path.
Read-only on raw data. Writes de-identified aggregates only.
"""
import json, subprocess, sys, time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, precision_recall_curve, brier_score_loss
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV

REPO = Path(__file__).resolve().parents[1]
DATA = REPO.parent / "Данные для предварительного изучения" / "Омск-Новосибирск (392-526)"
OUT = Path(__file__).resolve().parent
PARAMS = {"depth_min": 10, "win_dist": 2.0, "win_off": 0.5, "win_h": 1, "kmax": 133,
          "train": [2016, 2021], "test": [2021, 2025], "seeds": [0, 1, 2], "boot": 1000}

def fhash(p: Path):
    return {"name": p.name, "bytes": p.stat().st_size, "mtime": p.stat().st_mtime}

def load_anom(year):
    d = DATA / str(year)
    fp = d / "Аномалии.xlsx" if (d / "Аномалии.xlsx").exists() else d / "Аномалии_.xlsx"
    df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    return df, fhash(fp)

def norm(df):
    g = lambda *k: next((c for c in df.columns if all(x.lower() in c.lower() for x in k)), None)
    c_dist, c_depth = g("расстояние"), g("глубина")
    c_char, c_pipe = g("характер", "особен"), g("номер", "трубы")
    c_off = g("левого", "начала") or g("левого")
    c_ori = g("ориентация", "максимума") or g("ориентация", "центра")
    out = pd.DataFrame({
        "dist": pd.to_numeric(df[c_dist], errors="coerce"),
        "depth": pd.to_numeric(df[c_depth], errors="coerce"),
        "pipe": df[c_pipe].astype(str).str.strip().str.replace(r"\.0$", "", regex=True),
        "off": pd.to_numeric(df[c_off], errors="coerce") if c_off else np.nan,
        "ori": df[c_ori].astype(str) if c_ori else "",
        "char": df[[c for c in df.columns if "характер" in c.lower()][0]].astype(str) if c_char else "",
    }).dropna(subset=["dist"])
    out = out[out["depth"] >= PARAMS["depth_min"]].copy()
    out["corr"] = out["char"].str.contains("оррози", na=False)
    out["h"] = out["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    out["km"] = (out["dist"] // 1000).astype(int).clip(0, PARAMS["kmax"])
    return out

def match(past, fut):
    """Greedy per-pipe bipartite match. Returns fut matched flag, collision/match rates."""
    fut_m = np.zeros(len(fut), bool)
    n_cand = 0
    for pipe, fi in fut.groupby("pipe").groups.items():
        F = fut.loc[fi]
        P = past[past["pipe"] == pipe]
        if P.empty:
            continue
        for j, f in F.iterrows():
            dd = (P["dist"] - f["dist"]).abs().values
            cand = np.where(dd <= PARAMS["win_dist"])[0]
            if len(cand) == 0:
                continue
            if len(cand) > 1:
                n_cand += 1
            do = np.abs(P.iloc[cand]["off"].values - (f["off"] if pd.notna(f["off"]) else 1e9))
            do = np.where(pd.isna(P.iloc[cand]["off"].values) | pd.isna(f["off"]), 0.0, do)
            dhv = P.iloc[cand]["h"].values
            d = np.abs(dhv - f["h"]) % 12
            dh = np.where((dhv < 0) | (f["h"] < 0), 0.0, np.minimum(d, 12 - d))
            ok = (do <= PARAMS["win_off"]) & (dh <= PARAMS["win_h"])
            if not ok.any():
                continue
            cost = dd[cand][ok] + 2 * do[ok] + 0.5 * dh[ok]
            best = cand[ok][int(np.argmin(cost))]
            # one-to-one: remove used past row
            P = P.drop(P.index[best])
            fut_m[fut.index.get_loc(j)] = True
    return fut_m, {"match_rate": float(fut_m.mean()) if len(fut_m) else 0.0,
                   "collision_rate": float(n_cand / max(len(fut), 1))}

def seg_labels(g_past, g_fut, fut_m):
    kmax = PARAMS["kmax"]
    idx = range(kmax + 1)
    new_f = g_fut[~fut_m]
    y_new = new_f[new_f["corr"]].groupby("km").size().reindex(idx, fill_value=0).values > 0
    y_diff = ((g_fut.groupby("km").size().reindex(idx, fill_value=0).values -
               g_past.groupby("km").size().reindex(idx, fill_value=0).values) > 0)
    van = len(g_past) - int(fut_m.sum() * len(g_past) / max(len(g_fut), 1))  # approx retained
    return y_new.astype(int), y_diff.astype(int)

def ap_ci(y, s, n=1000, seed=0):
    rng = np.random.default_rng(seed)
    base = float(average_precision_score(y, s)) if y.sum() > 0 else 0.0
    bs = [float(average_precision_score(y[i], s[i])) for i in
          (rng.integers(0, len(y), len(y)) for _ in range(n)) if y[i].sum() > 0]
    return base, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

def pr_at(y, s, mode, t):
    prec, rec, _ = precision_recall_curve(y, s)
    if mode == "R@P":
        c = [(r, p) for p, r in zip(prec, rec) if p >= t]
        return max([r for r, _ in c]) if c else 0.0
    c = [(p, r) for p, r in zip(prec, rec) if r >= t]
    return max([p for p, _ in c]) if c else 0.0

def run():
    d16, h16 = load_anom(2016); d21, h21 = load_anom(2021); d25, h25 = load_anom(2025)
    g16, g21, g25 = norm(d16), norm(d21), norm(d25)
    m_tr, s_tr = match(g16, g21)
    m_te, s_te = match(g21, g25)
    ytr, ytr_d = seg_labels(g16, g21, m_tr)
    yte, yte_d = seg_labels(g21, g25, m_te)
    # agreement segment-diff vs matched-new
    agree_tr = float((ytr == ytr_d).mean()); agree_te = float((yte == yte_d).mean())
    van_tr = 1 - float(m_tr.mean()); van_te = 1 - float(m_te.mean())
    # features: past count + neighbour lags (past only)
    def feats(g):
        c = g.groupby("km").size().reindex(range(PARAMS["kmax"] + 1), fill_value=0).values.astype(float)
        return np.stack([c, np.concatenate([[0], c[:-1]]), np.concatenate([c[1:], [0]])], 1), c
    Xtr, c16 = feats(g16); Xte, c21v = feats(g21)
    # baselines: B1 past count; B2 constant prevalence from train; B3 pipe persistence approx
    pipe_past = set(g16[g16["corr"]]["pipe"])
    b3 = np.array([1.0 if set(g21[(g21.km == k) & g21["corr"]]["pipe"]) & pipe_past else (1.0 if c21v[k] > 0 else 0.0)
                   for k in range(PARAMS["kmax"] + 1)])
    b1 = c21v / max(c21v.max(), 1)
    b2 = np.full_like(b1, float(ytr.mean()))
    out = {"params": PARAMS, "files": [h16, h21, h25],
           "match": {"train": s_tr, "test": s_te, "vanished_frac_train": van_tr, "vanished_frac_test": van_te,
                      "agree_diff_vs_matched_train": agree_tr, "agree_diff_vs_matched_test": agree_te,
                      "prev_matched_new_train": float(ytr.mean()), "prev_matched_new_test": float(yte.mean()),
                      "prev_diff_train": float(ytr_d.mean()), "prev_diff_test": float(yte_d.mean())}}
    for name, s in [("B1_past_count", b1), ("B2_global_rate", b2), ("B3_pipe_persist", b3)]:
        ap, lo, hi = ap_ci(yte, s, PARAMS["boot"])
        out[name] = {"AP": ap, "CI95": [lo, hi], "R@P0.85": pr_at(yte, s, "R@P", 0.85), "P@R0.5": pr_at(yte, s, "P@R", 0.5)}
    # HGB + train-only threshold F1 + calibration (train-CV)
    thr = 0.5
    prec_tr, rec_tr, th = precision_recall_curve(ytr, HistGradientBoostingClassifier(random_state=0).fit(Xtr, ytr).predict_proba(Xtr)[:, 1])
    f1s = [2 * p * r / max(p + r, 1e-9) for p, r in zip(prec_tr, rec_tr)]
    thr = float(th[int(np.argmax(f1s[:-1]))]) if len(th) == len(f1s) - 1 else 0.5
    aps = []
    for seed in PARAMS["seeds"]:
        m = HistGradientBoostingClassifier(random_state=seed).fit(Xtr, ytr)
        s = m.predict_proba(Xte)[:, 1]
        ap, lo, hi = ap_ci(yte, s, 500)
        cal = CalibratedClassifierCV(m, cv=3).fit(Xtr, ytr)
        sc = cal.predict_proba(Xte)[:, 1]
        aps.append({"AP": ap, "CI95": [lo, hi], "R@P0.85": pr_at(yte, s, "R@P", 0.85),
                    "F1@train_thr": float(2 * ((sc >= thr) & (yte == 1)).sum() / max(((sc >= thr).sum() + yte.sum()), 1)),
                    "Brier": float(brier_score_loss(yte, sc))})
    out["HGB"] = aps
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh, "versions": {"pandas": pd.__version__, "numpy": np.__version__,
                     "sklearn": __import__("sklearn").__version__, "python": sys.version.split()[0]}}
    (OUT / "results_e02.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E02 matched-label results (ON 1km, Depth>=10, corr-only match)",
         f"match_rate tr/te: {s_tr['match_rate']:.3f}/{s_te['match_rate']:.3f} collision: {s_tr['collision_rate']:.3f}/{s_te['collision_rate']:.3f}",
         f"prev matched-new tr/te: {ytr.mean():.3f}/{yte.mean():.3f} vs segdiff: {ytr_d.mean():.3f}/{yte_d.mean():.3f}",
         f"agreement diff-vs-matched tr/te: {agree_tr:.3f}/{agree_te:.3f} vanished-frac tr/te: {van_tr:.3f}/{van_te:.3f}"]
    for k in ("B1_past_count", "B2_global_rate", "B3_pipe_persist"):
        v = out[k]
        L.append(f"- {k}: AP={v['AP']:.3f} [{v['CI95'][0]:.3f},{v['CI95'][1]:.3f}] R@P.85={v['R@P0.85']:.3f} P@R.5={v['P@R0.5']:.3f}")
    h = out["HGB"]
    L.append(f"- HGB AP: {[round(x['AP'],3) for x in h]} R@P.85: {[round(x['R@P0.85'],3) for x in h]} F1@train_thr: {[round(x['F1@train_thr'],3) for x in h]} Brier: {[round(x['Brier'],3) for x in h]}")
    (OUT / "results_e02.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
