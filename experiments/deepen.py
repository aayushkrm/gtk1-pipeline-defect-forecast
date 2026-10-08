"""deepen: defect deepening on matched pairs (how defects develop).

Pairs: ON 2021->2025, SRTO-1608 2021->2024. Frozen R1 matcher:
same pipe + |dd|<=2m + |doff|<=0.5m + circular |dh|<=1h greedy,
depth>=10 both sides before match. Loads via src.gtk1.io.
Local greedy loop mirrors src.gtk1.match.match_win exactly
(same pipe groups, same future-row order, same cost
|dd|+2|doff|+0.5|dh|, same argmin) but records pair indices;
match.py is not modified. Parity vs match_win is asserted.
Per pair: d_depth = future_depth - past_depth (pp).
Overall + per past-char class: n_pairs, median/IQR/mean,
share deepened (>0), unchanged (=0), shallower (<0).
Small-n classes (<20 pairs) flagged, not ranked.
Read-only raw data. CPU only. Aggregates only.
Interpretation: shallower readings bound measurement noise;
deepening mixes growth + tool differences. Claim neither
as pure growth.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize
from gtk1.match import match_win

BASE = REPO.parent / "Данные для предварительного изучения"
OUT = Path(__file__).resolve().parent

CUT = 10
DD, DOFF, DH = 2.0, 0.5, 1
SMALL_N = 20

PAIRS = {
    "ON_2021_2025": (
        BASE / "Омск-Новосибирск (392-526)" / "2021" / "Аномалии.xlsx",
        BASE / "Омск-Новосибирск (392-526)" / "2025" / "Аномалии_.xlsx",
    ),
    "SRTO1608_2021_2024": (
        BASE / "СРТО-Омск_(1608 – 1717)" / "2021" / "Аномалии.xls",
        BASE / "СРТО-Омск_(1608 – 1717)" / "2024" / "Аномалии1.xls",
    ),
}

INTERP = ("shallower readings bound measurement noise; deepening mixes "
          "growth + tool differences. Claim neither as pure growth.")


def clean(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        f = float(v)
        if not np.isfinite(f):
            return None
        return f
    if isinstance(v, (np.bool_, bool)):
        return bool(v)
    return v


def greedy_pairs(past, fut, dd=DD, doff=DOFF, dh=DH):
    """Future-driven greedy mirror of match_win; records (past_idx, fut_idx)."""
    pairs = []
    fut_m = np.zeros(len(fut), bool)
    for pipe, fi in fut.groupby("pipe").groups.items():
        F = fut.loc[fi]
        P = past[past["pipe"] == pipe]
        if P.empty:
            continue
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
            best_label = P.index[best]
            pairs.append((best_label, j))
            P = P.drop(P.index[best])
            fut_m[fut.index.get_loc(j)] = True
    return pairs, fut_m


def agg(d):
    d = np.asarray(d, dtype=float)
    n = int(len(d))
    if n == 0:
        return {"n_pairs": 0, "median": None, "q1": None, "q3": None,
                "iqr": None, "mean": None, "share_deepened": None,
                "share_unchanged": None, "share_shallower": None}
    q1, med, q3 = float(np.percentile(d, 25)), float(np.median(d)), float(np.percentile(d, 75))
    return {"n_pairs": n, "median": clean(med), "q1": clean(q1), "q3": clean(q3),
            "iqr": clean(q3 - q1), "mean": clean(float(np.mean(d))),
            "share_deepened": clean(float((d > 0).mean())),
            "share_unchanged": clean(float((d == 0).mean())),
            "share_shallower": clean(float((d < 0).mean()))}


def one_pair(fp_past, fp_fut):
    dp, _ = load_anomalies(fp_past, sheet="Аномалии", header=3)
    df, _ = load_anomalies(fp_fut, sheet="Аномалии", header=3)
    past = normalize(dp)
    fut = normalize(df)
    past = past[past["depth"] >= CUT].copy()
    fut = fut[fut["depth"] >= CUT].copy()
    ref = np.asarray(match_win(past, fut, DD, DOFF, DH))
    pairs, fut_m = greedy_pairs(past, fut)
    assert (np.asarray(fut_m) == ref).all(), "greedy mirror parity FAIL vs match_win"
    dd_list, cls_list = [], []
    for pi, fi in pairs:
        dd_list.append(float(fut.loc[fi, "depth"] - past.loc[pi, "depth"]))
        cls_list.append(str(past.loc[pi, "char"]))
    dd_arr = np.array(dd_list, dtype=float)
    out = {"files": [fp_past.name, fp_fut.name], "cut": CUT,
           "n_past": int(len(past)), "n_fut": int(len(fut)),
           "n_pairs": int(len(pairs)),
           "match_rate_fut": clean(float(np.mean(fut_m)) if len(fut_m) else None),
           "match_rate_past": clean(float(len(pairs) / len(past)) if len(past) else None),
           "parity_vs_match_win": "IDENTICAL",
           "overall": agg(dd_arr), "by_char": []}
    if len(pairs):
        dfp = pd.DataFrame({"cls": cls_list, "dd": dd_arr})
        order = dfp.groupby("cls").size().sort_values(ascending=False).index.tolist()
        for c in order:
            vv = dfp.loc[dfp["cls"] == c, "dd"].to_numpy(dtype=float)
            a = agg(vv)
            a["char"] = str(c)
            a["small_n"] = bool(a["n_pairs"] < SMALL_N)
            out["by_char"].append(a)
    return out


def run():
    t0 = time.time()
    out = {"params": {"depth_min": CUT, "dd": DD, "doff": DOFF, "dh": DH,
                      "greedy": True, "small_n": SMALL_N, "char_source": "past",
                      "d_depth": "future_depth - past_depth (pp)",
                      "match": "same pipe + |dd|<=2m + |doff|<=0.5m + circular |dh|<=1h"},
           "pairs": {},
           "interpretation": INTERP}
    for tag, (fp, ff) in PAIRS.items():
        out["pairs"][tag] = one_pair(fp, ff)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    # git may be unavailable (no repo); sanitize empty to nogit-like marker
    if not gh:
        gh = "nogit"
    out["repro"] = {"git": gh, "runtime_s": round(time.time() - t0, 1)}
    (OUT / "results_deepen.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False))
    for tag, p in out["pairs"].items():
        o = p["overall"]
        print(f"== {tag} files={p['files']} n_past={p['n_past']} n_fut={p['n_fut']} "
              f"pairs={p['n_pairs']} parity={p['parity_vs_match_win']}")
        print(f"   overall: median={o['median']} IQR=[{o['q1']},{o['q3']}] "
              f"mean={o['mean']} deepened={o['share_deepened']} "
              f"unchanged={o['share_unchanged']} shallower={o['share_shallower']}")
        for r in p["by_char"]:
            flag = " SMALL-N" if r["small_n"] else ""
            print(f"   {r['char'][:36]!r:40} n={r['n_pairs']:5d} med={r['median']} "
                  f"IQR=[{r['q1']},{r['q3']}] mean={r['mean']} "
                  f"deep={r['share_deepened']} same={r['share_unchanged']} "
                  f"shal={r['share_shallower']}{flag}")
    print(f"note: {INTERP}")
    print(f"wrote results_deepen.json in {out['repro']['runtime_s']}s git={gh}")


if __name__ == "__main__":
    run()
