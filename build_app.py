#!/usr/bin/env python3
"""
build_app.py — generates app/metadata_app.html from core_model.yaml + profiles/*.yaml

The app is NEVER hand-edited. It is generated. Change the model, re-run this.
That is the whole point: one form generator, not four forms.
"""
import yaml, json, glob, re, os, pathlib

ROOT = pathlib.Path(__file__).parent
core = yaml.safe_load(open(ROOT / "core_model.yaml"))

# ---- which category a core field belongs to (profiles declare their own) ----
PROV = {"project_id","title","description","consortium","funder_grant_id","pis",
        "contributors","data_steward","licence","sensitivity","embargo_until",
        "run_date","operator","acquisition_date","extraction_protocol"}
DESIGN = {"factors","infection"}

def category(level, name, decl):
    if "category" in decl: return decl["category"]
    if level == "project":
        if name in ("identifiers","deposition_target"): return "deposition"
        if name == "organisms": return "biological"
        return "provenance"
    if level == "sample":
        return "design" if name in DESIGN else "biological"
    if name in PROV: return "provenance"
    return "technical"

TYPE_RE = re.compile(r"^(enum|list|ref)\[(.*)\]$")

def norm(level, name, decl):
    """Flatten one field declaration into what the app needs."""
    if not isinstance(decl, dict) or "source" not in decl:
        return None
    t = str(decl.get("type", "string"))
    enum = None
    m = TYPE_RE.match(t)
    if m and m.group(1) == "enum":
        enum = [v.strip().strip('"').strip("'") for v in re.split(r",(?![^\[]*\])", m.group(2))]
        t = "enum"
    elif m:                       # list[...] / ref[...] -> free text for now
        t = "text" if "list" in t else "string"
    f = {
        "level": level, "name": name,
        "source": decl["source"],
        "category": category(level, name, decl),
        "type": t,
        "tier": decl.get("tier"),
        "why": decl.get("why", ""),
    }
    if enum: f["enum"] = enum
    if "ontology" in decl: f["ontology"] = decl["ontology"]
    if "default" in decl: f["default"] = decl["default"]
    if decl.get("required") is False: f["required"] = False
    return f

def collect(tree, level):
    """Walk one level of the model, returning flattened fields."""
    out = []
    for name, decl in (tree or {}).items():
        if not isinstance(decl, dict):
            continue
        if "source" in decl:
            f = norm(level, name, decl)
            if f: out.append(f)
        else:                       # nested group (e.g. project.identifiers)
            for n2, d2 in decl.items():
                if isinstance(d2, dict) and "source" in d2:
                    f = norm(level, n2, d2)
                    if f:
                        f["category"] = category(level, name, d2)
                        out.append(f)
    return out

CORE_FIELDS = []
for level in ("project", "protocol", "sample", "extract", "library", "assay", "file"):
    CORE_FIELDS += collect(core.get(level), level)

LABELS = {"scrnaseq":"Single-cell RNA-seq","bulk-rnaseq":"Bulk / dual RNA-seq",
          "proteomics-ms":"Proteomics (LC-MS/MS)","flow-cytometry":"Flow cytometry"}

profiles = {}
for p in sorted(glob.glob(str(ROOT / "profiles" / "*.yaml"))):
    d = yaml.safe_load(open(p))
    slug = pathlib.Path(p).stem
    fields = [dict(f) for f in CORE_FIELDS]

    # profile PROMOTES some core fields to required
    for req in d.get("requires", []):
        lvl, _, nm = req.partition(".")
        for f in fields:
            if f["level"] == lvl and f["name"] == nm:
                f.pop("required", None)
                f["tier"] = f.get("tier") or "bronze"

    # profile DEFAULTS override core
    for k, v in (d.get("defaults") or {}).items():
        for f in fields:
            if f["name"] == k and v:
                f["default"] = v

    # profile ADDS fields
    for level, group in (d.get("fields") or {}).items():
        fields += collect(group, level)

    profiles[slug] = {
        "profile": d["profile"],
        "label": LABELS.get(slug, d["profile"]),
        "fields": fields,
        "exports": d.get("exports", []),
    }

# demo values used by "Simulate import from data" — what the extractors WOULD fill
DEMO = {
    "library.library_layout":"PAIRED", "assay.instrument":"EFO:0008563 Illumina NovaSeq 6000",
    "assay.read_length":"[28, 90]", "assay.index_length":"[10, 10]", "assay.assay_id":"RUN_A01",
    "file.file_name":"S01_R1_001.fastq.gz", "file.file_type":"fastq", "file.file_role":"raw",
    "file.checksum_md5":"9f2c…e41b", "file.size_bytes":"4 812 993 021",
    "cell.n_cells":"12 486", "cell.n_genes":"21 903",
    "library.barcode_read":"R1", "library.umi_length":"12",
    "library.strandedness":"reverse", "multiorganism.per_organism_counts":"true",
    "multiorganism.pathogen_read_fraction":"0.021",
    "analysis.aligner":"STAR 2.7.11a", "analysis.counting_method":"featureCounts",
    "ms_run.ms_run_id":"RUN_20260714_01", "ms_run.instrument":"MS:1003029 Orbitrap Astral",
    "ms_run.lc_gradient_min":"44", "ms_run.isolation_window":"8", "ms_run.ms1_resolution":"120000",
    "search.n_proteins":"6 519", "search.n_peptides":"78 214",
    "fcs_run.cytometer":"BD FACSymphony A5", "fcs_run.acquisition_date":"2026-05-12",
    "fcs_run.operator":"ZA", "fcs_run.n_events":"500 000", "fcs_run.compensation":"matrix in FCS",
    "panel.markers":"⟨$PnN/$PnS keywords⟩", "analysis.gating_file":"panel3.wsp",
    "identifiers.code_doi":"10.5281/zenodo.…", "identifiers.cross_linked":"false",
    "identifiers.orcids_complete":"false",
}

MODEL = {"model_version": core["model_version"], "profiles": profiles, "demo": DEMO}

tplp = ROOT / "app" / "_template.html"
if not tplp.exists():
    raise SystemExit(
        "app/_template.html is missing.\n"
        "The app is GENERATED from this template. Without it the repo cannot rebuild\n"
        "its own app, and CI will fail. It must be committed."
    )
tpl = tplp.read_text()
out = tpl.replace("/*__MODEL_JSON__*/", json.dumps(MODEL, ensure_ascii=False))
(ROOT / "app").mkdir(exist_ok=True)
open(ROOT / "app" / "metadata_app.html", "w").write(out)

# ---- report -----------------------------------------------------------------
print(f"core v{core['model_version']}  ->  app/metadata_app.html  ({len(out)//1024} KB)\n")
print(f"{'profile':22s} {'fields':>7s} {'machine':>8s} {'project':>8s} {'YOU':>5s} {'exports':>8s}")
print("-" * 64)
for slug, p in profiles.items():
    c = {"auto":0, "project":0, "human":0}
    for f in p["fields"]: c[f["source"]] += 1
    tot = sum(c.values())
    print(f"{p['label']:22s} {tot:7d} {c['auto']:8d} {c['project']:8d} {c['human']:5d} {len(p['exports']):8d}")
print("-" * 64)
print("The 'YOU' column is the only one a human ever sees. Keeping it small is the job.")
