"""Salvage PK1-2025 weld log (short FAT chain: last ~65KB missing, rows intact).
Patches xlrd compdoc to accept truncated streams + tolerant cells. Reads SOURCE read-only.
Saves recovered CSV to outputs/ (ignored, persists unlike /tmp). Prints validation stats.
"""
import sys
from pathlib import Path
import pandas as pd
REPO = Path(__file__).resolve().parents[1]
SRC = (REPO.parent / "Данные для предварительного изучения"
       / "Парабель-Кузбасс-1 (572-714)" / "2025" / "Поперечные сварные швы.xls")
OUT = REPO / "outputs" / "pk1_2025_weld_salvaged.csv"


def _patch():
    import xlrd.compdoc as C
    EOCSID = -2

    def tolerant_locate(self, mem, base, sat, sec_size, start_sid,
                        expected_stream_size, qname, seen_id):
        from xlrd.compdoc import CompDocError
        s = start_sid
        if s < 0:
            raise CompDocError("start_sid -ve")
        p, slices, tot_found = -99, [], 0
        found_limit = (expected_stream_size + sec_size - 1) // sec_size
        start_pos, end_pos = -9999, -8888
        while s >= 0:
            self.seen[s] = seen_id
            tot_found += 1
            if tot_found > found_limit:
                raise CompDocError("size exceeds expected")
            if s == p + 1:
                end_pos += sec_size
            else:
                if p >= 0:
                    slices.append((start_pos, end_pos))
                start_pos = base + s * sec_size
                end_pos = start_pos + sec_size
            p = s
            s = sat[s] if s < len(sat) else EOCSID
        if not slices:
            return (mem, start_pos, tot_found * sec_size)
        slices.append((start_pos, end_pos))
        return (b"".join(mem[a:b] for a, b in slices), 0, tot_found * sec_size)

    C.CompDoc._locate_stream = tolerant_locate
    from xlrd.sheet import Sheet
    _orig = Sheet.put_cell_unragged

    def tol_unrag(self, rowx, colx, ctype, value, xf_index):
        try:
            if colx + 1 > self.utter_max_cols:
                self.utter_max_cols = colx + 1
            if rowx + 1 > self.utter_max_rows:
                self.utter_max_rows = rowx + 1
            return _orig(self, rowx, colx, ctype, value, xf_index)
        except (AssertionError, IndexError, KeyError):
            return None

    Sheet.put_cell_unragged = tol_unrag


def main():
    _patch()
    import xlrd
    bk = xlrd.open_workbook(str(SRC), logfile=open("/dev/null", "w"),
                            ignore_workbook_corruption=True, formatting_info=False)
    sh = bk.sheet_by_name("Поперечные сварные швы")
    print(f"sheet: {sh.nrows}x{sh.ncols}")
    df = pd.read_excel(str(SRC), sheet_name="Поперечные сварные швы", header=3, engine="xlrd")
    print(f"pandas: {len(df)}x{len(df.columns)}")
    dist = pd.to_numeric(df.iloc[:, 1], errors="coerce")
    print(f"dist notna={int(dist.notna().sum())} max={float(dist.max()):.1f} "
          f"pipes={int(df.iloc[:, 0].astype(str).nunique())}")
    df.to_csv(OUT, index=False)
    print(f"saved {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
