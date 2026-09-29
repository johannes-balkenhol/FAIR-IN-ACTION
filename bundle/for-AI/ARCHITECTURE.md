# The FAIR-in-action architecture — the whole picture

*The capstone. Everything the bundle is aiming at, as one map: the four connected systems,
the layers between raw measurement and a consortium knowledge graph, and what is real
today vs. what is the target. Grounded in the group's actual infrastructure.*

---

## The one sentence

**Every project, from a bachelor student's to a PI's, starts from one zip; the setup is
FAIR- and GDPR-compliant by construction, as much is automated as possible, and once a
project is set up this way it connects — to the ELN, the cloud, the HPC, GitHub, and to
every other project — so that a lab or a whole consortium becomes a queryable knowledge
graph of linked data, results, and provenance.**

That last clause is the north star. Everything below serves it.

## The four systems (real infrastructure)

| System | Where | Role |
|---|---|---|
| **ELN** — eLabFTW | elabftw.rz.uni-wuerzburg.de | metadata capture at the bench; templates; `.eln` export; API |
| **Cloud** — Nextcloud | coreunitrdm.biozentrum.uni-wuerzburg.de | data storage, sharing, the human-facing files |
| **HPC / JupyterHub** | 132.187.22.206:8000 | where pipelines run; scripts, analysis |
| **Code** — GitHub | github.com/CoreUnitRDM + FAIR-IN-ACTION | schema, apps, code, workflows — the source of truth for anything that is code |

**The separation rule (already written up in `RDM/RDM_SOPs+guidelines/Nextcloud+git/`):**
data lives in Nextcloud, code lives in Git, and they are *connected* — not merged —
through the README and through `.gitignore` (Nextcloud paths git-ignored; large data
never committed). This is the boundary that keeps the whole thing sane.

## The layered stack — raw measurement → knowledge graph

```
  ┌─ measurement ─────────────────────────────────────────────┐
  │  instrument / microscope / sequencer  →  raw data + technical metadata (auto)
  └───────────────────────────────────────────────────────────┘
                    │
  ┌─ capture ──────────────────────────────────────────────────┐
  │  eLabFTW templates (biological/human metadata) ── API ──┐   │
  │  metadata collection app  ◄── pulls from ELN & gadgets ─┘   │
  │       │  fills the SCHEMA; controlled vocab as dropdowns     │
  │       │  (ontology terms resolved against OLS)               │
  │       └── can also PUSH metadata back to the ELN entry       │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ schema (the one source) ──────────────────────────────────┐
  │  LinkML metadata schema, per use case, derived along the DMP │
  │  three requirement levels: mandatory / recommended / optional│
  │  → generates: JSON Schema · app forms · SQL · templates      │
  │  → the DMP defines the minimum set + project extras          │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ structure (the project) ──────────────────────────────────┐
  │  init from the bundle → fixed folder skeleton:               │
  │  data/{raw,primary,secondary,meta} · documents/{plan,report} │
  │  scripts/ (numbered to plan) · analysis/ (mirrors pipeline)  │
  │  code/ (notebooks, python, r, app, CWL) · results/ · var/    │
  │  README (fixed UKW/FHIR-style format) · DMP (fixed) · LICENSE │
  │  DATAFINDER = the metadata, searchable                       │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ automation ───────────────────────────────────────────────┐
  │  scripts → CWL / Snakemake / Nextflow workflows              │
  │  standardised rsync  Nextcloud ⇄ HPC                         │
  │  standardised commits  → GitHub                              │
  │  ELN .eln export → SOP (protocols.io-style)                  │
  │  once metadata + vocab are right, the PIPELINE JUST RUNS     │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ gates (FAIR + GDPR control) ──────────────────────────────┐
  │  G1 before SHARE: FAIR self-check + GDPR/sensitive-data check │
  │  G2 before PUBLISH: repository + DOI + licence               │
  │  checklists → can become automated controls                  │
  │  sensitive data: SECURE_PROCESSING_no_TRE until a TRE exists  │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ packaging ────────────────────────────────────────────────┐
  │  the whole project → an RO-Crate (the aim)                   │
  │  human- AND machine-readable; deposited with a DOI/accession │
  └────────────────────────────────────────────────────────────┘
                    │
  ┌─ connection (the north star) ──────────────────────────────┐
  │  many RO-Crates, one shared schema, cross-linked IDs         │
  │  → per-lab / per-consortium KNOWLEDGE GRAPH                  │
  │  → feedable to OMERO, ArrayExpress, CellWhisperer, atlases   │
  │  → an explorable data + results + analysis atlas             │
  └────────────────────────────────────────────────────────────┘
```

