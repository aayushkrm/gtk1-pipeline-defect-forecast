"""Exa neural search. Docs: https://docs.exa.ai. Auth: x-api-key: $EXA_API_KEY."""
import json
import os
import urllib.request

ENDPOINT = "https://api.exa.ai/search"


def search(query, num_results=10, timeout=40):
    key = os.environ.get("EXA_API_KEY", "")
    if not key:
        return {"provider": "exa", "status": "SKIP", "reason": "EXA_API_KEY absent", "results": []}
    body = json.dumps({"query": query, "numResults": num_results}).encode()
    req = urllib.request.Request(ENDPOINT, data=body,
                                 headers={"Content-Type": "application/json", "x-api-key": key})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            payload = json.loads(r.read().decode())
    except Exception as e:
        return {"provider": "exa", "status": "FAIL", "reason": f"{type(e).__name__}: {e}"[:200], "results": []}
    out = [{"title": x.get("title", ""), "url": x.get("url", ""),
            "snippet": (x.get("text") or "")[:500]} for x in payload.get("results", [])]
    return {"provider": "exa", "status": "OK", "results": out}
