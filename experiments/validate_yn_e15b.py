"""YN E15 phase 3: depth/placeholder/span/class-breakdown + pipe-number join check."""
import json
import csv
import collections
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "outputs"
BASE = REPO.parent / "Данные для предварительного изучения" / "Отчет ВТД_Ю-Н_0-154"


def num(x):
    try:
        return float(str(x).replace(",", "."))
    except (ValueError, TypeError):
        return None


def load(path):
    with open(path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        return r.fieldnames, list(r)


def share(vals, pred):
    ok = [v for v in vals if v is not None]
    return (sum(1 for v in ok if pred(v)) / len(ok) if ok else None), len(ok)


def main():
    out = {}
    # ---- 2020: depth missing by Character ----
    fn, rows = load(OUT / "yn2020_anom_salvaged.csv")
    print("2020 fields:", fn[:8], "...", fn[28:36])
    by_char = collections.defaultdict(list)
    for r in rows:
        by_char[r["Характер особенности"]].append(num(r["Глубина, %"]))
    print("2020 depth coverage by Character:")
    for k, v in sorted(by_char.items()):
        meas = [x for x in v if x is not None]
        ge10 = sum(1 for x in meas if x >= 10)
        print(f"  n={len(v):5d} measured={len(meas):5d} "
              f"ge10={ge10:5d} med={sorted(meas)[len(meas)//2] if meas else None}  {k!r}")
    out["2020_depth_by_char"] = {
        k: {"n": len(v), "measured": sum(1 for x in v if x is not None),
            "ge10": sum(1 for x in v if x is not None and x >= 10)} for k, v in by_char.items()}
    # non-numeric depth values
    nn = collections.Counter(r["Глубина, %"] for r in rows if num(r["Глубина, %"]) is None)
    print("2020 non-numeric Depth values:", nn.most_common(8))
    out["2020_depth_nonnumeric"] = {str(k): v for k, v in nn.most_common(8)}
    # clocks
    for c in ["Входящий ПШ, ч:мин", "Выходящий ПШ, ч:мин",
              "Ориентация центра, ч:мин", "Номер трубы", "Длина трубы, м",
              "Толщина, мм", "Длина, мм", "Ширина, мм", "КБД", "Опасность"]:
        vals = [r[c] for r in rows]
        nonemp = sum(1 for v in vals if v != "")
        print(f"  2020 {c}: filled={nonemp}/{len(vals)} sample={vals[3]}")
    # 2020 pipe-no vs weld log at same distance
    import openpyxl
    wb = openpyxl.load_workbook(str(BASE / "2020" / "Поперечные сварные швы.xlsx"),
                                read_only=True, data_only=True)
    ws = wb["Поперечные сварные швы"]
    it = iter(ws.iter_rows(values_only=True))
    hdr = next(it)
    print("weld hdr:", [str(v)[:24] if v is not None else None for v in hdr][:8])
    wrows = list(it)
    print("weld nrows:", len(wrows))
    print("weld row2:", [str(v)[:24] if v is not None else None for v in wrows[1]])
    # weld col layout: find pipe-no + distance cols
    for i, r in enumerate(wrows[1:6]):
        print("  weld", i, [str(v)[:20] if v is not None else None for v in r][:8])

    # ---- 2023 feat ----
    fn3, f3 = load(OUT / "yn2023_feat_salvaged.csv")
    print("feat fields:", fn3)
    for c in ["d,\n%", "d,\nмм", "Длина,\nмм", "Ширина,\nмм", "КБД", "Оценка",
              "Характер\nособенности", "Класс\nразмера", "Ориент.,\nч:мин",
              "N_x000D_\nп/п", "h,\nмм", "Ранг" if "Ранг" in fn3 else "Тип\nпол."]:
        if c not in fn3:
            continue
        vals = [r[c] for r in f3]
        nums = [num(v) for v in vals]
        ok = [v for v in nums if v is not None]
        if ok and len(ok) > len(vals) / 3:
            ge10 = sum(1 for v in ok if v >= 10)
            print(f"  feat {c!r}: numeric={len(ok)}/{len(vals)} "
                  f"min={min(ok)} max={max(ok)} ge10={ge10} "
                  f"({ge10/len(ok):.3f} of measured)")
            out[f"feat_{c}"] = {"numeric": len(ok), "n": len(vals),
                                "min": min(ok), "max": max(ok), "ge10": ge10}
        else:
            cnt = collections.Counter(vals)
            print(f"  feat {c!r}: distinct={len(cnt)} "
                  f"top={[(k[:24], v) for k, v in cnt.most_common(6)]}")
    ph = sum(1 for r in f3 if r["N\nтрубы"] == "60462" or r["Дистанция по\nодометру, м"] == "60462")
    print("feat placeholder-60462 rows:", ph)
    out["feat_placeholder60462"] = ph
    sane = [num(r["Дистанция по\nодометру, м"]) for r in f3]
    sane = [v for v in sane if v is not None and v < 160000 and v != 60462]
    print(f"feat sane-distance: n={len(sane)} span={min(sane)}..{max(sane)}")
    out["feat_sane_span"] = [min(sane), max(sane), len(sane)]
    sp = [r["N\nтрубы"] for r in f3 if num(r["N\nтрубы"]) is not None
          and num(r["N\nтрубы"]) < 20000]
    print(f"feat sane-pipe: n={len(sp)} min={min(float(x) for x in sp)} "
          f"max={max(float(x) for x in sp)}")

    # ---- 2023 anom ----
    fn4, f4 = load(OUT / "yn2023_anom_salvaged.csv")
    print("anom fields:", fn4)
    for c in ["d,\n%", "d,\nмм", "Длина,\nмм", "Ширина,\nмм", "КБД", "Оценка",
              "Характер\nособенности", "Класс\nразмера", "Ориент.,\nч:мин",
              "Ранг", "Срок, г.", "Тип\nпол.", "h,\nмм"]:
        if c not in fn4:
            continue
        vals = [r[c] for r in f4]
        nums = [num(v) for v in vals]
        ok = [v for v in nums if v is not None]
        if ok and len(ok) > len(vals) / 3:
            ge10 = sum(1 for v in ok if v >= 10)
            print(f"  anom {c!r}: numeric={len(ok)}/{len(vals)} "
                  f"min={min(ok)} max={max(ok)} ge10={ge10} "
                  f"({ge10/len(ok):.3f} of measured)")
            out[f"anom_{c}"] = {"numeric": len(ok), "n": len(vals),
                                "min": min(ok), "max": max(ok), "ge10": ge10}
        else:
            cnt = collections.Counter(vals)
            print(f"  anom {c!r}: distinct={len(cnt)} "
                  f"top={[(k[:24], v) for k, v in cnt.most_common(8)]}")
    (OUT / "yn_e15_phase3.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print("wrote yn_e15_phase3.json")


if __name__ == "__main__":
    main()
