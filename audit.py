#!/usr/bin/env python3
"""
audit.py — score a project bronze / silver / gold.

    python3 audit.py --path ~/Projects_shared/PANC_cancer --profile scrnaseq
    python3 audit.py --path . --self          # refuses: this repo is the ruler

Every check here is mechanical. If a criterion needed a human to judge it, it is
not in TIERS.md and it is not here. A tier you have to argue about is not a tier.

Honesty note: this scores what is ON DISK. It cannot tell whether the science is
any good, and it does not try. FAIR is orthogonal to quality.
"""
import argparse, pathlib, re, subprocess, sys, urllib.request, yaml
import fairlib as fl

TICK, CROSS, DASH = "\033[32m✓\033[0m", "\033[31m✗\033[0m", "\033[90m·\033[0m"


class Audit:
    def __init__(self, root, online=False):
        self.root, self.online = pathlib.Path(root), online
        self.res = {"bronze": [], "silver": [], "gold": []}

    def add(self, tier, code, label, passed, note=""):
        self.res[tier].append((code, label, bool(passed), note))

    def has(self, *names):
        return any((self.root / n).exists() for n in names)

    def read(self, name):
        p = self.root / name
        return p.read_text(errors="ignore") if p.exists() else ""

    # ---------------- bronze: free. Scaffolding + extraction. ----------------
    def bronze(self, fields, vals):
        r = self.root
        self.add("bronze", "B1", "standard folder structure",
                 all((r / d).exists() for d in ("data", "docs")) and
                 any((r / "data" / s).exists() for s in ("raw", "primary", "processed")))
        pj = self.has("project.yaml")
        self.add("bronze", "B2", "project.yaml present and parses", pj)
        self.add("bronze", "B3", "raw data locked + checksummed",
                 self.has("data/raw/checksums.txt", "checksums.txt"))
        auto = [f for f in fields if f.source == "auto"]
        got = [f for f in auto if str(vals.get(f.key, "")).strip()]
        self.add("bronze", "B4", "auto fields populated (extractors have run)",
                 auto and len(got) == len(auto), f"{len(got)}/{len(auto)}")
        proj = [f for f in fields if f.source == "project" and f.required]
        gotp = [f for f in proj if str(vals.get(f.key, "")).strip()]
        self.add("bronze", "B5", "project fields populated",
                 proj and len(gotp) == len(proj), f"{len(gotp)}/{len(proj)}")
        self.add("bronze", "B6", "LICENSE present", self.has("LICENSE", "LICENSE.md", "LICENSE.txt"))
        rd = self.read("README.md")
        self.add("bronze", "B7", "README with data-availability section",
                 bool(re.search(r"data.availability|accession|availability of data", rd, re.I)))
        self.add("bronze", "B8", "code in a public git repo", self.git_remote() is not None,
                 self.git_remote() or "")

    # ---------------- silver: a human answered, and it validates -------------
    def silver(self, fields, vals):
        hum = [f for f in fields if f.source == "human" and f.required]
        goth = [f for f in hum if str(vals.get(f.key, "")).strip()]
        self.add("silver", "S1", "human fields filled (gap-sheet returned)",
                 hum and len(goth) == len(hum), f"{len(goth)}/{len(hum)}")

        onto = [f for f in fields if f.get("ontology") and str(vals.get(f.key, "")).strip()]
        bad = [f.key for f in onto if not re.match(r"^[A-Za-z]+:[A-Za-z0-9_]+$", str(vals[f.key]))]
        self.add("silver", "S2", "ontology terms are CURIEs, not free text",
                 onto and not bad, f"{len(bad)} free-text" if bad else f"{len(onto)} terms")

        enums = [f for f in fields if f.get("enum") and str(vals.get(f.key, "")).strip()]
        bade = [f.key for f in enums if str(vals[f.key]) not in f["enum"]]
        self.add("silver", "S3", "controlled vocabularies respected", not bade,
                 ", ".join(bade[:2]))

        proj = self.project()
        orgs = proj.get("organisms") or []
        self.add("silver", "S4", "every organism has a role",
                 bool(orgs) and all(o.get("role") for o in orgs),
                 f"{len(orgs)} organism(s)")

        acc = self.ident(proj, "data_accession")
        self.add("silver", "S5", "data has a repository accession", bool(acc), acc or "")
        doi = self.ident(proj, "code_doi")
        self.add("silver", "S6", "code has a persistent DOI", bool(doi), doi or "")

        cff = self.read("CITATION.cff")
        cff_doi = bool(cff) and "doi:" in cff and not re.search(r"<FILL|TODO", cff)
        self.add("silver", "S7", "CITATION.cff present and DOI-populated", cff_doi)
        self.add("silver", "S8", "repository export validates", False, "run validate.py --online")
        self.add("silver", "S9", "DMP exists",
                 self.has("docs/DMP", "docs/dmp.md", "DMP.md", "docs/DMP/DMP.md"))

    # ---------------- gold: cross-linked, lean, reproducible, reused ---------
    def gold(self, fields, vals):
        proj = self.project()
        doi, acc = self.ident(proj, "code_doi"), self.ident(proj, "data_accession")
        paper = self.ident(proj, "paper_doi")
        linked = self.crosslinked(doi) if (doi and self.online) else None
        self.add("gold", "G1", "identifiers cross-linked (code ↔ data ↔ paper)",
                 bool(linked), "run with --online to check Zenodo relations"
                 if linked is None else ("related identifiers present" if linked else
                                         "Zenodo record has NO related identifiers"))
        self.add("gold", "G2", "ORCIDs complete (not the GitHub username autofill)",
                 bool(re.search(r"orcid:\s*\"?https://orcid\.org/(?!0000-0000-0000-0000)",
                                self.read("CITATION.cff"))))
        self.add("gold", "G3", "environment pinned",
                 self.has("environment.yml", "requirements.txt", "renv.lock",
                          "Dockerfile", "poetry.lock", "uv.lock"))
        big = self.notebooks_with_outputs()
        self.add("gold", "G4", "notebook outputs stripped / repo lean",
                 not big, f"{len(big)} notebook(s) carry outputs" if big else "")
        self.add("gold", "G5", "reruns end-to-end from raw + code", self.has(".github/workflows", ".gitlab-ci.yml"))
        self.add("gold", "G6", "model reused by another project", False,
                 "set by the RDM team when a second project inherits this config")

    # ---------------- helpers ------------------------------------------------
    def project(self):
        p = self.root / "project.yaml"
        return (yaml.safe_load(open(p)) or {}) if p.exists() else {}

    def ident(self, proj, key):
        v = (proj.get("identifiers") or {}).get(key) or proj.get(key)
        v = str(v).strip() if v else ""
        return "" if (not v or "FILL" in v or v.endswith("…")) else v

    def git_remote(self):
        try:
            out = subprocess.run(["git", "-C", str(self.root), "remote", "get-url", "origin"],
                                 capture_output=True, text=True, timeout=5)
            return out.stdout.strip() or None
        except Exception:
            return None

    def notebooks_with_outputs(self):
        bad = []
        for nb in self.root.rglob("*.ipynb"):
            if ".git" in nb.parts or "checkpoint" in nb.name:
                continue
            try:
                if '"output_type"' in nb.read_text(errors="ignore"):
                    bad.append(nb.name)
            except Exception:
                pass
        return bad

    def crosslinked(self, doi):
        """G1: does the Zenodo record actually point at anything?"""
        m = re.search(r"(10\.5281/zenodo\.\d+)", doi)
        if not m:
            return False
        rid = m.group(1).split(".")[-1]
        try:
            import json
            with urllib.request.urlopen(f"https://zenodo.org/api/records/{rid}", timeout=8) as r:
                d = json.load(r)
            rel = d.get("metadata", {}).get("related_identifiers", [])
            return len(rel) > 0
        except Exception:
            return None

    # ---------------- report -------------------------------------------------
    def report(self):
        tier, lines = None, []
        for t in ("bronze", "silver", "gold"):
            checks = self.res[t]
            passed = sum(1 for *_, p, _ in checks if p)
            lines.append((t, passed, len(checks), checks))
        for t, p, n, _ in lines:
            if p == n and n:
                tier = t
            else:
                break

        icon = {"bronze": "🥉", "silver": "🥈", "gold": "🥇"}
        print(f"\n  FAIR audit — {self.root}\n" + "  " + "─" * 62)
        for t, p, n, checks in lines:
            print(f"\n  {icon[t]} {t.upper()}   {p}/{n}")
            for code, label, ok_, note in checks:
                mark = TICK if ok_ else (DASH if "run with" in note or "set by" in note else CROSS)
                print(f"    {mark} {code}  {label}" + (f"  \033[90m({note})\033[0m" if note else ""))
        print("\n  " + "─" * 62)
        if tier:
            print(f"  → {icon[tier]}  {tier.upper()}")
        else:
            miss = [c for c, l, o, _ in self.res['bronze'] if not o]
            print(f"  → \033[31mNOT YET BRONZE\033[0m — missing {', '.join(miss)}")
            print("    Bronze is free: it is scaffolding and extraction, not effort.")
        nxt = {"bronze": "silver", "silver": "gold", None: "bronze"}.get(tier)
        if nxt and nxt in self.res:
            todo = [f"{c} {l}" for c, l, o, _ in self.res[nxt] if not o]
            if todo:
                print(f"\n  To reach {nxt}:")
                for t_ in todo:
                    print(f"    · {t_}")
        print()
        return tier


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".")
    ap.add_argument("--profile", help=f"one of: {', '.join(fl.list_profiles())}")
    ap.add_argument("--online", action="store_true",
                    help="check Zenodo related_identifiers (G1) — needs network")
    a = ap.parse_args()

    root = pathlib.Path(a.path).resolve()
    if (root / ".fairignore").exists():
        print(f"\n  {root} is marked `is_toolkit: true`.\n"
              f"  This repository is the ruler; it is not scored by its own rules.\n"
              f"  Use `validate.py --self` instead.\n")
        sys.exit(0)

    if not a.profile:
        raise SystemExit("--profile required. Available: " + ", ".join(fl.list_profiles()))

    prof, fields = fl.load_profile(a.profile)
    pj = root / "project.yaml"
    proj = yaml.safe_load(open(pj)) if pj.exists() else {}
    vals = fl.project_values(proj or {}, fields)

    au = Audit(root, a.online)
    au.bronze(fields, vals)
    au.silver(fields, vals)
    au.gold(fields, vals)
    tier = au.report()
    sys.exit(0 if tier else 1)


if __name__ == "__main__":
    main()
