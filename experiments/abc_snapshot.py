"""abc_snapshot: per-cell worst repair class for the latest survey per section.

Product purpose (Vlad, meeting 08.10.2026): red/orange/yellow/white heatmap colors
come from PRESENT labels (E16 closed per-class forecasting by evidence). This script
renders no map; it emits the data the prototype track (Satonin) consumes.
Method: normalize latest-survey anomaly table (ALL depths, ALL characters: critical
(a) flags concentrate on weld/geometry rows outside the corr-only triage population,
verified ON-2025 6/8 and PK1-2025 40/45 on ring-weld anomalies), cell_abc() worst-class
per 100m cell.
Writes triage/abc_<section>_<year>.json: per-cell worst array + counts + provenance.
Read-only raw data. No model, no thresholds, no claims. B1 triage pages stay corr-only
(R1 frozen); this snapshot is the separate all-character display layer.
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies, normalize
from gtk1.features import cell_abc

DATA_ROOT = REPO.parent / "Данные для предварительного изучения"
TARGETS = {
    ("on", 2025): ("Омск-Новосибирск (392-526)", "2025", ("Аномалии.xlsx", "Аномалии_.xlsx"), 1330),
    ("pk1", 2025): ("Парабель-Кузбасс-1 (572-714)", "2025", ("Аномалии.xls",), 1400),
    ("srto", 2024): ("СРТО-Омск_(1608 – 1717)", "2024", ("Аномалии.xls", "Аномалии1.xls"), 1040),
    ("srto1717", 2021): ("СРТО-Омск_(1717-1759)", "2021", ("Аномалии.xls",), 420),
}


def main():
    for (tag, year), (sdir, ydir, cands, kmax) in TARGETS.items():
        d = DATA_ROOT / sdir / str(ydir)
        fp = next((d / n for n in cands if (d / n).exists()), None)
        assert fp, f"no anomaly file in {d}"
        df, meta = load_anomalies(str(fp))
        g = normalize(df)
        cells = cell_abc(g, kmax)
        worst = cells["worst"].to_numpy()
        out = {
            "section": tag, "survey": year, "file": meta["name"],
            "meaning": "worst present repair class per 100m cell: 2=A(repair), 1=B(monitor), "
                         "0=C/none; n_c counts explicit (c) rows so yellow (C) separates from "
                         "white (clean: n_a=n_b=n_c=0)",
            "cells_with_a": int((worst == 2).sum()),
            "cells_with_b": int((worst == 1).sum()),
            "cells_with_c_only": int(((worst == 0) & (cells["n_c"].to_numpy() > 0)).sum()),
            "n_a_rows": int(cells["n_a"].sum()),
            "n_b_rows": int(cells["n_b"].sum()),
            "n_c_rows": int(cells["n_c"].sum()),
            "worst": worst.tolist(),
        }
        try:
            out["repro"] = {"git": subprocess.check_output(
                ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"]).decode().strip()}
        except Exception:
            out["repro"] = {"git": "unknown"}
        (REPO / "triage" / f"abc_{tag}_{year}.json").write_text(
            json.dumps(out, ensure_ascii=False))
        print(f"{tag} {year}: cells_a={out['cells_with_a']} cells_b={out['cells_with_b']} "
              f"rows_a={out['n_a_rows']} rows_b={out['n_b_rows']}")


if __name__ == "__main__":
    main()
