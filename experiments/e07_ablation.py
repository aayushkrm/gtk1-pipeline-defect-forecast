"""E07: SMALL feature ablation (pre-registered, ON only, SRTO held out).
PREREGISTERED 7 past-only features per 100m cell:
 f1 n_past | f2 neighbor-lag sum | f3 max_depth_past | f4 mean_depth_past |
 f5 gwan_count_past | f6 dent_gooug_count_past | f7 n_pipes_with_past
Models: B1 (f1) vs LR (tuned C, train-CV) vs HGB-binary. Controls: train-only selection
+ F1 threshold; paired-bootstrap delta-AP vs B1; leave-one-group ablation; shuffle control.
Cuts >=10 primary, >=12/>=15 sensitivity. Test pair built once per cut, no peeking across cuts
for selection. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom, PARAMS
from e04b_robust import match_win
from sklearn.metrics import average_precision_score, precision_recall_curve, brier_score_loss
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
W, KMAX = 100, 1330
FEATS = ["n_past", "nlag", "maxd", "meand", "gwan", "mech", "npipes"]

def raw(df):
    g = lambda *k: next((c for c in df.columns if all(x.lower() in c.lower() for x in k)), None)
    cd, cc, cp = g("расстояние"), g("глубина"), g("номер", "трубы")
    co = g("левого", "начала") or g("левого")
    cr = g("ориентация", "максимума") or g("ориентация", "центра")
    ch = [c for c in df.columns if "характер" in c.lower()][0]
    ca = [c for c in df.columns if "характер" in c.lower() and "аббр" in c.lower()]
    ca = ca[0] if ca else None
    o = pd.DataFrame({"dist": pd.to_numeric(df[cd], errors="coerce"),
                      "depth": pd.to_numeric(df[cc], errors="coerce"),
                      "pipe": df[cp].astype(str).str.strip().str.replace(r"\.0$", "", regex=True),
                      "off": pd.to_numeric(df[co], errors="coerce") if co else np.nan,
                      "ori": df[cr].astype(str) if cr else "", "char": df[ch].astype(str),
                      "abbr": df[ca].astype(str) if ca else ""})
    o = o.dropna(subset=["dist"])
    o["corr"] = o["char"].str.contains("оррози", na=False)
    o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
    o["cell"] = (o["dist"] // W).astype(int).clip(0, KMAX)
    return o

def build(gp_all, gf_all, cut):
    gp = gp_all[gp_all["depth"] >= cut].copy()
    gf = gf_all[gf_all["depth"] >= cut].copy()
    m = match_win(gp, gf, 2)
    mr = float(m.mean())
    new = gf[~m]; newc = new[new["corr"]]
    y = (newc.groupby("cell").size().reindex(range(KMAX + 1), fill_value=0).values > 0).astype(int)
    past = gp[gp["corr"]]
    X = pd.DataFrame(index=range(KMAX + 1))
    X["n_past"] = past.groupby("cell").size().reindex(X.index, fill_value=0).astype(float)
    X["nlag"] = X["n_past"].shift(1, fill_value=0) + X["n_past"].shift(-1, fill_value=0)
    X["maxd"] = past.groupby("cell")["depth"].max().reindex(X.index, fill_value=0).astype(float)
    X["meand"] = past.groupby("cell")["depth"].mean().reindex(X.index, fill_value=0).astype(float)
    gw = gp[gp["char"].str.contains("кольцевого", na=False)]
    X["gwan"] = gw.groupby("cell").size().reindex(X.index, fill_value=0).astype(float)
    me = gp[gp["char"].str.contains("механич|вмятина|заводск", case=False, na=False)]
    X["mech"] = me.groupby("cell").size().reindex(X.index, fill_value=0).astype(float)
    X["npipes"] = past.groupby("cell")["pipe"].nunique().reindex(X.index, fill_value=0).astype(float)
    return y, X[FEATS].values, mr

def apd(y, a, b, n=1000, seed=0):
    """paired bootstrap delta-AP(a-b) + individual CIs"""
    rng = np.random.default_rng(seed)
    d0 = float(average_precision_score(y, a) - average_precision_score(y, b)) if y.sum() else 0.0
    bs = []
    for _ in range(n):
        i = rng.integers(0, len(y), len(y))
        if y[i].sum() > 0:
            bs.append(float(average_precision_score(y[i], a[i]) - average_precision_score(y[i], b[i])))
    return d0, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    res = {"features": FEATS, "cuts": {}}
    for cut in (10, 12, 15):
        ytr, Xtr, mr_tr = build(r16, r21, cut)
        yte, Xte, mr_te = build(r21, r25, cut)
        b1tr = Xtr[:, 0] / max(Xtr[:, 0].max(), 1)
        b1te = Xte[:, 0] / max(Xte[:, 0].max(), 1)
        # train-only C for LR via stratified CV on train
        bestC, bestm = 1.0, -1
        skf = StratifiedKFold(3, shuffle=True, random_state=0)
        for C in (0.01, 0.1, 1.0, 10.0):
            ms = []
            for tr, va in skf.split(Xtr, ytr):
                ms.append(average_precision_score(ytr[va],
                          LogisticRegression(C=C, max_iter=2000).fit(Xtr[tr], ytr[tr]).predict_proba(Xtr[va])[:, 1]))
            if np.mean(ms) > bestm:
                bestC, bestm = C, float(np.mean(ms))
        lr = LogisticRegression(C=bestC, max_iter=2000).fit(Xtr, ytr)
        slr = lr.predict_proba(Xte)[:, 1]
        hgb = HistGradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
        shg = hgb.predict_proba(Xte)[:, 1]
        # train-only F1 threshold from LR train scores
        prec, rec, ths = precision_recall_curve(ytr, lr.predict_proba(Xtr)[:, 1])
        f1 = [2 * p * r / max(p + r, 1e-9) for p, r in zip(prec, rec)]
        thr = float(ths[int(np.argmax(f1[:-1]))]) if len(ths) == len(f1) - 1 and ytr.sum() else 0.5
        d_lr, lo_lr, hi_lr = apd(yte, slr, b1te)
        d_hg, lo_hg, hi_hg = apd(yte, shg, b1te)
        # leave-one-group ablation on LR (retrain, train-only C fixed)
        abl = {}
        for j, f in enumerate(FEATS):
            keep = [k for k in range(len(FEATS)) if k != j]
            m = LogisticRegression(C=bestC, max_iter=2000).fit(Xtr[:, keep], ytr)
            s = m.predict_proba(Xte[:, keep])[:, 1]
            d, lo, hi = apd(yte, s, b1te, n=500)
            abl[f] = {"delta_vs_B1": [d, lo, hi]}
        # shuffle control
        rng = np.random.default_rng(0)
        msh = LogisticRegression(C=bestC, max_iter=2000).fit(Xtr[rng.permutation(len(Xtr))], ytr)
        ssh = msh.predict_proba(Xte)[:, 1]
        cell = {"match_tr": mr_tr, "match_te": mr_te, "prev_tr": float(ytr.mean()), "prev_te": float(yte.mean()),
                "B1_AP": float(average_precision_score(yte, b1te)), "base": float(yte.mean()),
                "LR_C": bestC, "LR_AP": float(average_precision_score(yte, slr)),
                "delta_LR_B1": [d_lr, lo_lr, hi_lr],
                "HGB_AP": float(average_precision_score(yte, shg)),
                "delta_HGB_B1": [d_hg, lo_hg, hi_hg],
                "F1_LR_train_thr": float(2 * ((slr >= thr) & (yte == 1)).sum() / max(((slr >= thr).sum() + yte.sum()), 1)),
                "Brier_LR": float(brier_score_loss(yte, slr)),
                "ablation": abl,
                "shuffle_AP": float(average_precision_score(yte, ssh))}
        res["cuts"][str(cut)] = cell
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    res["repro"] = {"git": gh}
    (OUT / "results_e07.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    L = ["# E07 small ablation (ON @100m, 7 pre-registered features, SRTO held out)"]
    for cut in ("10", "12", "15"):
        v = res["cuts"][cut]
        L.append(f"- cut>={cut}%: prev {v['prev_tr']:.3f}/{v['prev_te']:.3f} match {v['match_tr']:.3f}/{v['match_te']:.3f} "
                 f"B1={v['B1_AP']:.3f}/b={v['base']:.3f} LR(C={v['LR_C']})={v['LR_AP']:.3f} "
                 f"dLR-B1={v['delta_LR_B1'][0]:+.3f}[{v['delta_LR_B1'][1]:+.3f},{v['delta_LR_B1'][2]:+.3f}] "
                 f"HGB={v['HGB_AP']:.3f} dHGB-B1={v['delta_HGB_B1'][0]:+.3f}[{v['delta_HGB_B1'][1]:+.3f},{v['delta_HGB_B1'][2]:+.3f}] "
                 f"F1={v['F1_LR_train_thr']:.3f} Brier={v['Brier_LR']:.3f} shuff={v['shuffle_AP']:.3f}")
        worst = sorted(v["ablation"].items(), key=lambda kv: kv[1]["delta_vs_B1"][0])[:2]
        L.append(f"    weakest-when-dropped: {[(k, round(x['delta_vs_B1'][0],3)) for k, x in worst]}")
    (OUT / "results_e07.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
