"""E04: honest P1 @100m (matched-new binary) + depth-threshold sensitivity.
Train 16->21, test 21->25, ON only. Labels from per-pipe greedy match
(same pipe + |dd|<=2 + |doff|<=0.5 + |dh|<=1h), Y=1 iff >=1 UNMATCHED future
corrosion in the 100m cell. Sensitivity over depth cuts {10, 15}%.
Past-only features. No test tuning. Seeds fixed. Read-only raw data.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e02_matched as E
from sklearn.metrics import average_precision_score, precision_recall_curve, brier_score_loss
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
W = 100
KMAX = 1330

def cell_key(g):
    return (g["dist"] // W).astype(int).clip(0, KMAX)

def run_cut(g16, g21, g25, cut):
    f = lambda g: g[g["depth"] >= cut].copy()
    a16, a21, a25 = f(g16), f(g21), f(g25)
    m_tr, s_tr = E.match(a16, a21)
    m_te, s_te = E.match(a21, a25)
    def labels(gp, gf, m):
        new = gf[~np.asarray(m)]; new = new[new["corr"]]
        y = new.groupby(cell_key(new)).size().reindex(range(KMAX + 1), fill_value=0).values > 0
        past = gp[gp["corr"]].groupby(cell_key(gp[gp["corr"]])).size() \
            .reindex(range(KMAX + 1), fill_value=0).values.astype(float)
        return y.astype(int), past
    ytr, ptr = labels(a16, a21, m_tr)
    yte, pte = labels(a21, a25, m_te)
    def feats(p):
        return np.stack([p, np.concatenate([[0], p[:-1]]), np.concatenate([p[1:], [0]])], 1)
    Xtr, Xte = feats(ptr), feats(pte)
    ppast = set(a16[a16["corr"]]["pipe"])
    b3 = np.array([1.0 if set(a21[(cell_key(a21) == k) & a21["corr"]]["pipe"]) & ppast
                   else (1.0 if pte[k] > 0 else 0.0) for k in range(KMAX + 1)])
    out = {"match_tr": s_tr, "match_te": s_te, "prev_tr": float(ytr.mean()), "prev_te": float(yte.mean())}
    rng = np.random.default_rng(0)
    def apci(y, s, n=500):
        b = float(average_precision_score(y, s)) if y.sum() > 0 else 0.0
        bs = [float(average_precision_score(y[i], s[i])) for i in
              (rng.integers(0, len(y), len(y)) for _ in range(n)) if y[i].sum() > 0]
        return b, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))
    for name, s in [("B1", pte / max(pte.max(), 1)), ("B2", np.full(KMAX + 1, float(ytr.mean()))), ("B3", b3)]:
        a, lo, hi = apci(yte, s)
        out[name] = {"AP": a, "CI": [lo, hi]}
    th = 0.5
    m0 = HistGradientBoostingClassifier(random_state=0).fit(Xtr, ytr)
    prec, rec, ths = precision_recall_curve(ytr, m0.predict_proba(Xtr)[:, 1])
    f1 = [2 * p * r / max(p + r, 1e-9) for p, r in zip(prec, rec)]
    if len(ths) == len(f1) - 1 and ytr.sum() > 0:
        th = float(ths[int(np.argmax(f1[:-1]))])
    hs = []
    for seed in E.PARAMS["seeds"]:
        m = HistGradientBoostingClassifier(random_state=seed).fit(Xtr, ytr)
        s = m.predict_proba(Xte)[:, 1]
        a, lo, hi = apci(yte, s)
        cal = CalibratedClassifierCV(m, cv=3).fit(Xtr, ytr)
        sc = cal.predict_proba(Xte)[:, 1]
        hs.append({"AP": a, "CI": [lo, hi],
                   "F1@train_thr": float(2 * ((sc >= th) & (yte == 1)).sum() / max(((sc >= th).sum() + yte.sum()), 1)),
                   "Brier": float(brier_score_loss(yte, sc))})
    out["HGB"] = hs
    return out

def run():
    d16, _ = E.load_anom(2016); d21, _ = E.load_anom(2021); d25, _ = E.load_anom(2025)
    g16, g21, g25 = E.norm(d16), E.norm(d21), E.norm(d25)
    # E.norm already applies depth>=10; re-expand by reloading raw depths:
    def raw(df):
        g = lambda *k: next((c for c in df.columns if all(x.lower() in c.lower() for x in k)), None)
        cd, cc, cp = g("расстояние"), g("глубина"), g("номер", "трубы")
        co = g("левого", "начала") or g("левого")
        cr = g("ориентация", "максимума") or g("ориентация", "центра")
        ch = [c for c in df.columns if "характер" in c.lower()][0]
        o = pd.DataFrame({"dist": pd.to_numeric(df[cd], errors="coerce"),
                          "depth": pd.to_numeric(df[cc], errors="coerce"),
                          "pipe": df[cp].astype(str).str.strip().str.replace(r"\.0$", "", regex=True),
                          "off": pd.to_numeric(df[co], errors="coerce") if co else np.nan,
                          "ori": df[cr].astype(str) if cr else "", "char": df[ch].astype(str)})
        o = o.dropna(subset=["dist"])
        o["corr"] = o["char"].str.contains("оррози", na=False)
        o["h"] = o["ori"].str.extract(r"(\d{1,2})")[0].astype(float).fillna(-99)
        return o
    import pandas as pd
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    res = {"width_m": W, "cuts": {}}
    for cut in (10, 15):
        res["cuts"][str(cut)] = run_cut(r16, r21, r25, cut)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    res["repro"] = {"git": gh, "versions": {"pandas": pd.__version__,
                     "sklearn": __import__("sklearn").__version__, "python": sys.version.split()[0]}}
    (OUT / "results_e04.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    L = ["# E04 honest P1 @100m, matched-new, depth-cut sensitivity (ON)"]
    for cut in ("10", "15"):
        v = res["cuts"][cut]
        L.append(f"- cut>={cut}%: prev tr/te {v['prev_tr']:.3f}/{v['prev_te']:.3f} "
                 f"match tr/te {v['match_tr']['match_rate']:.3f}/{v['match_te']['match_rate']:.3f}")
        for b in ("B1", "B2", "B3"):
            L.append(f"    {b}: AP={v[b]['AP']:.3f} [{v[b]['CI'][0]:.3f},{v[b]['CI'][1]:.3f}]")
        h = v["HGB"]
        L.append(f"    HGB AP={[round(x['AP'],3) for x in h]} F1={([round(x['F1@train_thr'],3) for x in h])} Brier={([round(x['Brier'],3) for x in h])}")
    (OUT / "results_e04.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
