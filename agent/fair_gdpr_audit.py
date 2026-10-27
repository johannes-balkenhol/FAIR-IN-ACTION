#!/usr/bin/env python3
# =============================================================================
# fair_gdpr_audit.py  —  read-only FAIR + GDPR audit for a projects root
# -----------------------------------------------------------------------------
# Checks each project folder for FAIR structure and GDPR signals, and the root
# itself for detached manifests, version sprawl and loose files. READ-ONLY:
# it opens nothing for writing and changes nothing.
#
#   python3 fair_gdpr_audit.py <root> [--json report.json] [--depth 3]
#
# Examples:
#   python3 fair_gdpr_audit.py /storage/users/job37yv/Projects
#   python3 fair_gdpr_audit.py /mnt/d/Research --json audit_2026-10-25.json
#
# Tiers (estimate): bronze = README + structure + manifest-inside ·
#   silver = + schema + licence · gold = + git + a deposition accession/DOI.
# =============================================================================
import os, sys, re, json, stat, argparse
try:
    import grp
except Exception:
    grp = None

SKIP = {"_archive", "archive", "trash", "var", "downloads", ".git",
        "_versions", "_working", "node_modules", "__pycache__"}

# sensitivity = personal / clinical data handling (NOT the mere word "human",
# which appears in every reference-genome mention and is pure noise)
SENSITIVE_HINT = re.compile(
    r"(patient|donor|proband|spender|clinical|klinisch|fhir|gdpr|dsgvo|ehds|"
    r"pseudonym|ethic|ethik|consent|einwillig|identif)", re.I)
ACCESSION = re.compile(
    r"(E-MTAB-\d+|E-GEOD-\d+|GSE\d+|PRJ[EDN][A-Z]\d+|SRR\d+|PXD\d+|"
    r"10\.\d{4,9}/\S+|zenodo\.\d+)", re.I)
VERSION_IN_NAME = re.compile(
    r"(_v\d+\b|_final\b|_clean\b|_baseline\b|_backup\b|_old\b|_copy\b|"
    r"-sync\b|_sync\b|\bORGANIZED\b|_new\b)", re.I)
# bioinformatics identifiers that look like initials+digits but are NOT PII
ACCESSION_DENY = re.compile(
    r"(GC[AF]_\d|^PF\d|PDB|^DB\d{5}|ENS[A-Z]*\d|GSE\d|SRR\d|PRJ[A-Z]|"
    r"E-MTAB|GO[:_]\d|R-HSA|UniProt|\.hmm$|patsy|conda)", re.I)
# PII-in-name heuristics (flag for human review, not a verdict)
PII_NAME = re.compile(
    r"(?i)(\bpatients?\b|\bdonors?\b|patient[ _-]|donor[ _-]|proband|spender|\bsubject[ _-]?\d)")
PII_IDDATE = re.compile(r"\b[A-ZÄÖÜ]{2,4}[ _-]?\d{3,}\b")

MANIFESTS = ("project.yaml", "ro-crate-metadata.json", "project.yml",
             " arc.json", "isa.investigation.xlsx")
READMES = ("readme.md", "readme.txt", "readme")
DMP_PAT = re.compile(r"\bdmp\b|data.?management.?plan", re.I)
LICENSE_PAT = re.compile(r"^licen[sc]e", re.I)
SCHEMA_PAT = re.compile(r"(\.linkml\.ya?ml$|\.sdrf\.|\.idf\.|schema.*\.(ya?ml|json)$|sdrf.*\.tsv$)", re.I)
DATA_DIRS = ("data", "raw_data", "rawdata")
ANALYSIS_DIRS = ("analysis", "scripts", "code", "notebooks")
META_DIRS = ("metadata", "meta_data", "meta")

def modestr(path):
    try:
        st = os.stat(path)
    except Exception:
        return "?", "?", False, False
    m = stat.filemode(st.st_mode)
    gname = "?"
    if grp:
        try:
            gname = grp.getgrgid(st.st_gid).gr_name
        except Exception:
            gname = str(st.st_gid)
    grp_read = bool(st.st_mode & stat.S_IRGRP)
    oth_read = bool(st.st_mode & stat.S_IROTH)
    return m, gname, grp_read, oth_read

def listdir(path):
    try:
        return sorted(os.listdir(path))
    except Exception:
        return []

