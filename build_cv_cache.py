#!/usr/bin/env python3
"""
build_cv_cache.py — fetch the ontology terms this consortium actually uses,
and bake them into the app so the browser NEVER needs network access.

    python3 build_cv_cache.py                # fetch and write cv_cache.json
    python3 build_cv_cache.py && python3 build_app.py   # then rebuild the app

WHY THIS EXISTS
---------------
The live OLS4 API works from the HPC shell but NOT from the browser rendering the
app: JupyterLab serves static files under a Content-Security-Policy that blocks
cross-origin fetch. So an app that DEPENDS on the live API is broken precisely
where it is used.

The fix is not to abandon ontologies. It is to fetch them where the network works
(here), cache the terms that are actually needed, and treat the live API as an
enhancement rather than a dependency.

DO NOT download whole ontologies. CL alone is ~20 MB and goes stale. Fetch the
terms your consortium uses — a few hundred — and refresh this file when the
vocabulary grows. That is the difference between a cache and a hoard.
"""
from __future__ import annotations
import json, pathlib, sys, time, urllib.parse, urllib.request

OLS = "https://www.ebi.ac.uk/ols4/api"
ROOT = pathlib.Path(__file__).resolve().parent

# The vocabulary this consortium actually uses. Grow this list; do not grow it
# speculatively. Every term here should be one somebody has needed.
SEEDS = {
    "CL": [  # cell types — infection immunology
        "alveolar macrophage", "macrophage", "monocyte", "neutrophil",
        "dendritic cell", "conventional dendritic cell", "plasmacytoid dendritic cell",
        "epithelial cell", "epithelial cell of lung",
        "pulmonary alveolar type 1 cell", "pulmonary alveolar type 2 cell",
        "club cell", "ciliated cell", "goblet cell", "intestinal epithelial cell",
        "Paneth cell", "enterocyte", "intestinal crypt stem cell",
        "T cell", "CD4-positive, alpha-beta T cell", "CD8-positive, alpha-beta T cell",
        "regulatory T cell", "gamma-delta T cell", "innate lymphoid cell",
        "B cell", "plasma cell", "natural killer cell",
        "fibroblast", "endothelial cell", "mesenchymal cell", "eosinophil", "basophil", "mast cell",
    ],
    "UBERON": [  # anatomy
        "lung", "alveolus of lung", "bronchus", "trachea", "respiratory system",
        "colon", "small intestine", "ileum", "caecum", "duodenum",
        "intestinal mucosa", "blood", "bone marrow", "spleen", "thymus",
        "lymph node", "mesenteric lymph node", "pancreas", "liver", "skin",
        "bronchoalveolar lavage fluid",
    ],
    "NCBITaxon": [  # host and pathogen
        "Homo sapiens", "Mus musculus",
        "Aspergillus fumigatus", "Candida albicans", "Cryptococcus neoformans",
        "Clostridioides difficile", "Salmonella enterica", "Staphylococcus aureus",
        "Streptococcus pneumoniae", "Pseudomonas aeruginosa", "Escherichia coli",
        "Listeria monocytogenes", "Mycobacterium tuberculosis",
        "Influenza A virus", "Severe acute respiratory syndrome coronavirus 2",
        "Human respiratory syncytial virus", "Murine cytomegalovirus",
    ],
    "MONDO": [
        "aspergillosis", "invasive aspergillosis", "pneumonia", "sepsis",
        "Clostridioides difficile infection", "inflammatory bowel disease",
        "pancreatic adenocarcinoma", "lung adenocarcinoma", "COVID-19", "influenza",
    ],
    "CHEBI": [
        "butyrate", "short-chain fatty acid", "lipopolysaccharide", "dexamethasone",
        "gemcitabine", "cyclophosphamide", "vancomycin", "amphotericin B",
        "voriconazole", "dimethyl sulfoxide", "ATP", "poly(I:C)",
    ],
    "EFO": [
        "Illumina NovaSeq 6000", "Illumina NextSeq 500", "Illumina NextSeq 2000",
        "Illumina MiSeq", "Illumina HiSeq 4000",
        "RNA-seq of coding RNA", "single cell RNA sequencing", "ATAC-seq",
    ],
    "OBI": [
        "RNA-seq assay", "single-cell RNA sequencing assay", "mass spectrometry assay",
        "flow cytometry assay", "imaging assay",
        "nucleic acid extraction", "library construction", "nucleic acid sequencing",
    ],
    "PR": [  # flow antigens
        "CD4", "CD8a", "CD11c", "CD45", "CD3e", "CD19", "Ly6G", "Ly6C",
        "SiglecF", "F4/80", "MHC class II", "CD64", "CD11b", "NK1.1",
    ],
    "MmusDv": ["adult stage", "postnatal stage", "embryonic stage"],
}


def fetch(onto: str, q: str, rows: int = 4):
    url = (f"{OLS}/select?q={urllib.parse.quote(q)}"
           f"&ontology={onto.lower()}&rows={rows}")
    with urllib.request.urlopen(url, timeout=15) as r:
        j = json.load(r)
    docs = (j.get("response") or {}).get("docs") or []
    out = []
    for d in docs:
        cid, lab = d.get("obo_id") or d.get("short_form"), d.get("label")
        if cid and lab and cid.split(":")[0].upper() == onto.upper():
            out.append([cid, lab])
    return out


def main():
    cache, exact, fuzzy, missed = {}, 0, 0, []
    for onto, terms in SEEDS.items():
        seen, rows = set(), []
        print(f"{onto:10s} ", end="", flush=True)
        for t in terms:
            try:
                hits = fetch(onto, t)
            except Exception as e:
                print(f"\n  ! {onto}/{t}: {e}", file=sys.stderr)
                missed.append(f"{onto}:{t}")
                continue
            if not hits:
                missed.append(f"{onto}:{t}")
                print("·", end="", flush=True)
                continue
            # is the top hit an exact label match? If not, we are guessing.
            top_exact = hits[0][1].lower() == t.lower()
            exact += top_exact
            fuzzy += (not top_exact)
            print("=" if top_exact else "~", end="", flush=True)
            for cid, lab in hits:
                if cid not in seen:
                    seen.add(cid)
                    # 3rd element: was the SEED an exact label match? Unverified terms
                    # are shown differently in the app — a fuzzy hit must never
                    # masquerade as an authority.
                    rows.append([cid, lab, 1 if lab.lower() == t.lower() else 0])
            time.sleep(0.05)
        cache[onto] = rows
        print(f"  {len(rows)} terms")

    out = ROOT / "cv_cache.json"
    out.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
    total = sum(len(v) for v in cache.values())

    print(f"\n  {total} terms across {len(cache)} ontologies → cv_cache.json "
          f"({out.stat().st_size // 1024} KB)")
    print(f"  {exact} exact label matches (=), {fuzzy} fuzzy (~)")
    if fuzzy:
        print("  ~ means the top hit was NOT an exact label match. The term is cached")
        print("    anyway, but check it — a fuzzy match is how a wrong CURIE gets in.")
    if missed:
        print(f"\n  ⚠ {len(missed)} seed(s) returned nothing:")
        for m in missed[:12]:
            print(f"      {m}")
        print("    Either the label is wrong, or that ontology does not contain it.")
    print("\n  Now run:  python3 build_app.py    (bakes the cache into the app)")
    print("  The app will then work with NO network at all — which is what it needs,")
    print("  because JupyterLab's CSP blocks cross-origin fetch from the page.")


if __name__ == "__main__":
    main()
