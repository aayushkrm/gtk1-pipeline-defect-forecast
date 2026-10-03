"""E04b: matcher x cut robustness matrix + vanished audit (reviewer gate before E05).
Grid: dd in {1,2,5}m x cuts {8,10,12,15}% @100m matched-new binary, ON train 16->21 / test 21->25.
Plus greedy-vs-Hungarian agreement at base (dd=2, cut=10) and depth histograms
(matched / new / vanished medians). Past-only B1 AP vs base per cell.
Read-only raw data. De-identified aggregates only.
"""
import json, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0, str(Path(__file__).resolve().parent))
import e02_matched as E
from sklearn.metrics import average_precision_score
from scipy.optimize import linear_sum_assignment

OUT = Path(__file__).resolve().parent
REPO = Path(__file__).resolve().parents[1]
W, KMAX = 100, 1330

def ck(g):
    return (g["dist"] // W).astype(int).clip(0, KMAX)

def match_win(past, fut, dd, doff=0.5, dh=1, hungarian=False):
    fut_m = np.zeros(len(fut), bool)
    for pipe, fi in fut.groupby("pipe").groups.items():
        F = fut.loc[fi]
        P = past[past["pipe"] == pipe]
        if P.empty:
            continue
        if not hungarian:
            for j, f in F.iterrows():
                ddA = (P["dist"] - f["dist"]).abs().values
                cand = np.where(ddA <= dd)[0]
                if len(cand) == 0:
                    continue
                do = np.abs(P.iloc[cand]["off"].values - f["off"])
                do = np.where(pd.isna(P.iloc[cand]["off"].values) | pd.isna(f["off"]), 0.0, do)
                dhv = P.iloc[cand]["h"].values
                d = np.abs(dhv - f["h"]) % 12
                dhA = np.where((dhv < 0) | (f["h"] < 0), 0.0, np.minimum(d, 12 - d))
                ok = (do <= doff) & (dhA <= dh)
                if not ok.any():
                    continue
                cost = ddA[cand][ok] + 2 * do[ok] + 0.5 * dhA[ok]
                best = cand[ok][int(np.argmin(cost))]
                P = P.drop(P.index[best])
                fut_m[fut.index.get_loc(j)] = True
        else:
            Pv, Fv = P.reset_index(drop=True), F.reset_index()
            C = np.full((len(Pv), len(Fv)), 1e9)
            for a, (_, p) in enumerate(Pv.iterrows()):
                for b, (_, f) in enumerate(Fv.iterrows()):
                    d0 = abs(p["dist"] - f["dist"])
                    if d0 > dd:
                        continue
                    do = abs(p["off"] - f["off"]) if pd.notna(p["off"]) and pd.notna(f["off"]) else 0.0
                    if do > doff:
                        continue
                    if p["h"] >= 0 and f["h"] >= 0:
                        dd2 = abs(p["h"] - f["h"]) % 12
                        dhA = min(dd2, 12 - dd2)
                    else:
                        dhA = 0.0
                    if dhA > dh:
                        continue
                    C[a, b] = d0 + 2 * do + 0.5 * dhA
            try:
                ra, ca = linear_sum_assignment(C)
                for a, b in zip(ra, ca):
                    if C[a, b] < 1e8:
                        fut_m[fut.index.get_loc(Fv.loc[b, "index"])] = True
            except Exception:
                pass
    return fut_m

def run():
    import pandas as pd
    d16, _ = E.load_anom(2016); d21, _ = E.load_anom(2021); d25, _ = E.load_anom(2025)
    g16, g21, g25 = E.norm(d16), E.norm(d21), E.norm(d25)
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
    r16, r21, r25 = raw(d16), raw(d21), raw(d25)
    res = {"cells": {}, "depth_audit": {}, "hungarian": {}}
    for cut in (8, 10, 12, 15):
        f = lambda g: g[g["depth"] >= cut].copy()
        a16, a21, a25 = f(r16), f(r21), f(r25)
        res["depth_audit"][str(cut)] = {
            "n16": int(len(a16)), "n21": int(len(a21)), "n25": int(len(a25)),
            "med16": float(a16["depth"].median()), "med21": float(a21["depth"].median()),
            "med25": float(a25["depth"].median())}
        for dd in (1, 2, 5):
            m_tr = match_win(a16, a21, dd); m_te = match_win(a21, a25, dd)
            ytr = (a21[~m_tr][a21[~m_tr]["corr"]].groupby(ck(a21[~m_tr][a21[~m_tr]["corr"]]))
                   .size().reindex(range(KMAX + 1), fill_value=0).values > 0).astype(int)
            yte = (a25[~m_te][a25[~m_te]["corr"]].groupby(ck(a25[~m_te][a25[~m_te]["corr"]]))
                   .size().reindex(range(KMAX + 1), fill_value=0).values > 0).astype(int)
            ptr = (a16[a16["corr"]].groupby(ck(a16[a16["corr"]])).size()
                   .reindex(range(KMAX + 1), fill_value=0).values.astype(float))
            pte = (a21[a21["corr"]].groupby(ck(a21[a21["corr"]])).size()
                   .reindex(range(KMAX + 1), fill_value=0).values.astype(float))
            ap = float(average_precision_score(yte, pte / max(pte.max(), 1))) if yte.sum() else 0.0
            res["cells"][f"cut{cut}_dd{dd}"] = {
                "match_tr": float(m_tr.mean()), "match_te": float(m_te.mean()),
                "prev_tr": float(ytr.mean()), "prev_te": float(yte.mean()),
                "B1_AP": ap, "base": float(yte.mean())}
    # greedy vs hungarian agreement + depth audit at base
    f = lambda g: g[g["depth"] >= 10].copy()
    a16, a21, a25 = f(r16), f(r21), f(r25)
    mg = match_win(a21, a25, 2); mh = match_win(a21, a25, 2, hungarian=True)
    res["hungarian"] = {"agree_greedy_hungarian": float((mg == mh).mean()),
                        "match_greedy": float(mg.mean()), "match_hungarian": float(mh.mean())}
    new = a25[~mg]
    # NOTE (limitation): vanished-past rows are not directly flagged by the
    # forward matcher (it flags future rows); vanished-frac here = 1 - match_rate
    # reported in E02. A reverse-match vanished depth audit is still open.
    res["depth_audit"]["base10"] = {"med_matched_fut": float(a25[mg]["depth"].median()),
        "med_new_corr": float(new[new["corr"]]["depth"].median()),
        "med_past_all": float(a21["depth"].median()),
        "med_past_corr": float(a21[a21["corr"]]["depth"].median())}
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    res["repro"] = {"git": gh}
    (OUT / "results_e04b.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    L = ["# E04b matcher x cut matrix @100m matched-new (ON)"]
    for cut in (8, 10, 12, 15):
        row = " | ".join(f"dd{dd}: m{e}=({res['cells'][f'cut{cut}_dd{dd}']['match_tr']:.2f}/{res['cells'][f'cut{cut}_dd{dd}']['match_te']:.2f}) "
                         f"p=({res['cells'][f'cut{cut}_dd{dd}']['prev_tr']:.2f}/{res['cells'][f'cut{cut}_dd{dd}']['prev_te']:.2f}) "
                         f"B1={res['cells'][f'cut{cut}_dd{dd}']['B1_AP']:.3f}/b={res['cells'][f'cut{cut}_dd{dd}']['base']:.3f}"
                         for dd, e in ((1, 1), (2, 2), (5, 5)))
        L.append(f"- cut>={cut}%: {row}")
    L.append(f"- greedy-vs-Hungarian agree: {res['hungarian']['agree_greedy_hungarian']:.3f} "
             f"(g {res['hungarian']['match_greedy']:.3f} / h {res['hungarian']['match_hungarian']:.3f})")
    L.append(f"- depths base10: {res['depth_audit']['base10']}")
    (OUT / "results_e04b.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    run()
