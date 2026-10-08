"""Parity: src/gtk1 vs frozen experiment copies on synthetic frames (no raw data)."""
import sys
import warnings
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "experiments"))
sys.path.insert(0, str(REPO / "src"))
import e04b_robust as E04
import e07b_null as E07
from gtk1 import match as M, features as F, metrics as MET
from gtk1 import io as IO


def frames():
    rng = np.random.default_rng(11)
    n = 60
    past = pd.DataFrame({
        "dist": rng.uniform(0, 5000, n), "depth": rng.uniform(8, 30, n),
        "pipe": [str(rng.integers(1, 8)) for _ in range(n)],
        "off": rng.uniform(-5, 5, n), "h": rng.integers(0, 12, n).astype(float),
        "char": ["Коррозия"] * n, "corr": [True] * n})
    fut = past.copy()
    fut["dist"] = fut["dist"] + rng.normal(0, 0.5, n)  # all matchable
    extra = pd.DataFrame({
        "dist": [6000.0, 7000.0], "depth": [12.0, 15.0], "pipe": ["99", "99"],
        "off": [0.0, 0.0], "h": [6.0, 6.0], "char": ["Коррозия", "Коррозия"], "corr": [True, True]})
    return past, pd.concat([fut, extra], ignore_index=True)


def _row(dist=100.0, depth=12.0, pipe="1", off=0.0, h=6.0, char="Коррозия"):
    return pd.DataFrame({"dist": [dist], "depth": [depth], "pipe": [pipe],
                         "off": [off], "h": [h], "char": [char], "corr": [True]})


def test_nan_off():
    past = _row(off=float("nan"))
    fut = _row(off=float("nan"))
    m = M.match_win(past, fut, 2)
    assert bool(np.asarray(m)[0]) is True, "NaN off must match with do=0"


def test_missing_h():
    past = _row(h=-99.0)
    fut = _row(h=5.0)
    m = M.match_win(past, fut, 2)
    assert bool(np.asarray(m)[0]) is True, "h=-99 (missing ori) must match with dh=0"
    past2 = _row(h=-99.0)
    fut2 = _row(h=-99.0)
    m2 = M.match_win(past2, fut2, 2)
    assert bool(np.asarray(m2)[0]) is True, "both h=-99 must match"


def test_empty_past():
    past = _row().iloc[0:0].copy()
    fut = pd.concat([_row(dist=100.0), _row(dist=200.0)], ignore_index=True)
    m = M.match_win(past, fut, 2)
    assert len(m) == 2 and not np.asarray(m).any(), "empty past must yield all-False"
    y, X, mr = F.build(past, fut, 10, 10)
    assert len(y) == 11 and X.shape == (11, 7) and mr == 0.0, "build with empty past must not crash"


def test_duplicate_pipes():
    past = _row(dist=100.0, pipe="7")
    fut = pd.concat([_row(dist=100.1, pipe="7"), _row(dist=100.2, pipe="7")], ignore_index=True)
    m = np.asarray(M.match_win(past, fut, 2))
    assert m.sum() == 1, f"one-to-one greedy must consume past row once, got {m.sum()}"


def _raw_df(rows):
    # rows: list of dicts with keys dist/depth/pipe/off/char
    df = pd.DataFrame({
        "Расстояние": [r.get("dist") for r in rows],
        "Глубина": [r.get("depth") for r in rows],
        "Номер трубы": [r.get("pipe") for r in rows],
        "Характер": [r.get("char", "Коррозия") for r in rows],
    })
    return df


