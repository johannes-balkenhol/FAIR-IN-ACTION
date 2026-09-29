#!/usr/bin/env python3
"""
fair_scan.py — scan project folders and score FAIR readiness. READ-ONLY.

    python3 fair_scan.py ~/Projects_shared                 # scan all subfolders
    python3 fair_scan.py ~/Projects_shared/DECIDE_A03_...   # one project

This is the AUTOMATION layer (maturity path step 2): it does the mechanical checks a
human would do by eye. It never guesses biology and never modifies anything. Pair it with
the Claude Code `fair-auditor` agent (which adds judgement + the action list) or run alone
for a fast tier map across many projects.
"""
import os, sys, re, pathlib, json

def find(root, *names):
    low = {p.name.lower(): p for p in root.iterdir() if p.exists()} if root.is_dir() else {}
    for n in names:
        if n.lower() in low: return low[n.lower()]
    return None

def has_any(root, patterns):
    for pat in patterns:
        if list(root.glob(pat)): return True
    return False

def score(proj: pathlib.Path):
    r = {"name": proj.name, "present": [], "bronze": {}, "silver": {}, "gdpr": "N/A"}
    # bronze
    data = find(proj, "data")
    r["bronze"]["structure"] = bool(data and any((data/d).exists() for d in
        ("raw_data","raw","primary_data","primary")))
    r["bronze"]["README"] = bool(find(proj, "README.md", "readme.md"))
    r["bronze"]["LICENSE"] = bool(find(proj, "LICENSE", "LICENSE.md", "LICENSE.txt"))
    r["bronze"]["DMP"] = bool(find(proj, "DMP.md", "dmp.md"))
    r["bronze"]["checksums"] = has_any(proj, ["**/md5*", "**/*checksums*", "**/*.md5"])
    r["bronze"]["env"] = bool(find(proj, "environment.yml", "requirements.txt", "renv.lock"))
    # silver
    r["silver"]["metadata"] = has_any(proj, ["**/*.sdrf*", "**/*.idf*", "**/*metadata*"])
    r["silver"]["scripts"] = bool(find(proj, "scripts", "code"))
    r["silver"]["results"] = bool(find(proj, "results"))
    # gdpr heuristic — flag folders that name clinical/patient
    if re.search(r"clinical|patient|human|CLINICAL", proj.name, re.I):
        r["gdpr"] = "⚠ check — name suggests sensitive data; verify handling"
    # assay heuristic (never assert biology, just note signals)
    signals = []
    if has_any(proj, ["**/*.h5ad"]): signals.append("scRNA-seq?(h5ad)")
    if has_any(proj, ["**/refs/*", "**/combined/*"]): signals.append("multi-ref/organism?")
    if has_any(proj, ["**/*.fcs"]): signals.append("flow?(fcs)")
    if has_any(proj, ["**/*.raw", "**/*.mzML"]): signals.append("MS?(raw)")
    r["assay_signals"] = signals or ["not determinable from files"]

    nb = sum(r["bronze"].values()); ns = sum(r["silver"].values())
    if nb >= 5:
        r["tier"] = "silver" if ns >= 3 else "bronze"
    else:
        r["tier"] = "not-yet-bronze"
    return r

def main(path):
    root = pathlib.Path(path).expanduser()
    if not root.is_dir(): sys.exit(f"not a dir: {root}")
    # is this one project (has README/data) or a parent of many?
    projs = [root] if (root/"data").exists() or (root/"README.md").exists() else \
            sorted(d for d in root.iterdir() if d.is_dir() and not d.name.startswith(('.','_')))
    rows = []
    for p in projs:
        try: rows.append(score(p))
        except Exception as e: print(f"  ! {p.name}: {e}", file=sys.stderr)
    # report
    print(f"\n  FAIR scan — {len(rows)} project(s) under {root}\n  " + "─"*66)
    icon = {"gold":"🥇","silver":"🥈","bronze":"🥉","not-yet-bronze":"·"}
    for r in rows:
        miss_b = [k for k,v in r["bronze"].items() if not v]
        miss_s = [k for k,v in r["silver"].items() if not v]
        print(f"\n  {icon[r['tier']]} {r['tier']:14s} {r['name']}")
        print(f"     signals: {', '.join(r['assay_signals'])}")
        if miss_b: print(f"     for bronze: {', '.join(miss_b)}")
        elif miss_s: print(f"     for silver: {', '.join(miss_s)}")
        if r['gdpr'] != "N/A": print(f"     GDPR: {r['gdpr']}")
    print("\n  " + "─"*66)
    from collections import Counter
    c = Counter(r['tier'] for r in rows)
    print(f"  {dict(c)}\n")
    print("  This is a READ-ONLY signal scan. It never guesses biology and never edits.")
    print("  For the full action list + judgement, use the Claude Code `fair-auditor` agent.")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else ".")
