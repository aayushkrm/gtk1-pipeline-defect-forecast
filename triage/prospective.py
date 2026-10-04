"""Prospective watchlist harness (no future labels; past-survey-only B1 ranking).
Usage: prospective.py --section on|pk1 --survey YEAR [--check]
--check: regression vs shipped retrospective pages (identical top-20 cells+scores required).
Outputs: ranked watchlist JSON summary (committable aggregates) + full CSV to outputs/ (ignored).
Per-section recalibration lives in configs/thresholds.yaml (placeholder until next survey).
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize

SECTIONS = {
    "on": {"dir": "Омск-Новосибирск (392-526)", "kmax": 1330,
           "files": ("Аномалии.xlsx", "Аномалии_.xlsx"),
           "retro_json": "triage_demo.json", "retro_top": "top20"},
    "pk1": {"dir": "Парабель-Кузбасс-1 (572-714)", "kmax": 1400,
            "files": None, "retro_json": "triage_pk1.json", "retro_top": "top20"},
}
DATA = REPO.parent / "Данные для предварительного изучения"


def load_section(section, year):
    cfg = SECTIONS[section]
    d = DATA / cfg["dir"] / str(year)
    if cfg["files"]:
        fp = next((d / n for n in cfg["files"] if (d / n).exists()), None)
    else:
        cands = sorted(p for p in d.glob("*.xls*") if Path(p).name.startswith("Аномалии"))
        fp = Path(cands[0]) if cands else None
    assert fp, f"no anomaly file in {d}"
    df, meta = load_anomalies(fp)
    return normalize(df), meta


def rank(g, kmax):
    g = g[(g["depth"] >= 10) & g["corr"]].copy()
    ck = (g["dist"] // 100).astype(int).clip(0, kmax)
    cnt = g.groupby(ck).size().reindex(range(kmax + 1), fill_value=0).values.astype(float)
    score = cnt / max(cnt.max(), 1)
    order = np.argsort(-score, kind="stable")
    return cnt, score, order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", choices=("on", "pk1"), required=True)
    ap.add_argument("--survey", type=int, required=True)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--drop-last", action="store_true",
                    help="E13 edge guard: exclude boundary cell from ranking (overrun accumulation)")
    a = ap.parse_args()
    cfg = SECTIONS[a.section]
    g, meta = load_section(a.section, a.survey)
    cnt, score, order = rank(g, cfg["kmax"])
    edge_dropped = None
    if a.drop_last:
        edge_dropped = {"cell": cfg["kmax"], "past_count": int(cnt[cfg["kmax"]])}
        cnt = cnt.copy()
        cnt[cfg["kmax"]] = -1.0
        score = cnt / max(cnt[cnt >= 0].max(), 1)
        order = np.argsort(-score, kind="stable")
        order = order[order != cfg["kmax"]]
    top = [(r, int(i), int(cnt[i]), float(score[i])) for r, i in enumerate(order[:20], 1)]
    out = {"section": a.section, "survey": a.survey, "file": meta["name"],
           "model": "B1 past-count only (prospective, no future labels)",
           "recalibration": "placeholder — per-section thresholds uncalibrated until next survey",
           "edge_guard": edge_dropped,
           "top20": [{"rank": r, "cell": i, "past_count": p, "score": s} for r, i, p, s in top],
           "score_deciles": [float(np.percentile(score, q)) for q in (0, 25, 50, 75, 90, 99, 100)],
           "nonzero_cells": int((cnt > 0).sum()), "n_cells": cfg["kmax"] + 1}
    if a.check:
        retro = json.loads((Path(__file__).resolve().parent / cfg["retro_json"]).read_text())
        rt = retro[cfg["retro_top"]]
        # retro top20 rows are [rank, cell, past_count, score(, flag)]
        ok = all(r["cell"] == rr[1] and r["past_count"] == rr[2] and abs(r["score"] - rr[3]) < 1e-12
                 for r, rr in zip(out["top20"], rt))
        out["regression_vs_shipped"] = "IDENTICAL" if ok else "MISMATCH"
        print(f"regression_vs_shipped: {out['regression_vs_shipped']}")
        if not ok:
            raise SystemExit("REGRESSION MISMATCH — harness disagrees with shipped page")
    tag = f"watchlist_{a.section}_{a.survey}" + ("_noedge" if a.drop_last else "")
    (Path(__file__).resolve().parent / f"{tag}.json").write_text(json.dumps(out, indent=2))
    full = [{"cell": int(i), "km": round(float(i) / 10, 1), "past_count": int(cnt[i]), "score": float(score[i])}
            for i in order]
    outdir = REPO / "outputs"
    outdir.mkdir(exist_ok=True)
    (outdir / f"{tag}.csv").write_text(
        "cell,km,past_count,score\n" + "\n".join(f"{r['cell']},{r['km']},{r['past_count']},{r['score']:.4f}" for r in full))
    print(f"section={a.section} survey={a.survey} nonzero={out['nonzero_cells']}/{out['n_cells']} "
          f"top_cell={top[0][1]} top_score={top[0][3]:.3f}")

if __name__ == "__main__":
    main()
