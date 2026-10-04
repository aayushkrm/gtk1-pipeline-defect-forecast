"""Frozen-number consistency: tripwire against accidental output edits (no raw data needed).
Asserts committed result/triage JSONs still carry the exact validated numbers.
Any intentional number change must update this file in the same commit with reviewer sign-off.
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXP = REPO / "experiments"
TRI = REPO / "triage"


def load(p):
    return json.loads((REPO / p).read_text())


def test_on_frozen():
    d = load("experiments/results_e04.json")
    assert d["cuts"]["10"]["B1"]["AP"] == load("triage/triage_demo.json")["AP"]
    t = load("triage/triage_demo.json")
    assert abs(t["AP"] - 0.6435734381993825) < 1e-12
    assert abs(t["base"] - 0.2682193839218633) < 1e-12
    assert abs(t["match_rate"] - 0.6115702479338843) < 1e-12


def test_pk1_frozen():
    t = load("triage/triage_pk1.json")
    assert abs(t["AP"] - 0.7794665808239355) < 1e-12
    assert abs(t["base"] - 0.4011420413990007) < 1e-12
    assert t["cut_sensitivity"] == {"10": 0.779, "12": 0.574, "15": 0.375}


def test_srto_frozen():
    t = load("triage/triage_srto.json")
    assert abs(t["AP"] - 0.2767) < 1e-4
    assert abs(t["base"] - 0.0605) < 1e-4
    assert abs(t["match_rate"] - 0.5511) < 1e-4


def test_src_only_imports():
    import re
    for p in ("triage/build_report.py", "triage/build_pk1.py", "triage/build_srto.py",
              "triage/prospective.py"):
        src = (REPO / p).read_text()
        assert "experiments/" not in src, p
        assert re.search(r"from gtk1\.|from \.gtk1|import gtk1", src), p


def _walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("lift_CI95", "liftCI") and isinstance(v, (list, tuple)) and len(v) == 2:
                yield v
            else:
                yield from _walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v)


def test_lift_cis_lower_above_zero():
    found = 0
    for f in ("results_e05b.json", "results_e10.json", "results_e11.json", "results_e12.json"):
        d = load(f"experiments/{f}")
        for ci in _walk(d):
            assert ci[0] > 0, (f, ci)
            found += 1
    assert found >= 5, f"expected >=5 lift CIs, found {found}"


def test_guardrails_present_on_pages():
    for p in ("triage/triage_demo.html", "triage/triage_pk1.html", "triage/triage_srto.html"):
        h = (REPO / p).read_text()
        for s in ("NOT a physical prediction", "Per-section thresholds", "do not pool"):
            assert s in h, (p, s)
