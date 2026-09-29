# The DMP decision-tree — the project's front door

*The missing keystone. At project start, a short decision tree (which IS the machine-
readable core of the DMP) determines everything downstream: the schema template, the
folder structure, the naming convention, the ontologies, and the export targets. Answer it
once → the project is configured. This is the MetaFold-like "one step" made FAIR.*

## Why this is the center

Everything the bundle does hangs off a few early decisions. Instead of asking them
scattered across the process, ask them **once, up front**, as a tree — and let the answers
generate the setup. The tree is the DMP's decision layer; filling it *is* writing the DMP.

## The tree (the questions, in order)

```
1. DATA TYPE?  ────────────────────────────────────────────────
   ├─ sequencing ─→ 1a. which?
   │      ├─ bulk RNA-seq            → schema: rnaseq-bulk        → ArrayExpress+ENA
   │      ├─ dual/triple RNA-seq     → schema: rnaseq-dual/triple → ArrayExpress+ENA
   │      ├─ single-cell (10x)       → schema: scrnaseq-10x       → ArrayExpress+ENA
   │      ├─ PacBio / Nanopore       → schema: pacbio/nanopore    → ENA
   │      └─ (host+pathogen?) ─→ add organism rows, read-partitioning field
   ├─ proteomics ─→ MS / phospho     → schema: proteomics-ms/phospho → PRIDE
   ├─ flow ───────→ cytometry/video  → schema: flow-*            → FlowRepository/BioImage
   ├─ imaging ────→ fluorescence     → schema: imaging-fluorescence → BioImage Archive/IDR
   │      └─ (multi-channel? lightsheet?) → add channel/fluorophore fields (REMBI)
   └─ clinical ───→ patient data     → schema: clinical-fhir     → EGA (controlled) ⚠ GDPR

2. SENSITIVITY?  ──────────────────────────────────────────────
   ├─ open        → open repository, cloud AI OK
   ├─ pseudonymised / identifying → controlled-access (EGA), LOCAL AI only,
   │                                 clinical/ track, DPO sign-off
   └─ (sets the whole compliance path — STACK.md §4)

3. ORGANISMS?  ── list each with role (host/bacterium/phage/fungus/…) → schema organism rows

4. TARGET REPOSITORY?  ── confirmed here → sets the minimum metadata set → the schema
   (ArrayExpress / ENA / PRIDE / BioImage Archive / IDR / EGA / FlowRepository / Zenodo)

5. EXPORT FORMATS NEEDED?  ── SDRF/IDF · REMBI · FHIR · SQL · JSON · XML · Excel · RO-Crate
   (multi-select → the app's export_map is filtered to these)

6. STRUCTURE & NAMING?  ── use the standard skeleton + YYYYMMDD_sampleID_type_v01
   (or import an existing structure to map onto)
```

## What the answers generate

| Answer | Generates |
|---|---|
| data type | the **schema template** loaded into the app (from `schemas/<assay>/`) |
| sensitivity | the **compliance path** (open→cloud / sensitive→local+EGA+DPO) |
| organisms | the **organism rows** + multi-organism fields |
| repository | the **minimum metadata set** + the primary `export_map` |
| export formats | the **app's export menu** (filtered) |
| structure/naming | the **folder scaffold** + naming rule (init_project) |

**Output:** a filled `DMP.md` (human) + a `project.yaml` (machine, drives the app) +
the tailored `metadata_app_<project>.html`. One tree, the whole project configured.

## Not only at the start

The tree is *usually* run at project start, but can be re-run or partially applied to an
existing project (the intake in STACK.md §0a feeds it: read what exists → pre-fill the
tree → only ask what's undetermined).

## Build status

🏗️ **Spec, not built.** This is the app's next major feature. The tree logic → template
selection is the highest-value thing to build after the schemas exist, because it's what
makes the whole system "answer a few questions → FAIR project configured" instead of
"read the SOPs and do it by hand." It is the automation of the maturity path's step 1→2.

## Relation to MetaFold

MetaFold (ThZobel) proved the "template → one-step folder + metadata" pattern. This tree is
that, generalized: the template isn't fixed — it's *selected by the decision tree* from the
schema database, and the export targets are chosen too. MetaFold picks a template; this
tree *generates* the right one from your answers.
