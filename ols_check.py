#!/usr/bin/env python3
"""
Diagnose the ontology lookup. Run this ON THE MACHINE WHOSE BROWSER IS FAILING.

    python3 ols_check.py

It answers the only question that matters: is EBI reachable, and does the API
still return the shape the app expects? If the network is fine but the shape has
changed, that is OLS's fault, not yours — and the app now falls back rather than
failing silently.
"""
import json, sys, urllib.request

OLS = "https://www.ebi.ac.uk/ols4/api"
TESTS = [
    ("select", f"{OLS}/select?q=alveolar%20macrophage&ontology=cl&rows=3"),
    ("search", f"{OLS}/search?q=alveolar%20macrophage&ontology=cl&rows=3"),
]

def shape(j):
    if isinstance(j.get("response"), dict) and isinstance(j["response"].get("docs"), list):
        return "response.docs", j["response"]["docs"]
    emb = j.get("_embedded") or {}
    if isinstance(emb.get("terms"), list):
        return "_embedded.terms", emb["terms"]
    return None, None

ok = False
for name, url in TESTS:
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            j = json.load(r)
        path, docs = shape(j)
        if path is None:
            print(f"  ✗ /{name}: reachable, but response shape UNKNOWN")
            print(f"      top-level keys: {list(j)[:6]}")
            continue
        print(f"  ✓ /{name}: {len(docs)} hit(s), shape = {path}")
        for d in docs[:3]:
            print(f"      {d.get('obo_id') or d.get('short_form')}  {d.get('label')}")
        ok = True
    except Exception as e:
        print(f"  ✗ /{name}: {type(e).__name__}: {e}")

print()
if ok:
    print("  OLS4 is reachable and the shape is understood.")
    print("  If the APP still fails, the problem is in the BROWSER, not the network:")
    print("    · opening the file via file:// → origin is 'null', some CORS setups reject it")
    print("      → serve it instead:  python3 -m http.server 8000   then open http://localhost:8000/app/metadata_app.html")
    print("    · a corporate proxy or extension blocking cross-origin fetch")
    print("    · open the browser console (F12) and read the actual error")
else:
    print("  EBI is not reachable from here. The app will fall back to its bundled")
    print("  cache and now SAYS SO in the rail, instead of failing silently.")
    print("  On an air-gapped HPC this is expected — use the app from your laptop.")
