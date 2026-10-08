"""e16_ab: per-class persistence ranker (sanctioned ABC track, first engine).

Question: do past (a)/(b) rows predict future (a)/(b) rows per 100m cell?
Score B1ab = past ab-count per cell (R1 machinery: pipe+2m/0.5m/1h greedy,
depth>=10, corr rows; label = UNMATCHED future row with danger in {(a),(b)}).
Comparators: base prevalence + B1 corr-count on the same ab-labels (skill check:
does ab-history beat plain corr-history?).
Caveat (recorded, not hidden): pairs crossing ~2022 span the requirement-lowering
regime break, so train-regime ab rates differ from test-regime rates; per-section
recalibration applies. Small-n pairs never count (R4).
Read-only raw data. Writes experiments/results_e16.json (aggregates only).
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
from gtk1 import metrics as MET

DATA_ROOT = REPO.parent / "Данные для предварительного изучения"
PAIRS = {
    "ON 2021->2025": ("Омск-Новосибирск (392-526)", "2021", ("Аномалии.xlsx",),
                      "2025", ("Аномалии.xlsx", "Аномалии_.xlsx"), 1330),
    "SRTO-1608 2021->2024": ("СРТО-Омск_(1608 – 1717)", "2021", ("Аномалии.xls",),
                             "2024", ("Аномалии.xls", "Аномалии1.xls"), 1040),
    "PK1 2022->2025": ("Парабель-Кузбасс-1 (572-714)", "2022", ("Аномалии.xls",),
                       "2025", ("Аномалии.xls",), 1400),
}
CUT, AB = 10, ("(a)", "(b)")


def load(sdir, year, cands):
    d = DATA_ROOT / sdir / str(year)
    fp = next((d / n for n in cands if (d / n).exists()), None)
    assert fp, f"no anomaly file in {d}"
    df, _ = load_anomalies(str(fp))
    g = normalize(df)
    return g[(g["depth"] >= CUT) & g["corr"]].copy()


def run_pair(sdir, y0, c0, y1, c1, kmax):
    gp, gf = load(sdir, y0, c0), load(sdir, y1, c1)
    m = np.asarray(match_win(gp, gf, 2), dtype=bool)
    new = gf[~m]
    is_ab = new["danger"].astype(str).isin(AB).to_numpy()
    ck = lambda g: (g["dist"] // 100).astype(int).clip(0, kmax)
    y = (pd.Series(is_ab.astype(int), index=ck(new).to_numpy()).groupby(level=0).sum()
         .reindex(range(kmax + 1), fill_value=0).to_numpy() > 0).astype(int)
    pab = gp["danger"].astype(str).isin(AB)
    s_ab = (pab.groupby(ck(gp)).sum().reindex(range(kmax + 1), fill_value=0)
            .to_numpy().astype(float))
    s_b1 = (pd.Series(np.ones(len(gp)), index=ck(gp).to_numpy()).groupby(level=0).sum()
            .reindex(range(kmax + 1), fill_value=0).to_numpy().astype(float))
    r_ab = MET.ap_lift_ci(y, s_ab / max(s_ab.max(), 1))
    r_b1 = MET.ap_lift_ci(y, s_b1 / max(s_b1.max(), 1))
    d0, lo, hi = MET.paired_delta_ci(y, s_ab / max(s_ab.max(), 1), s_b1 / max(s_b1.max(), 1))
    return {
        "n_pos": int(y.sum()), "n": len(y),
        "B1ab": {"AP": r_ab["AP"], "base": r_ab["base"], "lift_CI": r_ab["lift_CI"]},
        "B1corr_on_ablabels": {"AP": r_b1["AP"], "base": r_b1["base"], "lift_CI": r_b1["lift_CI"]},
        "delta_ab_minus_corr": [d0, lo, hi],
    }


def clean(o):
    if isinstance(o, float) and o != o:
        return None
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    return o


def main():
    out = {"cut": CUT, "label": "unmatched future danger in {(a),(b)}", "pairs": {}}
    for name, (sdir, y0, c0, y1, c1, kmax) in PAIRS.items():
        r = run_pair(sdir, y0, c0, y1, c1, kmax)
        out["pairs"][name] = r
        print(f"{name}: n_pos={r['n_pos']} base={r['B1ab']['base']:.4f} "
              f"B1ab={r['B1ab']['AP']:.4f} B1corr={r['B1corr_on_ablabels']['AP']:.4f} "
              f"delta={r['delta_ab_minus_corr'][0]:+.4f} [{r['delta_ab_minus_corr'][1]:+.4f},"
              f"{r['delta_ab_minus_corr'][2]:+.4f}]")
    try:
        out["repro"] = {"git": subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
    except Exception:
        out["repro"] = {"git": "unknown"}
    (Path(__file__).resolve().parent / "results_e16.json").write_text(
        json.dumps(clean(out), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
