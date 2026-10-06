"""Quad fan-out: all four providers CONCURRENTLY (threads), merged + URL-deduped.
This is the "all four in parallel" requirement in code. Missing-key providers SKIP gracefully.
"""
from concurrent.futures import ThreadPoolExecutor
from . import exa, firecrawl, parallel, tinyfish


def quad_search(query, per_provider=8, objective=None):
    objective = objective or query
    jobs = [
        lambda: exa.search(query, num_results=per_provider),
        lambda: firecrawl.search(query, limit=per_provider),
        lambda: parallel.search(objective, [query], mode="basic", max_results=per_provider),
        lambda: tinyfish.search(query),
    ]
    with ThreadPoolExecutor(max_workers=4) as pool:
        parts = list(pool.map(lambda f: f(), jobs))
    seen, merged = set(), []
    for p in parts:
        for r in p["results"]:
            u = (r.get("url") or "").rstrip("/").lower()
            if u and u not in seen:
                seen.add(u)
                merged.append({**r, "via": p["provider"]})
    return {"query": query,
            "status": {p["provider"]: p["status"] for p in parts},
            "results": merged}
