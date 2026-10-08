"""repair_cells: per-cell persistent-candidate maps (repair-schedule handover, Fyodor).

R1 frozen semantics reused exactly as in experiments/repair_candidates.py:
greedy pipe+2m/0.5m/1h match on depth>=10 corr rows (reverse-greedy flags).
This file imports load_year/SECTIONS/CUT from repair_candidates and mirrors its
run_triple matching lines verbatim; it only adds 100m-cell binning on top.
CPU only. Raw data is read-only; never commit raw data.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "experiments"))
import repair_candidates as RC
from gtk1.match import match_win

WIDTH_M = 100
TASKS = {
    "on": {"triple": "ON 2016->2021->2025", "kmax": 1330,
           "out": REPO / "triage" / "repair_cells_on.json"},
    "srto": {"triple": "SRTO-1608 2016->2021->2024", "kmax": 1040,
             "out": REPO / "triage" / "repair_cells_srto.json"},
}
EXPECTED_PERSISTENT = {
    "ON 2016->2021->2025": 406,
    "SRTO-1608 2016->2021->2024": 121,
}
MEANING = ("persistent disappearance across two later surveys = repair candidate "
           "per sanctioned rule; reappeared = misalignment control, not repair.")
METHOD = ("R1 frozen: greedy pipe+2m/0.5m/1h match on depth>=10 corr rows "
          "(reverse-greedy flags), identical to experiments/repair_candidates.py run_triple.")


def per_cell_counts(frame, kmax):
    idx = range(kmax + 1)
    if frame is None or len(frame) == 0:
        return np.zeros(kmax + 1, dtype=int)
    ck = (frame["dist"] // WIDTH_M).astype(int).clip(0, kmax)
    return frame.groupby(ck).size().reindex(idx, fill_value=0).to_numpy(dtype=int)


def run_triple_cells(section_dir, years_files, kmax):
    years = sorted(years_files)
    frames, names = [], []
    for y in years:
        g, fn = RC.load_year(section_dir, y, years_files[y])
        frames.append(g)
        names.append(fn)
    g0, g1, g2 = frames
    # Verbatim mirror of repair_candidates.run_triple matching lines:
    m0_in_1 = np.asarray(match_win(g1, g0, 2), dtype=bool)
    van = g0[~m0_in_1].copy()
    mvan_in_2 = np.asarray(match_win(g2, van, 2), dtype=bool) if len(van) else np.array([], bool)
    pers = van[~mvan_in_2].copy()
    reap = van[mvan_in_2].copy()
    return {"years": years, "files": names, "g0n": int(len(g0)),
            "van_n": int(len(van)), "pers": pers, "reap": reap}


def git_hash():
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()
    except Exception:
        return "unknown"


def main():
    ref = json.loads((REPO / "experiments" / "results_repair.json").read_text())
    t0 = time.time()
    for _tag, cfg in TASKS.items():
        triple = cfg["triple"]
        kmax = cfg["kmax"]
        section_dir, years_files = RC.SECTIONS[triple]
        r = run_triple_cells(section_dir, years_files, kmax)
        pcell = per_cell_counts(r["pers"], kmax)
        rcell = per_cell_counts(r["reap"], kmax)
        total = int(pcell.sum())
        reappeared_total = int(rcell.sum())
        expected = EXPECTED_PERSISTENT[triple]
        ref_n = int(ref["sections"][triple]["persistent_n"])
        assert total == expected, f"{triple}: per-cell total {total} != asserted {expected}"
        assert total == ref_n, f"{triple}: per-cell total {total} != results_repair.json {ref_n}"
        assert reappeared_total == int(ref["sections"][triple]["reappeared_n"]), (
            f"{triple}: reappeared total {reappeared_total} != results_repair.json "
            f"{ref['sections'][triple]['reappeared_n']}")
        out = {
            "section": triple,
            "section_dir": section_dir,
            "years": r["years"],
            "kmax": kmax,
            "n_cells": kmax + 1,
            "cell_width_m": WIDTH_M,
            "cut": RC.CUT,
            "method": METHOD,
            "meaning": MEANING,
            "persistent_per_cell": [int(v) for v in pcell],
            "persistent_total": total,
            "cells_with_candidates": int((pcell > 0).sum()),
            "reappeared_per_cell": [int(v) for v in rcell],
            "reappeared_total": reappeared_total,
            "cells_with_reappeared": int((rcell > 0).sum()),
            "provenance": {"years": r["years"], "files": r["files"],
                           "section_dir": section_dir,
                           "source": "experiments/repair_candidates.py run_triple logic (imported, not modified)",
                           "ref_results": "experiments/results_repair.json"},
            "repro": {"git": git_hash()},
        }
        cfg["out"].write_text(json.dumps(out, indent=2, ensure_ascii=False))
        print(f"{triple}: persistent_total={total} (assert {expected}) "
              f"cells_with_candidates={out['cells_with_candidates']} "
              f"reappeared_total={reappeared_total} -> {cfg['out'].name}")
    print(f"done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
