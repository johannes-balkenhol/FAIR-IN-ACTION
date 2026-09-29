# The metadata schema database — design & roadmap

*The growing, topic-wise database of per-assay metadata schemas that the HTML collection app
(github.com/johannes-balkenhol/FAIR-IN-ACTION/tree/main/app) loads. This is the long-term
build — architected here, grown one real submission at a time.*

## The two axes

Every schema is organised on two axes:

**Axis 1 — assay/topic** (one schema per):
- `scRNAseq-10x` (single-cell 10x Genomics) — ✅ gold template E-MTAB-17360
- `bulk-RNAseq`
- `dual-RNAseq` (host + pathogen)
- `triple-RNAseq` (host + bacterium + phage — A03)
- `PacBio` (long-read / chromosome / genome assembly)
- `flow-cytometry` / `flow-video`
- `proteomics-MS` (mass spec)
- `phosphoproteomics-MSMS`
- `imaging` (microscopy → REMBI)
- `clinical` (patient → FHIR)
- … grows as projects arrive

**Axis 2 — metadata category** (every field is tagged one of):
- `personal` (people, ORCIDs, roles, contact)
- `biological` (organism, tissue, disease, condition — ontology-bound)
- `technical` (instrument, library, chemistry, pipeline — mostly auto)
- `clinical` (diagnosis, phenotype — FHIR/SNOMED/LOINC, controlled-access)

## Each schema file carries, per field

```yaml
field:
  name: organism
  category: biological          # axis 2
  source: human                 # auto | project | human
  ontology: NCBITaxon           # the controlled vocabulary
  ontology_api: https://www.ebi.ac.uk/ols4/api/select   # live dropdown source
  requirement: mandatory        # mandatory | recommended | optional
  export_map:                   # how this field maps to each repository's format
    arrayexpress: "Characteristics[organism]"
    ena: "tax_id"
    biosamples: "organism"
```

The `export_map` is what makes one schema serve many repositories.

## Export targets — the FAIR domain repositories

| Repository | Domain | Standard | Your projects |
|---|---|---|---|
| **ArrayExpress** (+brokers to ENA) | expression / seq | MAGE-TAB | A03, A04, A06, PANC |
| **ENA** | raw reads | ENA checklist | (via ArrayExpress) |
| **GEO** | expression (US) | GEO SOFT | alt to ArrayExpress |
| **EGA** (European Genome-phenome Archive) | controlled human genomic | EGA schema | clinical (A06 CLINICAL) |
| **BioImage Archive** | imaging | REMBI | Z02 cycleHCR |
| **IDR** (Image Data Resource) | curated imaging | REMBI+ | high-value imaging |
| **PRIDE** | proteomics MS | SDRF-Proteomics | proteomics, phospho |
| **MetaboLights** | metabolomics | ISA-Tab | (if metabolomics) |
| **BioStudies** | multi-omics umbrella | BioStudies | integrative studies |
| **Zenodo** | code + any data | DataCite | every project's code DOI |
| **dbGaP** | US controlled human | — | (US collaborations) |
| **FlowRepository** | flow cytometry | MIFlowCyt | flow-video |
| **PDB / PRIDE-affiliated** | structures | — | (if structural) |

*You asked "what other databases?" — the additions worth knowing beyond your list:
**GEO** (US alternative to ArrayExpress), **MetaboLights** (metabolomics), **BioStudies**
(the umbrella that links multi-omics studies + holds anything without a specialised home),
**FlowRepository** (flow), **dbGaP** (US controlled-access, if you collaborate stateside).*

## The app connects it all (the endpoint)

The HTML collection app, per project:
1. loads the right **schema** (by assay) from this database
2. renders **category-grouped** forms (personal/biological/technical/clinical)
3. **autofills** technical/auto fields from source (machine, pipeline, ELN)
4. **controlled-vocabulary dropdowns** hit the ontology API live (OLS4, etc.)
5. links **ELN entry**, **data location**, **script repo** (GitHub/Zenodo)
6. shows **open-field count** → export the fill-in HTML for collaborators
7. **exports** to any target via `export_map` — ArrayExpress SDRF, EGA, REMBI, PRIDE…
8. **exports the whole thing as an RO-Crate** — the packaged research object

## The honest roadmap (this is a build, not a bundle edit)

| Phase | What | State |
|---|---|---|
| 1 | scRNA-seq schema from E-MTAB-17360 | ✅ done (gold template) |
| 2 | triple-RNAseq schema (A03) | 🔨 in the A03 chat now |
| 3 | one schema per active project, each from a real submission | ⏳ grows per project |
| 4 | `export_map` for ArrayExpress + ENA (the pair you've done) | ⏳ derive from E-MTAB-17360 |
| 5 | app loads schema-by-assay + category grouping | 🏗️ app exists; wire to schema DB |
| 6 | ontology-API dropdowns (OLS4) | 🏗️ partially in app |
| 7 | multi-repository export_map (EGA, REMBI, PRIDE) | 🏗️ one target at a time |
| 8 | RO-Crate export from the app | 🏗️ profile ready (for-AI/), wire to app |
| 9 | the growing DB connects to git — schemas versioned, app pulls them | 🏗️ needs the git connection below |

**Method for every schema (unchanged):** derive from a real accepted submission → tag
category + source + ontology + export_map → commit to this database → the app loads it.
Never hand-write a schema from imagination.
