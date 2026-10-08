"""persist_by_char: defect persistence per character class across surveys.

Pairs: ON 2021->2025, SRTO-1608 2021->2024. Frozen R1 matcher
(pipe + 2m / 0.5m / 1h greedy via src.gtk1.match.match_win),
depth>=10 filter before match. Global match on full frames, then
breakdown per char class (top 8 by past count + other).
Read-only raw data. Aggregates only.
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
TOP_K = 8
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


def rate(a, b):
    if not b:
        return None
    r = float(a) / float(b)
    return r if np.isfinite(r) else None


def one_pair(tag, fp_past, fp_fut):
    dp, _ = load_anomalies(fp_past, sheet="Аномалии", header=3)
    df, _ = load_anomalies(fp_fut, sheet="Аномалии", header=3)
    gp_all = normalize(dp)
    gf_all = normalize(df)
    past = gp_all[gp_all["depth"] >= CUT].copy()
    fut = gf_all[gf_all["depth"] >= CUT].copy()
    fut_m = match_win(past, fut, DD, DOFF, DH)  # flags FUTURE rows
    past_m = match_win(fut, past, DD, DOFF, DH)  # flags PAST rows w/ partner
    assert len(fut_m) == len(fut) and len(past_m) == len(past)
    fut = fut.copy()
    past = past.copy()
    fut["matched"] = np.asarray(fut_m, dtype=bool)
    past["matched"] = np.asarray(past_m, dtype=bool)
    # top classes by past count
    vc = past["char"].value_counts()
    top = list(vc.head(TOP_K).index)
    past["cls"] = past["char"].where(past["char"].isin(top), "other")
    fut["cls"] = fut["char"].where(fut["char"].isin(top), "other")
    order = top + (["other"] if (len(vc) > TOP_K) else [])
    rows = []
    for c in order:
        pp = past[past["cls"] == c]
        ff = fut[fut["cls"] == c]
        n_p = int(len(pp))
        n_mp = int(pp["matched"].sum())
        n_f = int(len(ff))
        n_mf = int(ff["matched"].sum())
        n_new = n_f - n_mf
        rows.append({
            "char": str(c),
            "n_past": n_p,
            "n_matched_past": n_mp,
            "match_rate_past": clean(rate(n_mp, n_p)),
            "n_vanished": n_p - n_mp,
            "n_fut": n_f,
            "n_matched_fut": n_mf,
            "n_new": n_new,
            "new_rate_fut": clean(rate(n_new, n_f)),
            "small_n": bool(n_p < SMALL_N),
        })
    return {
        "files": [fp_past.name, fp_fut.name],
        "cut": CUT,
        "n_past": int(len(past)),
        "n_fut": int(len(fut)),
        "match_rate_past": clean(rate(int(past["matched"].sum()), len(past))),
        "match_rate_past_def": "reverse-greedy: past rows with a future match / all past rows",
        "match_rate_fut": clean(rate(int(fut["matched"].sum()), len(fut))),
        "n_classes_union": int(pd.unique(pd.concat([past["char"], fut["char"]])).size),
        "classes": rows,
    }


def run():
    t0 = time.time()
    out = {"params": {"depth_min": CUT, "dd": DD, "doff": DOFF, "dh": DH,
                       "greedy": True, "top_k": TOP_K, "small_n": SMALL_N},
           "pairs": {}}
    for tag, (fp, ff) in PAIRS.items():
        out["pairs"][tag] = one_pair(tag, fp, ff)
    try:
        gh = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    except Exception:
        gh = "nogit"
    out["repro"] = {"git": gh, "runtime_s": round(time.time() - t0, 1)}
    (OUT / "results_persist_char.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False, allow_nan=False))
    for tag, p in out["pairs"].items():
        print(f"== {tag} files={p['files']} n_past={p['n_past']} n_fut={p['n_fut']} "
              f"match_past={p['match_rate_past']:.3f} match_fut={p['match_rate_fut']:.3f}")
        for r in sorted(p["classes"], key=lambda d: (d["match_rate_past"] is None, d["match_rate_past"])):
            flag = " SMALL-N" if r["small_n"] else ""
            print(f"  {r['char'][:40]!r:44} past={r['n_past']:5d} matched={r['n_matched_past']:5d} "
                  f"rate={r['match_rate_past'] if r['match_rate_past'] is None else round(r['match_rate_past'], 3)!s:>7} "
                  f"vanished={r['n_vanished']:5d} | fut={r['n_fut']:5d} new={r['n_new']:5d} "
                  f"newrate={r['new_rate_fut'] if r['new_rate_fut'] is None else round(r['new_rate_fut'], 3)!s:>7}{flag}")
    print(f"wrote results_persist_char.json in {out['repro']['runtime_s']}s git={gh}")


if __name__ == "__main__":
    run()
