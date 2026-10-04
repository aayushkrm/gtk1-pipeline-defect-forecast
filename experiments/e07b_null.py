"""E07b: null-calibration + ablation-vs-full + SRTO holdout (reviewer round-4 mandates).
Frozen <=7 features (same list as E07). C frozen by train-CV rule (reselected on train only).
1. constant-check: AP(mean-train constant on test) vs base, must match ~=0.005.
2. 100 train-label shuffles -> null AP_shuffle dist + (mean-base) CI. Pipeline FAILS calibration if CI excludes 0.
3. paired CI of Δ = AP_LR - mean(AP_shuffle null).
4. leave-one-out-vs-FULL ablation (paired delta, not vs B1).
5. SRTO holdout: same 7-feat LR trained SRTO-train (2016->2021), tested SRTO-test (2021->2024); Δ vs B1.
Cuts >=10 primary (+>=12 sensitivity for ON null only). Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
from e02_matched import load_anom, PARAMS
from e04b_robust import match_win
from e07_ablation import raw, FEATS
from e05_srto import load_any, SEC
from sklearn.metrics import average_precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]

def build(gp_all, gf_all, cut, kmax):
    gp = gp_all[gp_all["depth"] >= cut].copy()
    gf = gf_all[gf_all["depth"] >= cut].copy()
    m = match_win(gp, gf, 2)
    new = gf[~np.asarray(m)]; newc = new[new["corr"]]
    ck = lambda g: (g["dist"] // 100).astype(int).clip(0, kmax)
    y = (newc.groupby(ck(newc)).size().reindex(range(kmax + 1), fill_value=0).values > 0).astype(int)
    past = gp[gp["corr"]]
    X = pd.DataFrame(index=range(kmax + 1))
    X["n_past"] = past.groupby(ck(past)).size().reindex(X.index, fill_value=0).astype(float)
    X["nlag"] = X["n_past"].shift(1, fill_value=0) + X["n_past"].shift(-1, fill_value=0)
    X["maxd"] = past.groupby(ck(past))["depth"].max().reindex(X.index, fill_value=0).astype(float)
    X["meand"] = past.groupby(ck(past))["depth"].mean().reindex(X.index, fill_value=0).astype(float)
    gw = gp[gp["char"].str.contains("кольцевого", na=False)]
    X["gwan"] = gw.groupby(ck(gw)).size().reindex(X.index, fill_value=0).astype(float)
    me = gp[gp["char"].str.contains("механич|вмятина|заводск", case=False, na=False)]
    X["mech"] = me.groupby(ck(me)).size().reindex(X.index, fill_value=0).astype(float)
    X["npipes"] = past.groupby(ck(past))["pipe"].nunique().reindex(X.index, fill_value=0).astype(float)
    return y, X[FEATS].values, float(m.mean())

def pick_C(Xtr, ytr):
    bestC, bestm = 1.0, -1
    for C in (0.01, 0.1, 1.0, 10.0):
        ms = []
        for tr, va in StratifiedKFold(3, shuffle=True, random_state=0).split(Xtr, ytr):
            ms.append(average_precision_score(ytr[va],
                      LogisticRegression(C=C, max_iter=2000).fit(Xtr[tr], ytr[tr]).predict_proba(Xtr[va])[:, 1]))
        if np.mean(ms) > bestm:
            bestC, bestm = C, float(np.mean(ms))
    return bestC

def run():
    d16, _ = load_anom(2016); d21, _ = load_anom(2021); d25, _ = load_anom(2025)
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    out = {}
    for cut in (10, 12):
        ytr, Xtr, mr_tr = build(r16, r21, cut, 1330)
        yte, Xte, mr_te = build(r21, r25, cut, 1330)
        base = float(yte.mean())
        # 1. constant check
        const = np.full_like(yte, float(ytr.mean()), dtype=float)
        ap_const = float(average_precision_score(yte, const))
        # frozen C + LR
        C = pick_C(Xtr, ytr)
        lr = LogisticRegression(C=C, max_iter=2000).fit(Xtr, ytr)
        s_lr = lr.predict_proba(Xte)[:, 1]
        ap_lr = float(average_precision_score(yte, s_lr))
        # 2. 100-shuffle null
        rng = np.random.default_rng(0)
        null = []
        for i in range(100):
            m = LogisticRegression(C=C, max_iter=2000).fit(Xtr, ytr[rng.permutation(len(ytr))])
            null.append(float(average_precision_score(yte, m.predict_proba(Xte)[:, 1])))
        null = np.array(null)
        # 3. paired CI of Δ vs mean(null): bootstrap cells of (AP_LR - nullmean)? use fixed nullmean
        nm = float(null.mean())
        brng = np.random.default_rng(1)
        d0 = ap_lr - nm
        bs = []
        for _ in range(1000):
            idx = brng.integers(0, len(yte), len(yte))
            if yte[idx].sum() > 0:
                bs.append(float(average_precision_score(yte[idx], s_lr[idx])) - nm)
        # 4. ablation vs FULL
        abl = {}
        for j, f in enumerate(FEATS):
            keep = [k for k in range(len(FEATS)) if k != j]
            m = LogisticRegression(C=C, max_iter=2000).fit(Xtr[:, keep], ytr)
            s = m.predict_proba(Xte[:, keep])[:, 1]
            dd = []
            for _ in range(500):
                idx = brng.integers(0, len(yte), len(yte))
                if yte[idx].sum() > 0:
                    dd.append(float(average_precision_score(yte[idx], s[idx]) - average_precision_score(yte[idx], s_lr[idx])))
            abl[f] = {"delta_vs_full": float(np.mean(dd)), "CI": [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]}
        out[str(cut)] = {"C": C, "base": base, "const_AP": ap_const, "const_gap": ap_const - base,
                         "LR_AP": ap_lr, "null_mean": nm, "null_CI": [float(np.percentile(null, 2.5)), float(np.percentile(null, 97.5))],
                         "null_minus_base_CI": [float(np.percentile(null - base, 2.5)), float(np.percentile(null - base, 97.5))],
                         "delta_vs_nullmean": d0, "delta_CI": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                         "ablation_vs_full": abl, "match_tr": mr_tr, "match_te": mr_te}
    # 5. SRTO holdout of LR lift
    sframes = {}
    for y in (2016, 2021, 2024):
        df, _ = load_any(y)
        sframes[y] = raw(df)
    ytr, Xtr, _ = build(sframes[2016], sframes[2021], 10, 1040)
    yte, Xte, _ = build(sframes[2021], sframes[2024], 10, 1040)
    C = pick_C(Xtr, ytr)
    lr = LogisticRegression(C=C, max_iter=2000).fit(Xtr, ytr)
    s_lr = lr.predict_proba(Xte)[:, 1]
    b1 = Xte[:, 0] / max(Xte[:, 0].max(), 1)
    brng = np.random.default_rng(2)
    dd = []
    for _ in range(1000):
        idx = brng.integers(0, len(yte), len(yte))
        if yte[idx].sum() > 0:
            dd.append(float(average_precision_score(yte[idx], s_lr[idx]) - average_precision_score(yte[idx], b1[idx])))
    out["SRTO_holdout"] = {"C": C, "LR_AP": float(average_precision_score(yte, s_lr)),
                           "B1_AP": float(average_precision_score(yte, b1)), "base": float(yte.mean()),
                           "delta_CI": [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh}
    (OUT / "results_e07b.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    L = ["# E07b null-calibration + ablation-vs-full + SRTO holdout (frozen ≤7 feats)"]
    for cut in ("10", "12"):
        v = out[cut]
        L.append(f"- cut>={cut}%: base={v['base']:.3f} const={v['const_AP']:.3f} (gap {v['const_gap']:+.4f}) | "
                 f"LR={v['LR_AP']:.3f} null={v['null_mean']:.3f} null-baseCI=[{v['null_minus_base_CI'][0]:+.3f},{v['null_minus_base_CI'][1]:+.3f}] | "
                 f"d-vs-null={v['delta_vs_nullmean']:+.3f}[{v['delta_CI'][0]:+.3f},{v['delta_CI'][1]:+.3f}]")
        L.append(f"    abl-vs-full: {[(f, round(a['delta_vs_full'],3)) for f, a in sorted(v['ablation_vs_full'].items(), key=lambda kv: kv[1]['delta_vs_full'])]}")
    s = out["SRTO_holdout"]
    L.append(f"- SRTO holdout: LR={s['LR_AP']:.3f} B1={s['B1_AP']:.3f} base={s['base']:.3f} dCI=[{s['delta_CI'][0]:+.3f},{s['delta_CI'][1]:+.3f}]")
    (OUT / "results_e07b.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