def has(names, entries_lower):
    return any(n in entries_lower for n in names)

def read_small(path, limit=200000):
    try:
        with open(path, "r", errors="ignore") as f:
            return f.read(limit)
    except Exception:
        return ""

def grep_tree(root, depth, patterns, max_files=400):
    """Return dict pattern_name->bool by scanning small text files shallowly."""
    found = {k: False for k in patterns}
    seen = 0
    base_depth = root.rstrip("/").count("/")
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        if dirpath.count("/") - base_depth > depth:
            dirnames[:] = []
            continue
        for fn in filenames:
            if not fn.lower().endswith((".md", ".txt", ".yaml", ".yml", ".json",
                                        ".cff", ".tsv", ".csv")):
                continue
            seen += 1
            if seen > max_files:
                return found
            txt = read_small(os.path.join(dirpath, fn))
            for name, pat in patterns.items():
                if not found[name] and pat.search(txt):
                    found[name] = True
    return found

def scan_names(root, depth):
    """Collect dir/file names shallowly; flag PII-in-name candidates."""
    pii = []
    base_depth = root.rstrip("/").count("/")
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP and not d.startswith(".")]
        if dirpath.count("/") - base_depth > depth:
            dirnames[:] = []
            continue
        for nm in dirnames + filenames:
            if ACCESSION_DENY.search(nm):
                continue
            if PII_NAME.search(nm) or PII_IDDATE.search(nm):
                pii.append(os.path.relpath(os.path.join(dirpath, nm), root))
    return pii[:20]

def audit_project(path, depth):
    name = os.path.basename(path.rstrip("/"))
    entries = listdir(path)
    el = {e.lower() for e in entries}
    r = {"project": name}

    # --- FAIR structure ---
    r["readme"]        = has(READMES, el)
    r["manifest"]      = has([m.strip() for m in MANIFESTS], el)
    r["dmp"]           = any(DMP_PAT.search(e) for e in entries)
    r["license"]       = any(LICENSE_PAT.match(e) for e in entries)
    r["data_dir"]      = has(DATA_DIRS, el)
    r["analysis_dir"]  = has(ANALYSIS_DIRS, el)
    r["metadata_dir"]  = has(META_DIRS, el)
    r["git"]           = ".git" in el
    # schema + deposition marker (shallow grep)
    schema_found = any(SCHEMA_PAT.search(e) for e in entries)
    grep = grep_tree(path, depth, {"ethics": SENSITIVE_HINT, "accession": ACCESSION,
                                   "retention": re.compile(r"retention|aufbewahr|deletion|lösch|delete after", re.I),
                                   "schema": SCHEMA_PAT})
    r["schema"]        = schema_found or grep["schema"]
    r["deposition"]    = grep["accession"]

    # --- naming ---
    r["name_spaces"]   = " " in name
    r["name_version"]  = bool(VERSION_IN_NAME.search(name))

    # --- GDPR ---
    sens_name = bool(SENSITIVE_HINT.search(name))
    r["sensitive"]     = sens_name or grep["ethics"]
    m, gname, gread, oread = modestr(path)
    r["mode"], r["group"] = m, gname
    r["world_readable"] = oread
    r["broad_group"]   = gread and gname in ("users", "staff", "domain users", "everyone")
    r["ethics_ref"]    = grep["ethics"]
    r["retention"]     = grep["retention"]
    r["pii_names"]     = scan_names(path, depth)

    # --- tier estimate ---
    bronze = r["readme"] and r["manifest"] and (r["data_dir"] or r["analysis_dir"])
    silver = bronze and r["schema"] and r["license"]
    gold   = silver and r["git"] and r["deposition"]
    r["tier"] = "gold" if gold else "silver" if silver else "bronze" if bronze else "—"

    # --- flags (the human-readable verdicts) ---
    flags = []
    if not r["readme"]:    flags.append("no README")
    if not r["manifest"]:  flags.append("no manifest/project.yaml")
    if not r["dmp"]:       flags.append("no DMP")
    if not r["license"]:   flags.append("no LICENSE")
    if not r["git"]:       flags.append("code not in git")
    if r["name_spaces"]:   flags.append("spaces in name")
    if r["name_version"]:  flags.append("version in folder name")
    if r["sensitive"] and (r["world_readable"] or r["broad_group"]):
        flags.append(f"GDPR: sensitive but readable by {'world' if r['world_readable'] else r['group']}")
    if r["sensitive"] and not r["ethics_ref"]:
        flags.append("GDPR: sensitive, no ethics/consent reference found")
    if r["sensitive"] and not r["retention"]:
        flags.append("GDPR: no retention/deletion concept")
    if r["pii_names"]:     flags.append(f"GDPR: possible identifiers in names (verify, e.g. {r['pii_names'][0]})")
    r["flags"] = flags
    return r

