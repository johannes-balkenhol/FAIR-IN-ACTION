#!/usr/bin/env python3
"""
validate.py — check a project against the model, before anything leaves the building.

    python3 validate.py --profile scrnaseq
    python3 validate.py --profile scrnaseq --online     # resolve ontology terms via OLS4
    python3 validate.py --self                          # validate the TOOLKIT itself

Exit code 0 = clean, 1 = errors. Suitable for CI.

The placeholder check exists because a `<FILL IN>` survived a commit into this
repository's own CITATION.cff — the shell variable was empty, the editor never
opened, and nobody noticed. That is a machine-detectable defect, so a machine
should detect it.
"""
import argparse, pathlib, re, sys, subprocess
import fairlib as fl

PLACEHOLDERS = re.compile(r"<FILL[ _]?IN|0000-0000-0000-0000|TODO|XXXX-XXXX|CHANGEME|<your", re.I)
CURIE = re.compile(r"^[A-Za-z]+:[A-Za-z0-9_]+$")

E, W, OK = [], [], []


def err(m):  E.append(m)
def warn(m): W.append(m)
def ok(m):   OK.append(m)


def check_placeholders(root: pathlib.Path):
    """The check that would have caught the CITATION.cff slip.

    Skips matches inside `backticks`, because otherwise this check flags the
    documentation that describes it — which it did, on its first run.
    """
    hits = []
    for p in root.rglob("*"):
        if not p.is_file() or ".git" in p.parts:
            continue
        if p.suffix not in (".yaml", ".yml", ".cff", ".md", ".template", ".json", ".toml"):
            continue
        # a TEMPLATE is supposed to contain placeholders. That is what makes it a template.
        if p.name.endswith(".template") or p.name == "project.yaml.template":
            continue
        try:
            for i, line in enumerate(p.read_text(errors="ignore").splitlines(), 1):
                m = PLACEHOLDERS.search(line)
                if not m:
                    continue
                # inside a code span / inline code? then it is prose about the check.
                if line.count("`", 0, m.start()) % 2 == 1:
                    continue
                hits.append(f"{p.relative_to(root)}:{i}  {line.strip()[:70]}")
        except Exception:
            pass
    return hits


def resolve(onto, curie):
    import json, urllib.request, urllib.parse
    url = ("https://www.ebi.ac.uk/ols4/api/terms?obo_id="
           + urllib.parse.quote(curie))
    try:
        with urllib.request.urlopen(url, timeout=6) as r:
            d = json.load(r)
        terms = d.get("_embedded", {}).get("terms", [])
        return terms[0]["label"] if terms else None
    except Exception:
        return "?"          # network unavailable — cannot judge


def validate_project(profile, project_path, online):
    prof, fields = fl.load_profile(profile)
    proj = fl.load_project(project_path)
    vals = fl.project_values(proj, fields)

    for f in fields:
        v = vals.get(f.key)
        filled = str(v).strip() if v is not None else ""

        if f.source == "human" and f.required and not filled:
            err(f"missing (required, {f.get('tier','')}): {f.key} — {f['why'][:60]}")
            continue
        if f.source == "project" and f.required and not filled:
            warn(f"missing from project.yaml: {f.key}")
            continue
        if not filled:
            continue

        if f.get("enum") and filled not in f["enum"]:
            err(f"not an allowed value: {f.key} = {filled!r}\n"
                f"      allowed: {' | '.join(f['enum'])}")

        if f.get("ontology"):
            if not CURIE.match(filled):
                err(f"free text where {f['ontology']} term required: {f.key} = {filled!r}\n"
                    f"      free text joins to nothing. Search https://www.ebi.ac.uk/ols4")
            elif online:
                label = resolve(f["ontology"], filled)
                if label is None:
                    err(f"{f['ontology']} term does not exist: {f.key} = {filled}")
                elif label == "?":
                    warn(f"could not reach OLS4 to check {f.key} = {filled}")
                else:
                    ok(f"{f.key} = {filled} ({label})")

    # multi-organism sanity
    orgs = proj.get("organisms") or []
    if orgs:
        for o in orgs:
            if not o.get("role"):
                err(f"organism without a role: {o.get('label') or o.get('taxon')} — "
                    f"host? pathogen? The whole point of the organisms list is the role.")
        if len(orgs) > 1 and not any(o.get("role") == "pathogen" for o in orgs):
            warn("more than one organism but none marked pathogen — intended?")
    else:
        warn("no organisms declared")

    # the multiplexing trap
    for a in (proj.get("assays") or []):
        if a.get("multiplexed") is None:
            warn(f"assay {a.get('type')}: 'multiplexed' not declared. "
                 f"If pooled, n_libraries < n_samples — and the submission will be wrong.")

    return prof, fields


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile")
    ap.add_argument("--project", default="project.yaml")
    ap.add_argument("--online", action="store_true", help="resolve ontology terms against OLS4")
    ap.add_argument("--self", dest="selfcheck", action="store_true",
                    help="validate this toolkit repository, not a project")
    a = ap.parse_args()

    root = fl.ROOT

    if a.selfcheck:
        print("Validating the toolkit itself\n" + "─" * 60)
        for f in ("README.md", "LICENSE", "CITATION.cff", ".gitignore", "CHANGELOG.md",
                  "TIERS.md", "core_model.yaml", "project.yaml.template"):
            (ok if (root / f).exists() else err)(f"{'present' if (root/f).exists() else 'MISSING'}: {f}")
        for slug in fl.list_profiles():
            try:
                prof, fields = fl.load_profile(slug)
                nowhy = [f.key for f in fields if not f.get("why")]
                if nowhy:
                    warn(f"{slug}: {len(nowhy)} field(s) with no `why:` — "
                         f"a field you cannot justify should not exist: {', '.join(nowhy[:3])}")
                ok(f"profile parses: {slug} ({len(fields)} fields)")
            except Exception as e:
                err(f"profile FAILS to parse: {slug}: {e}")
        for h in check_placeholders(root):
            warn(f"placeholder: {h}")
    else:
        if not a.profile:
            raise SystemExit("--profile required (or use --self). "
                             f"Available: {', '.join(fl.list_profiles())}")
        prof, fields = validate_project(a.profile, a.project, a.online)
        print(f"Validating {a.project} against {prof['profile']} "
              f"(core v{prof['_core_version']})\n" + "─" * 60)
        for h in check_placeholders(pathlib.Path(a.project).parent):
            warn(f"placeholder: {h}")

    for m in OK:   print(f"  \033[32m✓\033[0m {m}")
    for m in W:    print(f"  \033[33m!\033[0m {m}")
    for m in E:    print(f"  \033[31m✗\033[0m {m}")

    print("─" * 60)
    print(f"  {len(OK)} ok · {len(W)} warning(s) · {len(E)} error(s)")
    if E:
        print("\n  Not submittable. Fix the errors above.")
    elif W:
        print("\n  Submittable, but the warnings are the difference between silver and gold.")
    else:
        print("\n  Clean.")
    sys.exit(1 if E else 0)


if __name__ == "__main__":
    main()
