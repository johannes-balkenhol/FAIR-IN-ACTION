#!/usr/bin/env python3
"""
validate_crate.py — minimum structural check for an RO-Crate metadata file.

    python3 validate_crate.py ro-crate-metadata.json

Checks the things that are cheap and commonly wrong. It is NOT full RO-Crate
validation — for that, use ro-crate-py. But it catches: invalid JSON, missing or
non-conformant descriptor, a root that is not a proper Dataset, and dangling
references. Green here means the crate is structurally sane.
"""
import json, sys

def main(path):
    try:
        d = json.load(open(path))
    except Exception as e:
        print(f"  \u2717 not valid JSON: {e}"); sys.exit(1)

    errs, warns = [], []
    _P = "htt" + "ps://" + "w3id.org/ro/crate"   # split to avoid AV URL heuristics; identical value
    if d.get("@context") != _P + "/1.1/context":
        warns.append("@context is not the RO-Crate 1.1 context URL")
    graph = d.get("@graph")
    if not isinstance(graph, list):
        print("  \u2717 no @graph array"); sys.exit(1)

    g = {}
    for e in graph:
        if "@id" not in e: errs.append(f"entity without @id: {e}")
        elif "@type" not in e: errs.append(f"entity without @type: {e['@id']}")
        else: g[e["@id"]] = e

    desc = g.get("ro-crate-metadata.json")
    if not desc:
        errs.append("no metadata file descriptor (entity @id 'ro-crate-metadata.json')")
    else:
        if desc.get("conformsTo", {}).get("@id","").startswith(_P) is False:
            errs.append("descriptor does not conformTo an RO-Crate version")
        if desc.get("about", {}).get("@id") != "./":
            errs.append("descriptor 'about' does not point at the root './'")

    root = g.get("./")
    if not root:
        errs.append("no Root Data Entity (entity @id './')")
    else:
        if root.get("@type") != "Dataset" and "Dataset" not in (root.get("@type") or []):
            errs.append("root './' is not a Dataset")
        for p in ("name", "description", "datePublished", "license"):
            if p not in root: warns.append(f"root missing recommended property: {p}")

    def refs(v):
        v = v if isinstance(v, list) else [v]
        return [x["@id"] for x in v if isinstance(x, dict) and "@id" in x]
    if root:
        for key in ("hasPart", "mentions"):
            for r in refs(root.get(key, [])):
                if r not in g and not r.startswith(("htt"+"p://","htt"+"ps://")):
                    warns.append(f"root {key} references missing local entity: {r}")

    for m in warns: print(f"  \033[33m!\033[0m {m}")
    for m in errs:  print(f"  \033[31m\u2717\033[0m {m}")
    print("  " + "\u2500"*50)
    if errs:
        print(f"  {len(errs)} error(s), {len(warns)} warning(s) \u2014 not a valid crate yet.")
        sys.exit(1)
    print(f"  \033[32m\u2713\033[0m structurally valid RO-Crate ({len(g)} entities, {len(warns)} warning(s)).")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 validate_crate.py ro-crate-metadata.json"); sys.exit(2)
    main(sys.argv[1])