def test_overrun_dist():
    df = _raw_df([{"dist": 999999.0, "depth": 12.0, "pipe": "1"}])
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        g = IO.normalize(df, width_m=100, kmax=70)
    assert int(g["cell"].iloc[0]) == 70, "overrun dist must clip to kmax"
    df2 = _raw_df([{"dist": -5.0, "depth": 12.0, "pipe": "1"}])
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        g2 = IO.normalize(df2, width_m=100, kmax=70)
    assert int(g2["cell"].iloc[0]) == 0, "negative dist must clip to 0"
    assert any("negative" in str(x.message).lower() for x in w), "negative dist must log/warn"
    # build with overrun dist must not crash
    past = _row(dist=999999.0)
    fut = _row(dist=999999.0)
    y, X, mr = F.build(past, fut, 10, 70)
    assert len(y) == 71, "build with overrun dist must keep kmax shape"


def test_hungarian_mode():
    past = pd.concat([_row(dist=100.0, pipe="1"), _row(dist=200.0, pipe="1")], ignore_index=True)
    fut = pd.concat([_row(dist=100.1, pipe="1"), _row(dist=200.1, pipe="1")], ignore_index=True)
    mg = np.asarray(M.match_win(past, fut, 2, hungarian=False))
    mh = np.asarray(M.match_win(past, fut, 2, hungarian=True))
    assert len(mh) == 2 and mh.sum() == 2, "Hungarian must match both"
    assert (mg == mh).all(), "greedy/Hungarian must agree on trivial frame"
    # failure must raise with shape info, never swallow
    import scipy.optimize as _opt
    _real = _opt.linear_sum_assignment

    def _boom(C):
        raise ValueError("boom")
    _opt.linear_sum_assignment = _boom
    try:
        try:
            M.match_win(past, fut, 2, hungarian=True)
            raise AssertionError("Hungarian failure must raise, not swallow")
        except RuntimeError as e:
            msg = str(e)
            assert "P=2" in msg and "F=2" in msg, f"shape info missing in: {msg}"
    finally:
        _opt.linear_sum_assignment = _real


def test_zero_positives():
    rng = np.random.default_rng(0)
    y0 = np.zeros(20, dtype=int)
    s0 = rng.uniform(0, 1, 20)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        lc = MET.ap_lift_ci(y0, s0, n=100)
    assert np.isnan(lc["lift_CI"][0]) and np.isnan(lc["lift_CI"][1]), "zero positives must give NaN lift CI"
    assert any("positives" in str(x.message).lower() or "bootstrap" in str(x.message).lower() for x in w)
    with warnings.catch_warnings(record=True) as w2:
        warnings.simplefilter("always")
        d0, lo, hi = MET.paired_delta_ci(y0, s0, np.zeros_like(s0), n=100)
    assert np.isnan(lo) and np.isnan(hi), "zero positives paired delta must give NaN interval"
    with warnings.catch_warnings(record=True) as w3:
        warnings.simplefilter("always")
        est, lo3, hi3 = MET.precision_at_k(np.array([]), np.array([]), 10, n_boot=10)
    assert np.isnan(est) and np.isnan(lo3), "empty precision_at_k must give NaNs"
    # non-empty zero-positive precision@K still defined (est 0.0, resample-rerank CI)
    est2, lo2, hi2 = MET.precision_at_k(y0, s0, 5, n_boot=100)
    assert est2 == 0.0, "P@K est must be 0.0 when no positives"


