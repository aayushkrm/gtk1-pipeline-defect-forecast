"""match: per-pipe greedy + Hungarian defect matching (consolidated from e04b; identical).
Rule: same pipe + |dd|<=win + |doff|<=0.5 + circular |dh|<=1h.
Cost: |dd| + 2|doff| + 0.5|dh|. No depth tie-break (leakage). Returns future-row mask.
"""
import numpy as np
import pandas as pd


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
            from scipy.optimize import linear_sum_assignment
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
            except Exception as e:
                raise RuntimeError(
                    f"match_win Hungarian failed: pipe={pipe!r} P={len(Pv)} F={len(Fv)} C={C.shape}: {e}"
                ) from e
            for a, b in zip(ra, ca):
                if C[a, b] < 1e8:
                    fut_m[fut.index.get_loc(Fv.loc[b, "index"])] = True
    return fut_m
