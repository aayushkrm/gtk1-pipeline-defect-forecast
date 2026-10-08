"""kbd_flag: never-validated secondary hypothesis (docs/PROBLEM.md:28).

Question: does past pipe high-risk flag KBD<0.9 (or danger a/b) mark
100-m cells with higher future ab-rate (danger (a)/(b) rows)?

Scope: PAST = all normalized rows (no depth/corr cut); cells 100 m with
kmax clip (1330 ON / 1040 SRTO); FUTURE = all normalized rows of the next
survey; future ab = danger in {(a),(b)}. Rates are ab rows per cell group
as shares of future rows, plus raw counts. Small-n flagged groups
(<20 cells) are flagged, not ranked. CPU only. Read-only raw data.
Writes experiments/results_kbd.json (aggregates only).
R1 frozen path: src.gtk1.io loader/normalizer (+ src.gtk1.match import).
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
from gtk1.io import load_anomalies, normalize  # noqa: E402
from gtk1.match import match_win  # noqa: E402  (R1 frozen matcher; not used: cell rates need no matching)

DATA_ROOT = REPO.parent / "Данные для предварительного изучения"
PAIRS = {
    "ON 2021->2025": (
        "Омск-Новосибирск (392-526)", "2021", ("Аномалии.xlsx",),
        "2025", ("Аномалии_.xlsx", "Аномалии.xlsx"), 1330,
    ),
    "SRTO-1608 2021->2024": (
        "СРТО-Омск_(1608 – 1717)", "2021", ("Аномалии.xls",),
        "2024", ("Аномалии1.xls", "Аномалии.xls"), 1040,
    ),
}
WIDTH_M = 100
KBD_THR = 0.9
AB = ("(a)", "(b)")
SMALL_N_CELLS = 20


def load_all(sdir, year, cands):
    d = DATA_ROOT / sdir / str(year)
    fp = next((d / n for n in cands if (d / n).exists()), None)
    assert fp is not None, f"no anomaly file in {d}"
    df, _ = load_anomalies(str(fp), header=3)
    g = normalize(df)
    return g, fp.name


def cells_of(g, kmax):
    return (g["dist"] // WIDTH_M).astype(int).clip(0, kmax).to_numpy()


def group_stats(fcell, fab, mask_cells, n_cells_total):
    n_cells = int(len(mask_cells))
    members = np.asarray(sorted(mask_cells)) if len(mask_cells) else np.asarray([], dtype=int)
    in_g = np.isin(fcell, members)
    n_rows = int(in_g.sum())
    n_ab = int((in_g & fab).sum())
    n_rows_out = int((~in_g).sum())
    n_ab_out = int(((~in_g) & fab).sum())
    rate_in = (n_ab / n_rows) if n_rows else float("nan")
    rate_out = (n_ab_out / n_rows_out) if n_rows_out else float("nan")
    n_fut = len(fcell)
    return {
        "n_cells": n_cells,
        "small_n": bool(n_cells < SMALL_N_CELLS),
        "flagged": {
            "n_future_rows": n_rows,
            "n_future_ab": n_ab,
            "ab_rate_within": rate_in,
            "ab_share_of_all_future": (n_ab / n_fut) if n_fut else float("nan"),
        },
        "unflagged": {
            "n_cells": int(n_cells_total - n_cells),
            "n_future_rows": n_rows_out,
            "n_future_ab": n_ab_out,
            "ab_rate_within": rate_out,
            "ab_share_of_all_future": (n_ab_out / n_fut) if n_fut else float("nan"),
        },
        "diff_within_flagged_minus_unflagged": rate_in - rate_out,
        "ratio_within_flagged_over_unflagged": (rate_in / rate_out)
        if rate_out and np.isfinite(rate_in) and np.isfinite(rate_out) and rate_out != 0
        else float("nan"),
    }


def run_pair(sdir, y0, c0, y1, c1, kmax):
    gp, past_file = load_all(sdir, y0, c0)
    gf, fut_file = load_all(sdir, y1, c1)
    n_cells_total = kmax + 1
    pcell = cells_of(gp, kmax)
    fcell = cells_of(gf, kmax)
    fab = gf["danger"].astype(str).isin(AB).to_numpy()
    pab = gp["danger"].astype(str).isin(AB).to_numpy()
    kbd = gp["kbd"].to_numpy(dtype=float)
    covered = np.isfinite(kbd)
    lt = covered & (kbd < KBD_THR)
    kbd_cells = set(np.unique(pcell[lt]).tolist()) if lt.any() else set()
    ab_cells = set(np.unique(pcell[pab]).tolist()) if pab.any() else set()
    n_over_past = int(((gp["dist"].to_numpy(dtype=float)) // WIDTH_M > kmax).sum())
    n_over_fut = int(((gf["dist"].to_numpy(dtype=float)) // WIDTH_M > kmax).sum())
    past = {
        "n_rows": int(len(gp)),
        "n_kbd_covered": int(covered.sum()),
        "coverage": float(covered.mean()) if len(gp) else float("nan"),
        "n_kbd_lt09_rows": int(lt.sum()),
        "n_flagged_cells": int(len(kbd_cells)),
        "flagged_share_cells": float(len(kbd_cells) / n_cells_total),
        "small_n": bool(len(kbd_cells) < SMALL_N_CELLS),
    }
    past_ab = {
        "n_ab_rows": int(pab.sum()),
        "n_ab_cells": int(len(ab_cells)),
        "ab_share_cells": float(len(ab_cells) / n_cells_total),
        "small_n": bool(len(ab_cells) < SMALL_N_CELLS),
    }
    future = {
        "n_rows": int(len(gf)),
        "n_ab_rows": int(fab.sum()),
        "ab_share_overall": float(fab.mean()) if len(gf) else float("nan"),
    }
    return {
        "kmax": kmax,
        "n_cells": n_cells_total,
        "past_file": past_file,
        "future_file": fut_file,
        "n_overrun_clipped_past": n_over_past,
        "n_overrun_clipped_future": n_over_fut,
        "past": past,
        "past_ab": past_ab,
        "future": future,
        "kbd_flag_cells_sorted": sorted(kbd_cells),
        "past_ab_cells_sorted": sorted(ab_cells),
        "kbd_flag": group_stats(fcell, fab, kbd_cells, n_cells_total),
        "ab_flag": group_stats(fcell, fab, ab_cells, n_cells_total),
    }


def clean(o):
    if isinstance(o, float) and (o != o or o in (float("inf"), float("-inf"))):
        return None
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    v = o.item() if isinstance(o, (np.integer, np.floating, np.bool_)) else o
    if isinstance(v, float) and (v != v or v in (float("inf"), float("-inf"))):
        return None
    return v


def main():
    t0 = time.perf_counter()
    out = {
        "cell_width_m": WIDTH_M,
        "kbd_threshold": KBD_THR,
        "danger_ab": list(AB),
        "scope": "all normalized rows, no depth/corr cut; "
        "cells (dist//100).clip(0,kmax); future ab = danger in {(a),(b)} "
        "over all future normalized rows",
        "small_n_cells": SMALL_N_CELLS,
        "pairs": {},
    }
    for name, (sdir, y0, c0, y1, c1, kmax) in PAIRS.items():
        r = run_pair(sdir, y0, c0, y1, c1, kmax)
        out["pairs"][name] = r
        kf, af = r["kbd_flag"], r["ab_flag"]
        print(
            f"{name}: past_n={r['past']['n_rows']} cov={r['past']['coverage']:.4f} "
            f"kbd_cells={r['past']['n_flagged_cells']}/{r['n_cells']} "
            f"fut_ab={r['future']['n_ab_rows']}/{r['future']['n_rows']} "
            f"kbd_flag_rate={kf['flagged']['ab_rate_within']:.4f} "
            f"(n={kf['flagged']['n_future_rows']},ab={kf['flagged']['n_future_ab']}) vs "
            f"unflag={kf['unflagged']['ab_rate_within']:.4f} "
            f"(n={kf['unflagged']['n_future_rows']},ab={kf['unflagged']['n_future_ab']}) | "
            f"ab_flag_rate={af['flagged']['ab_rate_within']:.4f} "
            f"(cells={r['past_ab']['n_ab_cells']},n={af['flagged']['n_future_rows']},"
            f"ab={af['flagged']['n_future_ab']}) vs "
            f"unflag={af['unflagged']['ab_rate_within']:.4f} "
            f"(n={af['unflagged']['n_future_rows']},ab={af['unflagged']['n_future_ab']})"
        )
    out["runtime_s"] = time.perf_counter() - t0
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    (Path(__file__).resolve().parent / "results_kbd.json").write_text(
        json.dumps(clean(out), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