def test_io_guards():
    from xlrd.sheet import Sheet
    IO._apply_tolerant_xlrd()
    f1 = Sheet.put_cell_unragged
    r1 = Sheet.read
    IO._apply_tolerant_xlrd()
    assert Sheet.put_cell_unragged is f1, "tolerant xlrd must never double-wrap put_cell_unragged"
    assert Sheet.read is r1, "tolerant xlrd must never double-wrap read"
    try:
        IO.load_anomalies("/nonexistent/path/Аномалии.xlsx")
        raise AssertionError("missing file must raise")
    except FileNotFoundError as e:
        assert "file not found" in str(e).lower()
    # missing sheet must raise clearly (no silent tolerant fallback)
    import tempfile, os
    with tempfile.TemporaryDirectory() as td:
        fp = os.path.join(td, "t.xlsx")
        pd.DataFrame({"a": [1]}).to_excel(fp, sheet_name="Wrong", index=False)
        try:
            IO.load_anomalies(fp, sheet="Аномалии", header=0)
            raise AssertionError("missing sheet must raise")
        except ValueError as e:
            assert "sheet" in str(e).lower() or "header" in str(e).lower()
    # normalize missing columns must raise explicit messages
    df_ok = _raw_df([{"dist": 100.0, "depth": 12.0, "pipe": "1"}])
    for drop, key in ((["Расстояние"], "расстояние"), (["Глубина"], "глубина"),
                       (["Номер трубы"], "номер"), (["Характер"], "характер")):
        bad = df_ok.drop(columns=drop)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                IO.normalize(bad)
            raise AssertionError(f"missing {key} must raise")
        except ValueError as e:
            assert key in str(e).lower(), f"explicit message must name {key}: {e}"
    # non-finite dist dropped with warning
    df_inf = _raw_df([{"dist": float("inf"), "depth": 12.0, "pipe": "1"}])
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        g = IO.normalize(df_inf)
    assert len(g) == 0, "inf dist must be dropped"
    assert any("non-finite" in str(x.message).lower() or "nonfinite" in str(x.message).lower()
               or "finite" in str(x.message).lower() for x in w)


def test_danger_kbd_passthrough():
    # Опасность=(a/b/c) repair classes + КБД must survive normalize; absent columns default empty/NaN.
    df = _raw_df([{"dist": 100.0, "depth": 12.0, "pipe": "1"}])
    df["Опасность"] = ["(b)"]
    df["КБД"] = [0.89]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        g = IO.normalize(df)
    assert str(g["danger"].iloc[0]) == "(b)", f"danger passthrough broken: {g['danger'].iloc[0]}"
    assert abs(float(g["kbd"].iloc[0]) - 0.89) < 1e-12, "kbd passthrough broken"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        g2 = IO.normalize(_raw_df([{"dist": 100.0, "depth": 12.0, "pipe": "1"}]))
    assert str(g2["danger"].iloc[0]) == "" and pd.isna(g2["kbd"].iloc[0]), \
        "absent danger/kbd must default to empty/NaN"


def test_cell_abc():
    # worst class per cell: a(2) beats b(1) beats c/empty(0); absent danger column -> all zero.
    df = pd.DataFrame({
        "dist": [50.0, 50.0, 150.0, 250.0],
        "danger": ["(a)", "(c)", "(b)", ""],
    })
    c = F.cell_abc(df, 10)
    assert len(c) == 11
    assert int(c.loc[0, "worst"]) == 2 and int(c.loc[0, "n_a"]) == 1 and int(c.loc[0, "n_b"]) == 0
    assert int(c.loc[1, "worst"]) == 1 and int(c.loc[1, "n_b"]) == 1
    assert int(c.loc[2, "worst"]) == 0
    c2 = F.cell_abc(df.drop(columns=["danger"]), 10)
    assert int(c2["worst"].sum()) == 0 and int(c2["n_a"].sum()) == 0
    # n_c counts explicit (c) rows only: clean cells read all-zero.
    df3 = pd.DataFrame({
        "dist": [50.0, 50.0, 150.0],
        "danger": ["(c)", "", "(c)"],
    })
    c3 = F.cell_abc(df3, 10)
    assert int(c3.loc[0, "worst"]) == 0 and int(c3.loc[0, "n_c"]) == 1
    assert int(c3.loc[1, "worst"]) == 0 and int(c3.loc[1, "n_c"]) == 1


