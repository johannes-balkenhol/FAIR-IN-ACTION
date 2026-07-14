#!/usr/bin/env python3
"""
gapsheet.py — generate the fill-in sheet.

The ONLY thing this emits is `source: human` fields that are still empty.
Nothing that the machine can read from your data, and nothing already in
project.yaml, ever reaches a researcher. That restraint is the whole product.

    python3 gapsheet.py --profile scrnaseq
    python3 gapsheet.py --profile proteomics-ms --project project.yaml -o gaps.csv
    python3 gapsheet.py --profile flow-cytometry --format md

The 'why we need it' column is not decoration. People answer better when they
know what breaks without the answer — so a field with no `why:` in the model
is a field that should not exist.
"""
import argparse, csv, sys, pathlib
import fairlib as fl


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help=f"one of: {', '.join(fl.list_profiles())}")
    ap.add_argument("--project", default="project.yaml")
    ap.add_argument("-o", "--out", help="output file (default: stdout)")
    ap.add_argument("--format", choices=["csv", "md"], default="csv")
    ap.add_argument("--all", action="store_true",
                    help="include human fields that are already answered")
    a = ap.parse_args()

    prof, fields = fl.load_profile(a.profile)

    proj = {}
    if pathlib.Path(a.project).exists():
        proj = fl.load_project(a.project)
    vals = fl.project_values(proj, fields)

    rows = []
    for f in fields:
        if f.source != "human":
            continue
        answered = str(vals.get(f.key, "")).strip()
        if answered and not a.all:
            continue
        rows.append({
            "field":            f["name"],
            "level":            f["level"],
            "required":         "yes" if f.required else "optional",
            "tier":             f.get("tier", ""),
            "ontology":         f.get("ontology", ""),
            "allowed values":   " | ".join(f.get("enum", [])),
            "example":          f.get("default", ""),
            "why we need it":   f.get("why", ""),
            "YOUR VALUE":       answered,
        })

    cols = ["field", "level", "required", "tier", "ontology",
            "allowed values", "example", "why we need it", "YOUR VALUE"]

    out = open(a.out, "w", newline="") if a.out else sys.stdout
    if a.format == "csv":
        w = csv.DictWriter(out, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    else:
        print(f"# Metadata still needed — {prof['profile']}\n", file=out)
        print(f"**{len(rows)} field(s).** Everything else was already filled in "
              f"from your data or from `project.yaml`.\n", file=out)
        print("| " + " | ".join(cols) + " |", file=out)
        print("|" + "---|" * len(cols), file=out)
        for r in rows:
            print("| " + " | ".join(str(r[c]).replace("|", "/") for c in cols) + " |", file=out)
    if a.out:
        out.close()

    c = fl.counts(fields)
    tot = sum(c.values())
    filled = tot - len(rows)
    print(f"\n{prof['profile']} · core v{prof['_core_version']}", file=sys.stderr)
    print(f"  machine fills {c['auto']}   project.yaml fills {c['project']}   "
          f"you fill {len(rows)}", file=sys.stderr)
    print(f"  → {round(100 * (tot - len(rows)) / tot)}% of this sheet was completed without you.",
          file=sys.stderr)
    if a.out:
        print(f"  → wrote {a.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
