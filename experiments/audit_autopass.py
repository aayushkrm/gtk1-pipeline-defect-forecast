"""Audit: fraction of matcher matches decided by auto-pass (additive, stdout only).

Auto-pass = off-window passed because off is NaN on either side, or h-window
passed because h < 0 (missing orientation) on either side. Instruments a copy
of e04b_robust.match_win greedy loop (same logic as e02_matched.match) on the
ON train (2016->2021) and test (2021->2025) pairs. Writes nothing to
results_e*.json. Read-only on raw data.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e02_matched as E

DD, DOFF, DH = 2.0, 0.5, 1


def audit(past, fut):
    n_match = 0
    off_auto = 0
    h_auto = 0
    either_auto = 0
    P = None
    fut_m = np.zeros(len(fut), bool)
    for pipe, fi in fut.groupby("pipe").groups.items():
        F = fut.loc[fi]
        P = past[past["pipe"] == pipe]
        if P.empty:
            continue
        for j, f in F.iterrows():
            ddA = (P["dist"] - f["dist"]).abs().values
            cand = np.where(ddA <= DD)[0]
            if len(cand) == 0:
                continue
            do = np.abs(P.iloc[cand]["off"].values - f["off"])
            do = np.where(pd.isna(P.iloc[cand]["off"].values) | pd.isna(f["off"]), 0.0, do)
            dhv = P.iloc[cand]["h"].values
            d = np.abs(dhv - f["h"]) % 12
            dhA = np.where((dhv < 0) | (f["h"] < 0), 0.0, np.minimum(d, 12 - d))
            ok = (do <= DOFF) & (dhA <= DH)
            if not ok.any():
                continue
            cost = ddA[cand][ok] + 2 * do[ok] + 0.5 * dhA[ok]
            best = cand[ok][int(np.argmin(cost))]
            prow = P.iloc[best]
            off_a = bool(pd.isna(prow["off"]) or pd.isna(f["off"]))
            h_a = bool(prow["h"] < 0 or f["h"] < 0)
            n_match += 1
            off_auto += off_a
            h_auto += h_a
            either_auto += (off_a or h_a)
            P = P.drop(P.index[best])
            fut_m[fut.index.get_loc(j)] = True
    n_fut = len(fut)
    return {
        "n_fut": n_fut,
        "n_match": n_match,
        "match_rate": n_match / max(n_fut, 1),
        "frac_off_auto_of_match": off_auto / max(n_match, 1),
        "frac_h_auto_of_match": h_auto / max(n_match, 1),
        "frac_either_auto_of_match": either_auto / max(n_match, 1),
    }


def main():
    d16, _ = E.load_anom(2016)
    d21, _ = E.load_anom(2021)
    d25, _ = E.load_anom(2025)
    g16, g21, g25 = E.norm(d16), E.norm(d21), E.norm(d25)
    for tag, gp, gf in (("train 2016->2021", g16, g21), ("test 2021->2025", g21, g25)):
        r = audit(gp, gf)
        print(f"ON {tag}: n_fut={r['n_fut']} n_match={r['n_match']} "
              f"match_rate={r['match_rate']:.4f} "
              f"off_auto={r['frac_off_auto_of_match']:.4f} "
              f"h_auto={r['frac_h_auto_of_match']:.4f} "
              f"either_auto={r['frac_either_auto_of_match']:.4f}")


if __name__ == "__main__":
    main()