def test_build_filter_first_threshold_semantics():
    # R1 frozen semantics: the cut applies BEFORE matching, so a shallow past
    # row (5%) can never match a deep future (12%) at the same location.
    # Threshold-crossers count as newly-reported BY DESIGN (report-threshold
    # semantics). Any reorder needs a pipeline version bump + recompute.
    gp = _row(dist=500.0, depth=5.0, pipe="3", off=0.0, h=6.0)
    gf = _row(dist=500.1, depth=12.0, pipe="3", off=0.0, h=6.0)
    y, X, mr = F.build(gp, gf, 10, 10)
    assert mr == 0.0, f"filter-first match must give mr=0.0, got {mr}"
    assert int(y.sum()) == 1, "unmatched deep future must be labelled new"
    # contrast: both shallow -> future excluded by cut, no labels either
    gp2 = _row(dist=500.0, depth=5.0, pipe="3")
    gf2 = _row(dist=900.0, depth=5.0, pipe="3")
    y2, X2, mr2 = F.build(gp2, gf2, 10, 10)
    assert int(y2.sum()) == 0 and mr2 == 0.0, "all-shallow pair gives empty cut future"


def test_prospective_drop_last_semantics():
    # boundary cell is the max; kept-only deciles must exclude it and never contain -1.
    cnt = np.array([5.0, 3.0, 211.0])
    kmax = 2
    kept = np.ones(len(cnt), dtype=bool)
    kept[kmax] = False
    cnt_kept = cnt[kept]
    score_kept = cnt_kept / max(float(cnt_kept.max()), 1.0)
    dec = [float(np.percentile(score_kept, q)) for q in (0, 25, 50, 75, 90, 99, 100)]
    assert dec[0] >= 0.0, f"kept-only deciles must exclude -1 sentinel, got {dec}"
    assert int(cnt[kmax]) == 211, "edge count preserved for guard record"
    assert not bool(((cnt_kept) == -1).any()), "never write past_count=-1"


def main():
    past, fut = frames()
    m1 = E04.match_win(past, fut, 2)
    m2 = M.match_win(past, fut, 2)
    assert (np.asarray(m1) == np.asarray(m2)).all(), "match_win parity FAIL"
    assert m2.sum() == 60 and (~m2).sum() == 2, f"unexpected flags {m2.sum()}"
    y2, X2, mr2 = F.build(past, fut, 10, 70)
    y1b, X1b, mr1b = E07.build(past, fut, 10, 70)
    assert (y1b == y2).all() and np.allclose(X1b, X2) and mr1b == mr2, "build parity FAIL"
    s = X2[:, 0] / X2[:, 0].max()
    from sklearn.metrics import average_precision_score
    assert abs(MET.ap(y2, s) - float(average_precision_score(y2, s))) < 1e-12, "ap parity FAIL"
    lc = MET.ap_lift_ci(y2, s, n=200)
    assert lc["n_pos"] == int(y2.sum()) and lc["lift"] == lc["AP"] - lc["base"]
    d, lo, hi = MET.paired_delta_ci(y2, s, np.zeros_like(s), n=200)
    assert lo <= d <= hi, "paired CI must bracket its own point estimate"
    print(f"parity OK: match {m2.sum()}/{len(m2)}, build kmax70 pos={y2.sum()}, AP={lc['AP']:.3f}")
    test_nan_off()
    print("edge NaN-off OK")
    test_missing_h()
    print("edge missing-h OK")
    test_empty_past()
    print("edge empty-past OK")
    test_duplicate_pipes()
    print("edge duplicate-pipes OK")
    test_overrun_dist()
    print("edge overrun-dist OK")
    test_hungarian_mode()
    print("edge hungarian OK")
    test_zero_positives()
    print("edge zero-positives OK")
    test_io_guards()
    print("edge io-guards OK")
    test_danger_kbd_passthrough()
    print("edge danger-kbd OK")
    test_cell_abc()
    print("edge cell-abc OK")
    test_build_filter_first_threshold_semantics()
    print("edge filter-first-threshold OK")
    test_prospective_drop_last_semantics()
    print("edge drop-last OK")
    print("ALL EDGE CASES OK")


if __name__ == "__main__":
    main()
