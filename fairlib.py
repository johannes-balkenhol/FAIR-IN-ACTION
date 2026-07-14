#!/usr/bin/env python3
"""
fairlib.py — the one place the model is loaded and flattened.

build_app.py, gapsheet.py, validate.py and audit.py ALL go through this.
If they each parsed the YAML themselves they would drift, and a metadata
toolkit whose own tools disagree about the schema is worse than none.
"""
from __future__ import annotations
import re, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent

PROV = {"project_id", "title", "description", "consortium", "funder_grant_id", "pis",
        "contributors", "data_steward", "licence", "sensitivity", "embargo_until",
        "run_date", "operator", "acquisition_date", "extraction_protocol"}
DESIGN = {"factors", "infection"}
TYPE_RE = re.compile(r"^(enum|list|ref)\[(.*)\]$")

CATEGORIES = [
    ("biological",  "Biological"),
    ("design",      "Experimental design"),
    ("technical",   "Technical / assay"),
    ("provenance",  "Provenance & people"),
    ("deposition",  "Deposition & identifiers"),
]


class Field(dict):
    """A flattened field. dict for easy JSON dumping, attrs for readability."""
    @property
    def key(self):      return f"{self['level']}.{self['name']}"
    @property
    def source(self):   return self["source"]
    @property
    def required(self): return self.get("required", True)


def _category(level, name, decl):
    if "category" in decl:
        return decl["category"]
    if level == "project":
        if name in ("identifiers", "deposition_target"): return "deposition"
        if name == "organisms": return "biological"
        return "provenance"
    if level == "sample":
        return "design" if name in DESIGN else "biological"
    return "provenance" if name in PROV else "technical"


def _norm(level, name, decl, group=None):
    if not isinstance(decl, dict) or "source" not in decl:
        return None
    t = str(decl.get("type", "string"))
    enum = None
    m = TYPE_RE.match(t)
    if m and m.group(1) == "enum":
        enum = [v.strip().strip('"').strip("'")
                for v in re.split(r",(?![^\[]*\])", m.group(2))]
        t = "enum"
    elif m:
        t = "text" if t.startswith("list") else "string"
    f = Field(level=level, name=name, source=decl["source"],
              category=_category(level, group or name, decl),
              type=t, tier=decl.get("tier"), why=decl.get("why", ""))
    if enum:                      f["enum"] = enum
    if "ontology" in decl:        f["ontology"] = decl["ontology"]
    if "default" in decl:         f["default"] = decl["default"]
    if decl.get("required") is False: f["required"] = False
    return f


def _collect(tree, level):
    out = []
    for name, decl in (tree or {}).items():
        if not isinstance(decl, dict):
            continue
        if "source" in decl:
            f = _norm(level, name, decl)
            if f: out.append(f)
        else:                                   # nested group, e.g. project.identifiers
            for n2, d2 in decl.items():
                f = _norm(level, n2, d2, group=name)
                if f: out.append(f)
    return out


def load_core(root: pathlib.Path = ROOT):
    return yaml.safe_load(open(root / "core_model.yaml"))


def core_fields(core):
    out = []
    for level in ("project", "sample", "extract", "library", "assay", "file"):
        out += _collect(core.get(level), level)
    return out


def list_profiles(root: pathlib.Path = ROOT):
    return sorted(p.stem for p in (root / "profiles").glob("*.yaml"))


def load_profile(slug, root: pathlib.Path = ROOT):
    """Return (profile_dict, [Field]) — core overlaid with the assay profile."""
    core = load_core(root)
    path = root / "profiles" / f"{slug}.yaml"
    if not path.exists():
        raise SystemExit(f"no such profile: {slug}. Available: {', '.join(list_profiles(root))}")
    prof = yaml.safe_load(open(path))
    fields = [Field(f) for f in core_fields(core)]

    for req in prof.get("requires", []):        # profile promotes core fields to required
        lvl, _, nm = req.partition(".")
        for f in fields:
            if f["level"] == lvl and f["name"] == nm:
                f.pop("required", None)
                f["tier"] = f.get("tier") or "bronze"

    for k, v in (prof.get("defaults") or {}).items():   # profile defaults win
        if not v:
            continue
        for f in fields:
            if f["name"] == k:
                f["default"] = v

    for level, group in (prof.get("fields") or {}).items():   # profile adds fields
        fields += _collect(group, level)

    prof["_core_version"] = core["model_version"]
    return prof, fields


def load_project(path="project.yaml"):
    p = pathlib.Path(path)
    if not p.exists():
        raise SystemExit(f"{path} not found. Copy project.yaml.template and fill it in.")
    return yaml.safe_load(open(p)) or {}


def project_values(proj: dict, fields):
    """Map the flat project.yaml keys onto model field keys."""
    vals = {}
    flat = {}
    for k, v in proj.items():
        flat[k] = v
        if isinstance(v, dict):
            for k2, v2 in v.items():
                flat[k2] = v2
    for f in fields:
        for cand in (f.key, f"{f['level']}_{f['name']}", f["name"]):
            if cand in flat and flat[cand] not in (None, "", []):
                vals[f.key] = flat[cand]
                break
        else:
            if "default" in f:
                vals[f.key] = f["default"]
    return vals


def counts(fields):
    c = {"auto": 0, "project": 0, "human": 0}
    for f in fields:
        c[f.source] += 1
    return c
