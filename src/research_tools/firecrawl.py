"""Firecrawl search (web + full-page markdown). Docs: https://docs.firecrawl.dev.
POST https://api.firecrawl.dev/v2/search, Bearer auth. Auth: $FIRECRAWL_API_KEY."""
import json
import os
import urllib.request

ENDPOINT = "https://api.firecrawl.dev/v2/search"


def search(query, limit=10, scrape=False, timeout=60):
    key = os.environ.get("FIRECRAWL_API_KEY", "")
    if not key:
        return {"provider": "firecrawl", "status": "SKIP", "reason": "FIRECRAWL_API_KEY absent", "results": []}
    body = {"query": query, "limit": limit}
    if scrape:
        body["scrapeOptions"] = {"formats": ["markdown"], "onlyMainContent": True}
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:
        return {"provider": "firecrawl", "status": "FAIL", "reason": f"{type(e).__name__}: {e}"[:200], "results": []}
    out = [{"title": x.get("title", ""), "url": x.get("url", ""),
            "snippet": (x.get("description") or x.get("markdown") or "")[:500]}
           for x in payload.get("data", {}).get("web", [])]
    return {"provider": "firecrawl", "status": "OK", "results": out}
