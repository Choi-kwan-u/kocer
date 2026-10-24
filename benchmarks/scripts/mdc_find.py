"""Find Common Voice Korean on Mozilla Data Collective. Key from env MDC_API_KEY (never stored)."""
import os, sys, json, requests
KEY = os.environ["MDC_API_KEY"]
H = {"Authorization": "Bearer " + KEY}
BASE = "https://datacollective.mozillafoundation.org/api/"

def get(path, **params):
    r = requests.get(BASE + path, headers=H, params=params, timeout=60)
    r.raise_for_status()
    return r.json()

first = get("datasets/")
print("top-level keys:", {k: v for k, v in first.items() if k != "items"})
print("item keys:", list(first["items"][0].keys()))
seen, hits, page = 0, [], first
pages = 0
while True:
    for it in page["items"]:
        seen += 1
        blob = json.dumps(it, ensure_ascii=False).lower()
        if ("korean" in blob or '"ko"' in blob or "한국어" in blob) and ("common voice" in blob or "commonvoice" in blob or "common-voice" in blob):
            hits.append({k: it.get(k) for k in ("id", "slug", "name", "sizeBytes", "locale", "language", "version", "createdAt")})
    pages += 1
    nxt = page.get("nextCursor") or page.get("next_cursor") or page.get("next") or (page.get("pagination") or {}).get("nextCursor")
    if not nxt or pages > 200:
        break
    page = get("datasets/", cursor=nxt)
print("scanned", seen, "datasets in", pages, "pages")
for h in hits:
    print(json.dumps(h, ensure_ascii=False))
