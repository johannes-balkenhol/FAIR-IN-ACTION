# SOP — build a per-assay schema and generate the tailored capture app

*This is the method every project chat follows to (1) build the metadata schema for its
assay, and (2) generate the project-tailored HTML capture app that autofills what it can
and hands a collaborator the open fields. The bundle carries this METHOD; each project
chat does the INSTANCE.*

**Where this runs:** in the individual project chat (it needs the project's own files).
**What it produces, per project:** a validated `<assay>_schema` + a filled + a
`metadata_app_<project>.html` with the open fields highlighted, ready to email.

---

## The principle — never write a schema from imagination

A schema is derived from a **real accepted submission**, so it is correct by construction.
For expression data the anchor is **E-MTAB-17360** (a completed, curator-accepted
scRNA-seq ArrayExpress submission). Every RNA-seq schema is that template, adjusted for
the assay's organism count and library type.

```
E-MTAB-17360 (accepted scRNA-seq)  ← the gold template, correct by construction
        │
        ├── strip single-cell barcode Comments  → bulk RNA-seq schema
        ├── + host + pathogen organism rows      → dual RNA-seq schema
        ├── + a third organism row               → triple RNA-seq schema
        └── swap platform + library strategy      → PacBio / chromosome-seq schema
```

---

## Step 1 — establish the assay and organisms

From the project's `data/refs/`, `config.yaml`, and `.sdrf.tsv`, determine:
- **assay:** bulk | dual | triple RNA-seq | scRNA-seq | PacBio
- **organisms with roles:** e.g. A03 = mouse (host, GRCm39) + bacteria E10 (bacterium) +
  phage SepSi_11_M (phage) → **triple**
- **the design factors:** e.g. A03 = GF/SPF × bacteria/phage

## Step 2 — build the schema from the template

Take the gold template's field set (13 biological `Characteristics[...]`, the technical
`Comment[...]`, the 10 named protocols, EFO bindings) and adjust:

**For bulk/dual/triple RNA-seq (vs the scRNA-seq template):**
- **remove** single-cell-only Comments: `cell barcode read/offset/size`,
  `umi barcode …`, `sample barcode …`, `cdna read …`, `single cell isolation`,
  `cell multiplexing label`
- **keep** the core: organism, organism part, disease, developmental stage, strain,
  sex, age, growth condition, the library params (`LIBRARY_STRATEGY=RNA-Seq`,
  `LIBRARY_SELECTION`, `LIBRARY_LAYOUT`, `LIBRARY_SOURCE`)
- **add** one `Characteristics[organism]` handling per organism, each with its
  `Term Source REF = NCBITaxon` and role recorded

**For multi-organism (dual/triple) specifically — the fields that don't exist in the
single-organism template and MUST be added:**
- `Characteristics[organism]` becomes multi-valued or per-compartment (host + each pathogen)
- a `Comment[combined reference]` = the exact concatenated build (A03: GRCm39 + E10 + phage)
- a `Comment[read partitioning]` = competitive | sequential | in-silico (how host and
  pathogen reads were separated — the core methodological choice, almost never reported)
- confirm `Comment[LIBRARY_SELECTION]` = rRNA depletion (NOT polyA) for any bacterial
  component — bacteria have no polyA tails; polyA selection loses the pathogen
- per-organism count outputs recorded (A03 has `mouse_counts.tsv`, `E10_counts.tsv`,
  `phage_counts.tsv` — that separation is the evidence the partitioning worked)

## Step 3 — source-tag every field (auto / project / human)

Mark each field so the app knows who fills it:
- **auto** — from the data/pipeline: instrument, read lengths, MD5, file names,
  per-organism read fractions, aligner/counter from logs
- **project** — from the DMP, once: organisms+roles, licence, people, protocols,
  combined reference build
- **human** — only a person knows: the condition per sample (GF/SPF × bacteria/phage),
  organism part, the biological factor values

## Step 4 — prefill (autofill as much as possible)

Run the existing generators (on HPC: `make_ae_metadata.py`, `make_metadata.py`) plus the
pipeline logs to fill every `auto` field, and inherit `project` fields from the DMP. What
remains is only the `human` list — keep it as short as the data allows.

## Step 5 — generate the tailored capture app

Load the built + prefilled schema into the capture app
(`app/metadata_app.html`, in the FAIR-IN-ACTION repo). The app then:
- renders the form for **this project's** schema
- shows the prefilled `auto`/`project` fields as locked (editable if wrong)
- renders the `human` fields as inputs, with **ontology dropdowns** (OLS4 / domain
  ontology DB) for controlled-vocabulary fields
- **counts and highlights the open (unfilled human) fields**
- exports: the filled SDRF/IDF, and a **gap sheet** of what's still open

Save it as `metadata_app_<project>.html`. Because it's one self-contained HTML file with
the schema baked in, you **email it to the collaborator** (e.g. Mercedes Gomez's team);
they fill the highlighted open fields in a browser, no install, and send it back. Their
answers merge into the SDRF.

## Step 6 — validate and record

- every ontology field resolves to a real CURIE (no free text)
- every organism has a role
- the multiplexing/library≠sample relationship is correct
- write the result to `documents/planing/FAIR_ACTION_PLAN.md` and the filled
  metadata to `data/meta_data/`

---

## Why the app is generated, not bundled

The app is **step 3 of the maturity path** — it enforces the schema. But it is generated
*from* the schema, which is generated *from* a real submission. So the bundle carries the
method (this SOP) and the gold template (E-MTAB-17360's shape); each project chat
generates its own schema and its own tailored app. Bundling a frozen app would drift from
the schema; generating it per project keeps them in lockstep.

**One source (the real submission) → the schema → the app → the collaborator's fill-in
HTML.** That chain, run per project, is the whole metadata-capture system.
