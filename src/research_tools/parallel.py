"""Parallel search (objective + keyword probes, LLM excerpts). Docs: https://docs.parallel.ai.
POST https://api.parallel.ai/v1/search, x-api-key header. Auth: $PARALLEL_API_KEY."""
import json
import os
import urllib.request

ENDPOINT = "https://api.parallel.ai/v1/search"


def search(objective, queries, mode="basic", max_results=10, timeout=90):
    key = os.environ.get("PARALLEL_API_KEY", "")
    if not key:
        return {"provider": "parallel", "status": "SKIP", "reason": "PARALLEL_API_KEY absent", "results": []}
    body = {"objective": objective, "search_queries": list(queries), "mode": mode,
            "advanced_settings": {"max_results": max_results}}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "x-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:
        return {"provider": "parallel", "status": "FAIL", "reason": f"{type(e).__name__}: {e}"[:200], "results": []}
    out = []
    for x in payload.get("results", []):
        ex = x.get("excerpts") or []
        out.append({"title": x.get("title", ""), "url": x.get("url", ""),
                    "snippet": " ".join(ex)[:600], "date": x.get("publish_date", "")})
    return {"provider": "parallel", "status": "OK", "results": out}
