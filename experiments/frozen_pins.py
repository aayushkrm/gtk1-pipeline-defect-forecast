"""Frozen-copy hash pins (additive check-only; writes nothing to results_e*.json).

The frozen experiment copies (e04b_robust.match_win, e07b_null.build) and src/gtk1
(match.match_win, features.build) share verified-identical OUTPUTS on all current data
(see src/tests/test_parity.py + `prospective.py --check` IDENTICAL), but their SOURCE
differs by audited guards only: Hungarian raise-vs-pass, width_m param, mr empty-guard,
scipy import position (round-15 review). Byte-identity was already broken upstream;
these pins now detect UNINTENDED drift. Any output-changing edit still needs a pipeline
version bump plus full recompute and reviewer approval. Read-only.
"""
import hashlib
import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))


def pin(fn):
    src = inspect.getsource(fn)
    norm = b"\n".join(line.rstrip().encode() for line in src.splitlines())
    return hashlib.sha256(norm).hexdigest()[:16]


def main():
    import e04b_robust as E04
    import e07b_null as E07
    from gtk1 import match as M, features as F

    pairs = [
        ("match_win", E04.match_win, M.match_win),
        ("build", E07.build, F.build),
    ]
    drift = 0
    for name, frozen, live in pairs:
        hf, hl = pin(frozen), pin(live)
        ok = hf == hl
        drift += not ok
        print(f"{name}: frozen={hf} src={hl} {'PIN PASS' if ok else 'DRIFT'}")
    print("FROZEN PINS " + ("OK" if drift == 0 else f"DRIFT x{drift}"))
    return drift


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