## The DMP is the spine

Not a form filed and forgotten. The **DMP is written first, along the RDM lifecycle, and
it defines**: which repository you will publish to → which metadata that repository
demands → therefore the *minimum* metadata set → plus the extra metadata this project
collects. The schema for the project is the machine-readable form of the DMP's metadata
section. **DMP → schema → app → RO-Crate → repository** is one chain, decided at the start.

## What each role does (from the VRC roles/responsibilities work)

| Role | Fills | Owns |
|---|---|---|
| **Experimenter** | biological/human metadata (ELN templates, gap sheet) | the sample-level truth |
| **Analyst** | technical/analysis metadata, the pipeline | scripts/, analysis/, code/ |
| **Data steward** | the schema, the DMP, the deposition | the FAIR/GDPR gates |
| **PI** | signs off; consumes the knowledge graph | the project's existence |

SOPs connect roles → workflows. An eLabFTW entry can *become* an SOP; a script can become
a CWL/Snakemake workflow; both get a **fixed chosen format** (as the README has the
UKW/FHIR-style fixed format) so they are human- and machine-readable.

## The payoff — why anyone does this (the "quick gains")

Once a use case is set up FAIR + GDPR-compliant with the right metadata and controlled
vocabulary, these stop being weeks of work and become hours:

- deploy data with the right structure → **the pipeline just runs**, results rsync back,
  the report is drafted (by an AI) — **hours, not weeks**
- a PI has a live **knowledge graph** of the lab / consortium
- a new PhD understands a predecessor's project **in hours, not months**
- a thesis / publication outline / grant is writable fast, because everything is in place
- a consortium builds a shared **data + results + analysis atlas** in days
- a single-cell centre stands up a FAIR/GDPR database with the same leverage

**That list is the business case.** It is why the up-front discipline pays — and it is the
argument to put to a PI who asks "why bother".

## Real assets to build from (not from scratch)

The group already has, on disk and in Git:

| Asset | Where |
|---|---|
| naming convention | `RDM/folderstructure-naming/` |
| Nextcloud+Git separation SOP | `RDM/RDM_SOPs+guidelines/Nextcloud+git/` |
| metadata templates (NFDI/ArrayExpress/LabFolder) | `RDM/Metadata-templates/DECIDE_MetaDataTemplates/` |
| RO-Crate notes | `RDM/RDM_resources/ResearchObjectCrate/` |
| ELN test reports & template examples | `RDM/RDM_resources/eLabFTW/`, `Labfolder/` |
| metadata generator scaffold | `Scripts/Metadatgenerator/`, `CoreUnitRDM/MetaDataGeneratorNC` |
| MetaDataTemplates generator | `CoreUnitRDM/MetaDataTemplates` |
| 20+ use-case metadata registries | `UseCases/USECASE_Metadata_*.xlsx` |
| clinical secure-pipeline use case | `UseCases/26-09_ALM-diagnosis-secure-pipeline` |
| MetaFold (reference to study) | github.com/ThZobel/MetaFold |

Consolidating these *is* the work — the architecture above is mostly assembly, not
invention.

## Status — honest

| Layer | State |
|---|---|
| structure, naming, handout, gates | **real, in use** |
| schema (LinkML, FlowSep) | **real prototype** |
| metadata apps (NC + JS) | **two prototypes, to reconcile onto one schema** |
| RO-Crate profile | **profile ready; ro-crate-py packaging future** |
| ELN ⇄ app ⇄ schema round-trip | **designed, not built** |
| CWL/Snakemake/Nextflow automation | **designed; scripts exist, not yet workflow-ified** |
| knowledge graph / atlas | **north star; follows once many RO-Crates share the schema** |

The bundle's job is to make the *top* of this real for every new project today, while the
lower layers are professionalised step by step.

---

*The whole point in one line: **set a project up right once, and everything downstream —
analysis, reports, theses, grants, the consortium atlas — gets cheaper, because it was
FAIR from the start.***
