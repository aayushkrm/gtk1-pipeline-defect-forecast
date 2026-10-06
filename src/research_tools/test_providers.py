"""Provider self-test: OK / SKIP (no key) / FAIL per provider + one quad fan-out.
Exit 0 unless a KEYED provider FAILs. Missing keys are expected-shortfall, reported not hidden.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_tools import exa, firecrawl, parallel, tinyfish, quad

Q = "ILI in-line inspection pipeline corrosion growth forecasting"
O = "Find research on forecasting corrosion growth from repeat in-line inspection surveys."


def main():
    reps = [
        exa.search(Q, num_results=3),
        firecrawl.search(Q, limit=3),
        parallel.search(O, [Q], mode="turbo", max_results=3),
        tinyfish.search(Q),
    ]
    bad = 0
    for r in reps:
        n = len(r["results"])
        print(f"- {r['provider']:10s} {r['status']:5s} n={n} {r.get('reason', '')}"
              f"{(' e.g. ' + r['results'][0]['url'][:80]) if n else ''}")
        import os
        keyed = bool(os.environ.get({"exa": "EXA_API_KEY", "firecrawl": "FIRECRAWL_API_KEY",
                                     "parallel": "PARALLEL_API_KEY",
                                     "tinyfish": "TINYFISH_API_KEY"}[r["provider"]], ""))
        if keyed and r["status"] != "OK":
            bad += 1
    q = quad.quad_search(Q, per_provider=3, objective=O)
    print(f"quad: {q['status']} merged_unique_urls={len(q['results'])}")
    print("SELFTEST " + ("FAIL" if bad else "PASS"))
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
