"""YN E15 validation: salvage-parse truncated YN anomaly/feature sheets.

Read-only on sources. Method:
 1. Raw-extract each sheet stream (ignore ZIP CRC) + tolerant zlib inflate.
 2. Cache inflated XML under outputs/ (gitignored; avoids re-inflate).
 3. Linear salvage: split on </row>, take text after last <row r="N".
    A chunk is CLEAN if it holds exactly one <row> open; else GARBLE
    (duplication-garble: repeated <row> opens with no closes).
 4. Resolve t="s" cells via intact sharedStrings.xml (stock zip read).
 5. Header detect + column map + validation. CSVs to outputs/.
"""
import struct
import sys
import zlib
import zipfile
import re
import json
import csv
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BASE = REPO.parent / "Данные для предварительного изучения" / "Отчет ВТД_Ю-Н_0-154"
OUT = REPO / "outputs"
OUT.mkdir(exist_ok=True)

F20 = BASE / "2020" / "Аномалии.xlsx"
F23 = BASE / "2023" / "otchet_скорр.xlsx"

CELL_RE = re.compile(r'<c r="([A-Z]+)\d+"[^>]*>(.*?)</c>', re.S)
V_RE = re.compile(r"<v>(.*?)</v>", re.S)
ROW_OPEN_RE = re.compile(r'<row r="(\d+)"')


def col_idx(letters):
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def inflate(xlsx_path, part, cache_name):
    cache = OUT / cache_name
    if cache.exists():
        return cache.read_text(encoding="utf-8", errors="replace")
    raw = Path(xlsx_path).read_bytes()
    pos = 0
    while True:
        i = raw.find(b"\x50\x4b\x03\x04", pos)
        if i < 0:
            raise KeyError(f"{part} not found")
        comp, uncomp, fnlen, eflen = struct.unpack("<IIHH", raw[i + 18:i + 30])
        fn = raw[i + 30:i + 30 + fnlen].decode("utf-8", "replace")
        if fn == part:
            start = i + 30 + fnlen + eflen
            data = raw[start:start + comp]
            d = zlib.decompressobj(-15)
            out = d.decompress(data)
            info = {"eof": d.eof, "got": len(out), "want": uncomp,
                    "comp": comp, "unused": len(d.unused_data)}
            (OUT / (cache_name + ".info.json")).write_text(json.dumps(info))
            txt = out.decode("utf-8", "replace")
            cache.write_text(txt, encoding="utf-8")
            return txt
        pos = i + 30 + fnlen


def load_strings(xlsx_path):
    import io
    import xml.etree.ElementTree as ET
    z = zipfile.ZipFile(str(xlsx_path))
    raw = z.read("xl/sharedStrings.xml")
    ss = []
    for _, el in ET.iterparse(io.BytesIO(raw), events=("end",)):
        if el.tag.endswith("}si"):
            ss.append("".join(el.itertext()))
            el.clear()
    return ss


def salvage_rows(xml_text):
    """Return (clean_rows, garble_chunks). clean_rows: list of (rnum, body)."""
    chunks = xml_text.split("</row>")
    clean, garble = [], []
    for ch in chunks:
        opens = ROW_OPEN_RE.findall(ch)
        if not opens:
            continue
        if len(opens) == 1:
            m = list(ROW_OPEN_RE.finditer(ch))[-1]
            clean.append((int(m.group(1)), ch[m.start():]))
        else:
            garble.append((opens[0], opens[-1], len(opens)))
    return clean, garble


def parse_cells(body, ss):
    out = {}
    for m in CELL_RE.finditer(body):
        col = m.group(1)
        b = m.group(2)
        vm = V_RE.search(b)
        v = vm.group(1).strip() if vm else ""
        head = m.group(0)[:80]
        if 't="s"' in head and v != "":
            try:
                v = ss[int(float(v))]
            except (ValueError, IndexError):
                v = f"SI?{v}"
        out[col_idx(col)] = v
    return out


def salvage_sheet(xlsx_path, part, cache_name):
    ss = load_strings(xlsx_path)
    txt = inflate(xlsx_path, part, cache_name)
    clean, garble = salvage_rows(txt)
    rows = [(r, parse_cells(b, ss)) for r, b in clean]
    rows.sort(key=lambda x: x[0])
    return {"strings": len(ss), "clean": rows, "garble": garble,
            "xml_len": len(txt)}


def show(name, res, n=3):
    print(f"=== {name}: strings={res['strings']} clean={len(res['clean'])} "
          f"garble_chunks={len(res['garble'])} garble_opens="
          f"{sum(g[2] for g in res['garble'])}")
    for r, cells in res["clean"][:n]:
        items = sorted(cells.items())[:10]
        print(f"  row {r} ncols={len(cells)}",
              [(c, v[:24]) for c, v in items])


def main(which="all"):
    if which in ("all", "20"):
        r20 = salvage_sheet(F20, "xl/worksheets/sheet3.xml", "_yn20_sheet3.xml")
        show("YN2020 sheet3 Anomaly", r20, 5)
        json.dump({"clean_n": len(r20["clean"]),
                   "garble": r20["garble"][:20],
                   "first_rows": [r for r, _ in r20["clean"][:5]],
                   "last_rows": [r for r, _ in r20["clean"][-5:]]},
                  open(OUT / "_yn20_meta.json", "w"), ensure_ascii=False)
    if which in ("all", "23"):
        for part, tag in [("xl/worksheets/sheet3.xml", "feat"),
                          ("xl/worksheets/sheet4.xml", "anom"),
                          ("xl/worksheets/sheet5.xml", "pipe")]:
            r = salvage_sheet(F23, part, f"_yn23_{tag}.xml")
            show(f"YN2023 {tag} {part}", r, 2)
            json.dump({"clean_n": len(r["clean"]),
                       "garble_n": len(r["garble"]),
                       "garble_opens": sum(g[2] for g in r["garble"]),
                       "first_rows": [x for x, _ in r["clean"][:5]],
                       "last_rows": [x for x, _ in r["clean"][-5:]]},
                      open(OUT / f"_yn23_{tag}_meta.json", "w"), ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
