"""Character (defect-type) distributions per survey — re-derived for README tables.
Strict files via gtk1.io loader; 2015 via header=0; YN via salvaged CSVs in outputs/.
Writes results_char.json {section: {year: {top5, n}}} + full value_counts. Read-only.
"""
import json
import sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
from gtk1.io import load_anomalies

BASE = REPO.parent / "Данные для предварительного изучения"
OUT = REPO / "experiments"


def charcol(df):
    c = [x for x in df.columns if "арактер" in str(x).lower() and "аббр" not in str(x).lower()]
    return c[0] if c else None


def dist_xlsx(fp, sheet, header):
    df, _ = load_anomalies(fp, sheet=sheet, header=header)
    c = charcol(df)
    vc = df[c].astype(str).value_counts()
    return {"n": int(len(df)), "top": {k: int(v) for k, v in vc.head(6).items()}}


def dist_csv(fp):
    df = pd.read_csv(fp)
    c = charcol(df)
    vc = df[c].astype(str).value_counts()
    return {"n": int(len(df)), "top": {k: int(v) for k, v in vc.head(6).items()}}


def run():
    S = BASE
    out = {}
    jobs = [
        ("ON", 2016, lambda: dist_xlsx(S / "Омск-Новосибирск (392-526)" / "2016" / "Аномалии.xlsx", "Аномалии", 3)),
        ("ON", 2021, lambda: dist_xlsx(S / "Омск-Новосибирск (392-526)" / "2021" / "Аномалии.xlsx", "Аномалии", 3)),
        ("ON", 2025, lambda: dist_xlsx(S / "Омск-Новосибирск (392-526)" / "2025" / "Аномалии_.xlsx", "Аномалии", 3)),
        ("PK1", 2022, lambda: dist_xlsx(S / "Парабель-Кузбасс-1 (572-714)" / "2022" / "Аномалии.xls", "Аномалии", 3)),
        ("PK1", 2025, lambda: dist_xlsx(S / "Парабель-Кузбасс-1 (572-714)" / "2025" / "Аномалии.xls", "Аномалии", 3)),
        ("PK2", 2015, lambda: dist_xlsx(S / "Парабель-Кузбасс-2 (0-110)" / "2015" / "Таблица дефектов 2015.xlsx", "Таблица дефектов", 0)),
        ("PK2", 2020, lambda: dist_xlsx(S / "Парабель-Кузбасс-2 (0-110)" / "2020" / "Аномалии.xlsx", "Аномалии", 3)),
        ("SRTO1608", 2016, lambda: dist_xlsx(S / "СРТО-Омск_(1608 – 1717)" / "2016" / "Аномалии.xls", "Аномалии", 3)),
        ("SRTO1608", 2021, lambda: dist_xlsx(S / "СРТО-Омск_(1608 – 1717)" / "2021" / "Аномалии.xls", "Аномалии", 3)),
        ("SRTO1608", 2024, lambda: dist_xlsx(S / "СРТО-Омск_(1608 – 1717)" / "2024" / "Аномалии1.xls", "Аномалии", 3)),
        ("SRTO1717", 2021, lambda: dist_xlsx(S / "СРТО-Омск_(1717-1759)" / "2021" / "Аномалии.xls", "Аномалии", 3)),
        ("YN", 2020, lambda: dist_csv(REPO / "outputs" / "yn2020_anom_salvaged.csv")),
        ("YN", 2023, lambda: dist_csv(REPO / "outputs" / "yn2023_anom_salvaged.csv")),
    ]
    for sec, yr, fn in jobs:
        try:
            out.setdefault(sec, {})[str(yr)] = fn()
        except Exception as e:
            out.setdefault(sec, {})[str(yr)] = {"error": f"{type(e).__name__}: {str(e)[:100]}"}
        print(f"done {sec} {yr}", flush=True)
    (OUT / "results_char.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("wrote results_char.json")


if __name__ == "__main__":
    run()
