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
        "lymph node", "mesenteric lymph node", "pancreas", "liver",
        "skin of body",          # UBERON has no bare "skin" — only specific regions
        # "bronchoalveolar lavage fluid" REMOVED: zero candidates in UBERON.
        # BAL is a COLLECTION METHOD, not an anatomical structure. It goes in
        # sample.characteristics[] as {name: sample collection method, value: BAL}.
        # This matters: BAL is likely A06's most common sample type.
    ],
    "NCBITaxon": [  # host and pathogen
        "Homo sapiens", "Mus musculus",
        "Aspergillus fumigatus", "Candida albicans", "Cryptococcus neoformans",
        "Clostridioides difficile", "Salmonella enterica", "Staphylococcus aureus",
        "Streptococcus pneumoniae", "Pseudomonas aeruginosa", "Escherichia coli",
        "Listeria monocytogenes", "Mycobacterium tuberculosis",
        "Influenza A virus", "Severe acute respiratory syndrome coronavirus 2",
        # NCBI renamed both of these. The old names now resolve only to STRAINS,
        # which is a silent downgrade in specificity — and a warning that a cached
        # taxonomy rots. Re-run this script periodically and diff.
        "human respiratory syncytial virus",   # species level (was: "Human respiratory syncytial virus")
        "Murid betaherpesvirus 1",             # species level (was: "Murine cytomegalovirus")
    ],
    "MONDO": [
        "aspergillosis", "invasive aspergillosis", "pneumonia",
        # "sepsis" REMOVED: MONDO returns only qualified variants ("bacterial
        # infectious disease with sepsis", "sepsis, non-human animal"). Check OLS4
        # by hand and add the right CURIE, or leave it to live search. Do not guess.
        "Clostridium difficile colitis",   # the HUMAN disease term. "Clostridioides
                                           # difficile infection" resolves only to the
                                           # non-human-animal variant, which is wrong.
        "inflammatory bowel disease",
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
        "RNA-seq of coding RNA", "single-cell RNA sequencing", "ATAC-seq",   # hyphen!
        # ArrayExpress IDF protocol types come from EFO, NOT OBI. These exact labels
        # are what the IDF expects; OBI has no protocol terms at this level.
        "growth protocol", "treatment protocol",
        "nucleic acid extraction protocol",
        "nucleic acid library construction protocol",
        "nucleic acid sequencing protocol",
        "normalization data transformation protocol",
    ],
    "OBI": [
        # ASSAY TYPES ONLY. Protocol types were moved to EFO, because OBI does not
        # have them: querying OBI for "nucleic acid sequencing" returns
        # OBI:0001108 "nucleic acid sequencer" — a DEVICE — and for "library
        # construction" it returns "number of PCR cycles during library
        # construction" — a MEASUREMENT. An IDF built on those would not validate.
        "RNA-seq assay", "single-cell RNA sequencing assay", "mass spectrometry assay",
        "flow cytometry assay", "imaging assay",
    ],
    # PR REMOVED — 14/14 seeds failed, and the "matches" were worse than the misses:
    #   CD4  -> PR:P16070-10  CD44 antigen isoform h10   (a DIFFERENT protein)
    #   CD8a -> PR:F1NXT4     uncharacterized protein, chicken
    # The Protein Ontology names protein ENTITIES; immunologists name antibody
    # TARGETS. These are different vocabularies and no query tuning bridges them.
    # Flow markers are now a hand-curated list (MARKERS, below), and the antibody
    # itself is identified by RRID — which is the actual unambiguous identifier.
    "MmusDv": [
        # MmusDv has no bare "adult stage" — it is granular by design.
        "young adult stage", "prime adult stage", "late adult stage",
        "postnatal stage", "embryonic stage",
    ],
}


def _query(url, onto):
    with urllib.request.urlopen(url, timeout=15) as r:
        j = json.load(r)
    docs = (j.get("response") or {}).get("docs") or []
    out = []
    for d in docs:
        cid, lab = d.get("obo_id") or d.get("short_form"), d.get("label")
        if cid and lab and cid.split(":")[0].upper() == onto.upper():
            out.append([cid, lab])
    return out


# Hand-curated flow marker vocabulary. Not an ontology — a controlled list.
# ~30 markers is an hour of work and gives something defensible, which is more
# than a wrong PR CURIE ever will. Add to it as panels grow.
MARKERS = [
    "CD3e", "CD4", "CD8a", "CD11b", "CD11c", "CD19", "CD44", "CD45", "CD45R/B220",
    "CD62L", "CD64", "CD69", "CD86", "CD103", "CD115", "CD117/c-Kit", "CD127",
    "CD206", "F4/80", "Ly6C", "Ly6G", "MHC class I", "MHC class II (I-A/I-E)",
    "NK1.1", "NKp46", "SiglecF", "TCRb", "TCRgd", "Ter119", "FoxP3", "Ki-67",
    "IFN-gamma", "TNF-alpha", "IL-17A", "Live/Dead",
]


def fetch(onto: str, q: str, rows: int = 4):
    """EXACT MATCH FIRST. This is the whole fix.

    The first version went straight to a ranked fuzzy search, and OLS happily
    ranked a more specific CHILD above the term asked for:
        skin                    -> "pedal digit skin"
        nucleic acid sequencing -> "nucleic acid extraction"
        COVID-19                -> "post-COVID-19 disorder"
    Every one of those labels exists exactly. We simply never asked for it.
    """
    qq = urllib.parse.quote(q)
    o = onto.lower()
    exact = _query(f"{OLS}/search?q={qq}&ontology={o}&exact=true&queryFields=label&rows=3", onto)
    if exact:
        return exact, True
    fuzzy = _query(f"{OLS}/select?q={qq}&ontology={o}&rows={rows}", onto)
    return fuzzy, False


def main():
    cache, exact, fuzzy, missed = {}, 0, 0, []
    for onto, terms in SEEDS.items():
        seen, rows = set(), []
        print(f"{onto:10s} ", end="", flush=True)
        for t in terms:
            try:
                hits, was_exact = fetch(onto, t)
            except Exception as e:
                print(f"\n  ! {onto}/{t}: {e}", file=sys.stderr)
                missed.append(f"{onto}:{t}")
                continue
            if not hits:
                missed.append(f"{onto}:{t}")
                print("·", end="", flush=True)
                continue
            # exact endpoint hit, or the top fuzzy hit happens to match the label
            top_exact = was_exact or hits[0][1].lower() == t.lower()
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

    # the curated marker list ships as its own vocabulary, with no CURIEs,
    # because an honest free-text controlled list beats a confident wrong CURIE.
    cache["MARKER"] = [[m, m, 1] for m in MARKERS]
    print(f"{'MARKER':10s} {'=' * len(MARKERS)}  {len(MARKERS)} terms (hand-curated, no ontology)")

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
