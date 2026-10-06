"""TinyFish search (structured snippets; research_paper mode for academic).
Docs: https://docs.tinyfish.ai. GET https://api.search.tinyfish.ai, X-API-Key header.
Auth: $TINYFISH_API_KEY."""
import os
import urllib.parse
import urllib.request
import json

ENDPOINT = "https://api.search.tinyfish.ai"


def search(query, domain_type="web", language="en", timeout=40):
    key = os.environ.get("TINYFISH_API_KEY", "")
    if not key:
        return {"provider": "tinyfish", "status": "SKIP", "reason": "TINYFISH_API_KEY absent", "results": []}
    qs = urllib.parse.urlencode({"query": query, "domain_type": domain_type, "language": language})
    req = urllib.request.Request(f"{ENDPOINT}?{qs}", headers={"X-API-Key": key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:
        return {"provider": "tinyfish", "status": "FAIL", "reason": f"{type(e).__name__}: {e}"[:200], "results": []}
    out = [{"title": x.get("title", ""), "url": x.get("url", ""),
            "snippet": (x.get("snippet") or "")[:500]} for x in payload.get("results", [])]
    return {"provider": "tinyfish", "status": "OK", "results": out}
