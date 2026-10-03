"""E01-E06 cheap baselines: ON 392-526, 1km grid, Depth>=10%.
Read-only on raw data. Writes only de-identified aggregates to experiments/.
No test tuning. Seeds fixed.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import average_precision_score, precision_recall_curve
from sklearn.ensemble import HistGradientBoostingClassifier
from scipy.stats import spearmanr

BASE = Path("/Users/akm/Tsu Project/Данные для предварительного изучения/Омск-Новосибирск (392-526)")
OUT = Path(__file__).resolve().parent

def load_anom(year: int) -> pd.DataFrame:
    d = BASE / str(year)
    fp = next((d / n for n in ["Аномалии.xlsx", "Аномалии_.xlsx"] if (d / n).exists()), None)
    assert fp, f"missing {d}"
    df = pd.read_excel(fp, sheet_name="Аномалии", header=3, engine="openpyxl")
    df.columns = [str(c).strip() for c in df.columns]
    return df

def find_col(df, *keys):
    for c in df.columns:
        lc = c.lower()
        if all(k.lower() in lc for k in keys):
            return c
    return None

def norm_year(df: pd.DataFrame) -> pd.DataFrame:
    dist = find_col(df, "расстояние")
    depth = find_col(df, "глубина")
    char = find_col(df, "характер")
    out = pd.DataFrame({
        "dist": pd.to_numeric(df[dist], errors="coerce"),
        "depth": pd.to_numeric(df[depth], errors="coerce"),
        "char": df[char].astype(str) if char else "",
    }).dropna(subset=["dist"])
    out = out[out["depth"] >= 10].copy()
    out["km"] = (out["dist"] // 1000).astype(int).clip(0, 133)
    out["is_corr"] = out["char"].str.contains("оррози", na=False)
    return out

def grid_counts(g: pd.DataFrame, kmax=133):
    idx = pd.Index(range(kmax + 1), name="km")
    return g.groupby("km").size().reindex(idx, fill_value=0)

def recall_at_p(y, s, p0=0.7):
    prec, rec, _ = precision_recall_curve(y, s)
    # precision_recall_curve returns arrays len thresholds+1; take max rec with prec>=p0
    best = 0.0
    hit = False
    for p, r in zip(prec, rec):
        if p >= p0 and r > best:
            best, hit = float(r), True
    return best if hit else 0.0

def main():
    g16, g21, g25 = (norm_year(load_anom(y)) for y in (2016, 2021, 2025))
    c16, c21, c25 = (grid_counts(g) for g in (g16, g21, g25))
    present21 = (c21 > 0).astype(int).values
    present25 = (c25 > 0).astype(int).values
    growth2125 = ((c25 - c21).clip(lower=0) > 0).astype(int).values  # new-anomaly proxy at segment level
    growth1621 = ((c21 - c16).clip(lower=0) > 0).astype(int).values
    new_in_empty = present25[(c21 == 0).values]  # for reporting prevalence only

    res = {"counts": {"2016": int(len(g16)), "2021": int(len(g21)), "2025": int(len(g25))},
           "mean_per_seg": [float(c16.mean()), float(c21.mean()), float(c25.mean())]}
    # E01 persistence: past count predicts future presence/growth
    for name, y, s in [("16->21 presence", (c21 > 0).astype(int).values, c16.values),
                       ("21->25 presence", present25, c21.values),
                       ("16->21 growth", growth1621, c16.values),
                       ("21->25 growth", growth2125, c21.values)]:
        ap = float(average_precision_score(y, s)) if y.sum() > 0 else 0.0
        res[name] = {"ap": ap, "base": float(y.mean()), "recall@P0.7": recall_at_p(y, s),
                     "spearman_past_future": float(spearmanr(c16.values, c21.values).statistic) if "16" in name[:2] else float(spearmanr(c21.values, c25.values).statistic)}
    # E04-E06 HGB on growth 21->25, trained on 16->21 mapping (past count + density features only)
    def feats(c):
        v = c.values.astype(float)
        return np.stack([v, np.concatenate([[0], v[:-1]]), np.concatenate([v[1:], [0]])], axis=1)
    Xtr, ytr = feats(c16), growth1621
    Xte, yte = feats(c21), growth2125
    aps = []
    for seed in (0, 1, 2):
        m = HistGradientBoostingClassifier(random_state=seed)
        m.fit(Xtr, ytr)
        s = m.predict_proba(Xte)[:, 1]
        aps.append({"ap": float(average_precision_score(yte, s)), "r@P0.7": recall_at_p(yte, s)})
    res["HGB_growth_21->25_trained_16->21"] = aps
    (OUT / "results_e01.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    lines = ["# E01-E06 cheap results (ON 392-526, 1km, Depth>=10%)",
             f"normalized counts: {res['counts']}",
             f"mean/seg: {[round(x,2) for x in res['mean_per_seg']]}"]
    for k, v in res.items():
        if k.startswith(("16", "21")):
            lines.append(f"- {k}: AP={v['ap']:.3f} base={v['base']:.3f} R@P0.7={v['recall@P0.7']:.3f} spear={v['spearman_past_future']:.3f}")
    h = res["HGB_growth_21->25_trained_16->21"]
    lines.append(f"- HGB growth AP: {[round(x['ap'],3) for x in h]} R@P0.7: {[round(x['r@P0.7'],3) for x in h]}")
    (OUT / "results_e01.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
