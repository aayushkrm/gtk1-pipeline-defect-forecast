"""repair_candidates: persistent-disappearance (repair) candidates, ON 2016->2021->2025.

Sanctioned rule (Evgeny/Vlad, meeting 08.10.2026): defect present, then gone for years
=> repaired. Commercial repair logs are sealed, so this reconstructs the schedule.

Method (R1 frozen semantics): greedy pipe+2m/0.5m/1h match on depth>=10 corr rows.
  vanished_1  = 2016 rows with no match in 2021 (reverse-greedy flag).
  persistent  = vanished_1 rows with no match in 2025 either -> repair candidates.
  reappeared  = vanished_1 rows matched in 2025 -> misalignment control (NOT repair).
Read-only raw data. Writes experiments/results_repair.json (counts + shares only).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize
from gtk1.match import match_win

DATA = REPO.parent / "Данные для предварительного изучения" / "Омск-Новосибирск (392-526)"
FILES = {"2016": ("Аномалии.xlsx",), "2021": ("Аномалии.xlsx",), "2025": ("Аномалии.xlsx", "Аномалии_.xlsx")}
CUT = 10


def load_year(year):
    d = DATA / str(year)
    fp = next((d / n for n in FILES[str(year)] if (d / n).exists()), None)
    assert fp, f"no anomaly file in {d}"
    df, meta = load_anomalies(str(fp))
    g = normalize(df)
    g = g[(g["depth"] >= CUT) & g["corr"]].copy()
    return g, meta["name"]


def main():
    g16, f16 = load_year(2016)
    g21, f21 = load_year(2021)
    g25, f25 = load_year(2025)
    m16_in_21 = np.asarray(match_win(g21, g16, 2), dtype=bool)
    van = g16[~m16_in_21].copy()
    mvan_in_25 = np.asarray(match_win(g25, van, 2), dtype=bool) if len(van) else np.array([], bool)
    pers = van[~mvan_in_25].copy()
    reap = van[mvan_in_25].copy()
    n_past = len(g16)
    out = {
        "pair": "ON 2016->2021->2025",
        "cut": CUT,
        "files": [f16, f21, f25],
        "n_past_d10_corr": n_past,
        "vanished_1_n": int(len(van)),
        "vanished_1_share": float(len(van) / max(n_past, 1)),
        "persistent_n": int(len(pers)),
        "persistent_share_of_past": float(len(pers) / max(n_past, 1)),
        "reappeared_n": int(len(reap)),
        "reappeared_share_of_vanished": float(len(reap) / max(len(van), 1)),
    }
    for tag, fr in (("persistent", pers), ("reappeared", reap)):
        dv = fr["danger"].astype(str) if "danger" in fr.columns else pd.Series([], dtype=str)
        out[f"{tag}_danger"] = {k: int((dv == k).sum()) for k in ("(a)", "(b)", "(c)")}
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    (Path(__file__).resolve().parent / "results_repair.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    print(f"past={n_past} vanished1={len(van)} ({out['vanished_1_share']:.3f}) "
          f"persistent={len(pers)} ({out['persistent_share_of_past']:.3f}) "
          f"reappeared={len(reap)} ({out['reappeared_share_of_vanished']:.3f})")
    print("danger persistent:", out["persistent_danger"], "reappeared:", out["reappeared_danger"])


if __name__ == "__main__":
    main()