def audit_root(root):
    entries = listdir(root)
    loose, manifests_at_root, stems = [], [], {}
    for e in entries:
        p = os.path.join(root, e)
        if os.path.isfile(p):
            if e.lower().endswith((".yaml", ".yml")) and ("project" in e.lower() or "coinfection" in e.lower() or "butyrate" in e.lower()):
                manifests_at_root.append(e)
            elif not e.lower().startswith("readme") and not LICENSE_PAT.match(e):
                loose.append(e)
        elif os.path.isdir(p) and e not in SKIP and not e.startswith("."):
            stem = re.split(r"[_\-]?(v\d+|final|clean|baseline|backup|sync|new|\d{4})", e, maxsplit=1, flags=re.I)[0].rstrip("_-").lower()
            stem = re.sub(r"\d+$", "", stem).rstrip("_-")
            if len(stem) >= 3:
                stems.setdefault(stem, []).append(e)
    dups = {k: v for k, v in stems.items() if len(v) >= 3}
    return {"loose_files_at_root": loose,
            "detached_manifests_at_root": manifests_at_root,
            "version_sprawl": dups}

def main():
    ap = argparse.ArgumentParser(description="Read-only FAIR + GDPR audit of a projects root.")
    ap.add_argument("root")
    ap.add_argument("--json", default=None)
    ap.add_argument("--depth", type=int, default=3)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    projects = [os.path.join(root, e) for e in listdir(root)
                if os.path.isdir(os.path.join(root, e)) and e not in SKIP and not e.startswith(".")]
    results = [audit_project(p, a.depth) for p in projects]
    rootinfo = audit_root(root)

    # ---- human report ----
    print(f"\n=== FAIR + GDPR audit : {root} ===  ({len(results)} projects)\n")
    print(f"{'PROJECT':40} {'TIER':7} FLAGS")
    print("-" * 100)
    for r in sorted(results, key=lambda x: (x["tier"] == "—", x["project"].lower())):
        flags = "; ".join(r["flags"]) if r["flags"] else "ok"
        print(f"{r['project'][:40]:40} {r['tier']:7} {flags}")

    print("\n--- ROOT-LEVEL ---")
    if rootinfo["detached_manifests_at_root"]:
        print("  ⚠ manifest(s) loose at root (should live inside their project): "
              + ", ".join(rootinfo["detached_manifests_at_root"]))
    if rootinfo["version_sprawl"]:
        for stem, v in rootinfo["version_sprawl"].items():
            print(f"  ⚠ version sprawl '{stem}' ×{len(v)}: {', '.join(v)}")
    if rootinfo["loose_files_at_root"]:
        print(f"  ⚠ {len(rootinfo['loose_files_at_root'])} loose file(s) at root: "
              + ", ".join(rootinfo["loose_files_at_root"][:12])
              + (" …" if len(rootinfo["loose_files_at_root"]) > 12 else ""))

    # ---- summary ----
    tiers = {}
    for r in results:
        tiers[r["tier"]] = tiers.get(r["tier"], 0) + 1
    gdpr = [r["project"] for r in results if any("GDPR" in f for f in r["flags"])]
    print("\n--- SUMMARY ---")
    print("  tiers: " + ", ".join(f"{k}={v}" for k, v in sorted(tiers.items())))
    print(f"  GDPR flags on {len(gdpr)} project(s): " + (", ".join(gdpr) if gdpr else "none"))
    print("\n(heuristic + read-only; PII-in-name and sensitivity flags are candidates to verify, not verdicts.)")

    if a.json:
        with open(a.json, "w") as f:
            json.dump({"root": root, "projects": results, "root_level": rootinfo}, f, indent=2)
        print(f"\nJSON written: {a.json}")

if __name__ == "__main__":
    main()
