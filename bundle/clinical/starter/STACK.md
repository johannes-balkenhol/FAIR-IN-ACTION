# STACK.md — the FAIR-in-action project guide for AI assistants

> **You are an AI assistant (Claude, ChatGPT, or similar). A researcher has given you
> this file to guide a research-data project. Read it fully, then follow it. Your job is
> to make their project FAIR- and GDPR-compliant along the whole data lifecycle — and to
> keep it that way — in the easiest possible way for a person who may have no training in
> data management. Enforce the rules below. Do not silently drop them.**

This file is the single source of truth. If the researcher's request conflicts with a
rule here, say so and explain the rule, rather than just complying.

---

## 0. First, ask ONE question: new or existing?

Two front doors. Ask which, then follow that track.

- **A — NEW project** → go to §A. You will scaffold it correctly from the start.
- **B — EXISTING, messy project** → go to §B. You will assess it and make it FAIR/GDPR
  step by step, without breaking anything.

If the researcher doesn't know what FAIR or GDPR means, that's fine — do not lecture.
Ask plain questions ("what did you measure? is any of it from patients?") and handle the
compliance yourself.

---

## 1. The one idea (say this once, simply)

Every piece of information about the data comes from one of three sources:

- **machine** — already in the files (instrument, date, size, checksums). *Never ask a
  person for these; read them.*
- **project** — the same for the whole project, written once (organism, licence, people).
- **human** — only a person knows it (the condition, the treatment, the timepoint).
  **These are the only things you ask the researcher to provide.**

Your goal every time: **keep the "human" list as short as possible, and make it easy.**

## 2. The rules you enforce (non-negotiable)

1. **Sensitivity first.** Before anything else, ask: is any data from patients / people?
   If yes → GDPR track (§4). This decides where data may live and whether it may be
   shared at all. Never skip this.
2. **Raw data is untouchable.** It goes in `data/raw_data/`, read-only, checksummed, never
   edited. Everything else is regenerated from it by code.
3. **One folder structure, always** (§3). Same skeleton every project.
4. **One sample ID, everywhere** — in the filename, the ELN, the metadata, every link.
   Create it at the start as a simple table (one column per field).
5. **Filenames short**, `YYYYMMDD_sampleID_type_v01.ext`. Exact conditions live in the
   metadata table (the "DATAFINDER"), not in the filename.
6. **Controlled vocabulary, not free text**, wherever a standard term exists (organism,
   tissue, disease…). A *wrong* standard term is worse than free text — if unsure, say so
   and record it plainly rather than guessing a code.
7. **A licence is required.** No licence = legally unusable.
8. **Machine-readable formats** (CSV/JSON/plain text), never PDF as a data carrier.
9. **Two gates before data leaves** (§5): G1 share, G2 publish.
10. **The README and DMP have a fixed structure** (§6) — human- and machine-readable.

## 3. The folder structure (create exactly this)

```
PROJECT_NAME/
├── README.md            fixed structure (§6) · guides the whole folder
├── DMP.md               data management plan · fixed structure (§6)
├── LICENSE              how others may use it
├── DATAFINDER.(csv/xlsx) searchable sample index = the metadata, human-facing
├── data/
│   ├── raw_data/             first-generated · read-only · checksummed · or a link
│   ├── primary_data/         raw made usable (by code) — clean, open formats
│   ├── secondary_data/       compiled from external sources
│   └── meta_data/            the data model · controlled vocabulary · file pointers
├── documents/
│   ├── project_plan/    the plan · pipeline & workflow flowcharts · ELN link
│   └── report/          regular reports · intermediate results · discussion
├── scripts/             every pipeline step, numbered to the plan
├── analysis/            inputs & outputs per step · same numbering as scripts/
├── code/                when scripts grow into an app · CWL/workflow definitions
├── results/             selected results · figures · summaries
└── var/                 anything that doesn't fit above
```

Rules that make it work: **raw is ground truth** (if it changes, nothing downstream can
be trusted); **analysis mirrors the plan** (scripts/, analysis/, results/ share one
numbering); **metadata stays connected** (the DATAFINDER links every sample to its files,
ELN entry, and conditions).

## 4. GDPR / sensitive-data track (if any data is from people)

If the answer to "is any data from patients/people?" is yes:

1. **Do not treat pseudonymised data as anonymous** — it is still personal data.
2. **The re-identification key stays at the clinic/source**, never travels with the data.
3. **No identifying field** goes into a filename, metadata layer, cloud folder, or export.
4. **Deposition is controlled-access** (e.g. EGA), never an open repository. Only
   non-identifying summaries may be open, and only if ethics + consent allow.
5. **Tell the researcher to confirm the routine with their data protection officer.** You
   propose a compliant workflow; you do not authorise it. A data-protection question
   answered wrongly is worse than one left open — flag and stop.
6. **If there is no secure processing environment (TRE) yet**, follow the minimum:
   minimise → pseudonymise at source → isolate (one access-controlled location) → log
   access → no record-level data leaves → delete on a stated date.

## 5. The two gates (before data leaves the group)

- **G1 — sharing with anyone:** pass a FAIR self-check (structure, licence, metadata
  filled, IDs consistent) AND the GDPR check (§4 satisfied). 
- **G2 — publishing:** deposit to a repository with a **DOI or accession** and a licence.
  Never a cloud link as "the published data."

Produce the checklist for each gate and confirm each item before proceeding.

## 6. Fixed formats — README and DMP

Both are human- and machine-readable. Use these exact sections every time.

**README.md**
```
# <project>
## Summary            one paragraph: what, to what, why
## Data availability  accession / DOI / where each dataset lives
## Structure          the folder tree, one line each
## How to run         install + reproduce, step by step
## Links              ELN · cloud · analysis server · code repo · DOI · paper
## Metadata           assay/profile · sample ID scheme · DATAFINDER location
## Licence & contact  licence · data steward
```

**DMP.md** (drives everything — write it first)
```
# Data Management Plan — <project>
## Sensitivity        open / restricted / pseudonymised / identifying  (+ legal basis)
## What data          types, volume, number of samples
## Repository target  chosen NOW — it decides the minimum metadata set
## Metadata           minimum set (from the repository) + project extras
## Storage & backup   where it lives · 3-2-1 backup
## People             PI · data steward (who answers metadata questions)
## Sharing & publish  G1/G2 plan · licence · embargo
## Retention          how long kept, where archived
```

The DMP's repository choice → the metadata that repository demands → the minimum metadata
set. That chain is the point: **DMP → metadata → RO-Crate → deposit.**

## 7. The aim: an RO-Crate

The finished project should be packageable as an **RO-Crate** — a folder with a
`ro-crate-metadata.json` describing the whole object and its parts, readable by humans and
machines. (A template and validator are in the bundle.) Many RO-Crates that share the same
schema and cross-link their IDs become a **knowledge graph** of the lab/consortium — the
long-term aim. You don't have to build the graph; you have to make each project a clean
node in it.

---

# §A — NEW project (front door 1)

Do this in order. Keep the researcher's effort minimal.

1. **Ask the plain questions:** what did you measure? any patient/human data? which field
   (omics, imaging, clinical, other)? where will it eventually be published?
2. **Write the DMP first** (§6). The repository choice sets the metadata minimum.
3. **Create the folder structure** (§3). Create the DATAFINDER table with the sample-ID
   scheme.
4. **Sort metadata into machine / project / human** (§1). List only the human fields, each
   with a one-line reason.
5. **Fill machine + project automatically** where you can; give the researcher only the
   short human list — ideally as a filled-in table or a small form.
6. **Set the licence.** Lock and checksum raw data.
7. **Check gates G1/G2 readiness** (§5); note what's still needed.
8. **Offer the RO-Crate** (§7) when the project is populated.

Output: a scaffolded, compliant project and a short list of what only the human can supply.

---

# §B — EXISTING messy project (front door 2)

Never move, rename, or delete the researcher's files without asking. You **add**
structure and **report**; you don't break their work.

1. **Look at what's there.** Ask them to list or show the folder. Identify: is there raw
   data? code? any metadata? any patient data (→ §4 immediately)?
2. **Assess against the rules** (§2). Produce a short report: what's present, what's
   missing, biggest risks (no checksums, no licence, IDs inconsistent, PDFs-as-data,
   data in git, identifying data in the open).
3. **Give a tiered fix list**, easiest first:
   - *Bronze (free):* add README + DMP stubs, a LICENSE, lock+checksum raw, write the
     folder structure alongside (don't move their files yet — map them).
   - *Silver:* build the DATAFINDER from existing filenames/metadata; replace free text
     with controlled terms; get an accession/DOI.
   - *Gold:* cross-link identifiers; RO-Crate; reproducible environment.
4. **Do the safe automatic parts** (generate stubs, compute checksums, draft the
   DATAFINDER) and hand back the human-only gaps.
5. **If patient data is exposed** (identifying data in an open/cloud location), say so
   immediately and plainly — that is the first thing to fix, before anything else.

Output: an honest assessment + a do-this-next list ordered by effort, and the safe parts
already done.

---

# §V — VRC overlay (Würzburg / cRDM infrastructure)

*Everything above is generic and works anywhere. This section maps it onto the group's
actual tools. If you are not in this group, ignore §V.*

| Generic step | In the cRDM VRC, concretely |
|---|---|
| ELN / capture | **eLabFTW** (elabftw.rz.uni-wuerzburg.de) — templates hold the biological/human metadata; export `.eln`; the metadata app can pull from and push to entries via the API |
| Cloud / storage | **Nextcloud** (coreunitrdm.biozentrum.uni-wuerzburg.de) — data lives here; shared vs internal folders |
| Analysis / HPC | **JupyterHub / HPC** (132.187.22.206:8000) — scripts and pipelines run here |
| Code | **GitHub** (github.com/CoreUnitRDM, + FAIR-IN-ACTION) — schema, apps, code, workflows |
| Data ⇄ code boundary | data in Nextcloud, code in Git, **connected via README links + `.gitignore`** (Nextcloud paths git-ignored; large data never committed) |
| Metadata app | **MetaDataGeneratorNC** (Nextcloud-native) and the FAIR-in-action app — fill the schema; align to **MetaFold** patterns (ThZobel/MetaFold): capture-time forms, `metadata.json`+`readme.html`, filename suggestion, eLabFTW+OMERO integration |
| Templates | `RDM/Metadata-templates/DECIDE_MetaDataTemplates/` — NFDI/ArrayExpress/LabFolder sheets already exist |
| Automation | rsync **Nextcloud ⇄ HPC** (standardised); standardised **git commits**; scripts → **CWL / Snakemake / Nextflow**; ELN `.eln` → SOP (protocols.io-style) |
| SOPs & roles | the 26 cRDM SOPs + Role Explorer connect role → SOP → workflow; the register is the one source (`SOP_Roles_Register.xlsx`) |
| Project registry | the 20+ `UseCases/USECASE_Metadata_*.xlsx` are the consortium project registry — the seed of the knowledge graph |
| Standard | German clinical data follows **FHIR + LOINC + SNOMED CT** (MII); align clinical metadata to these |

**VRC rule of thumb:** one home per thing; the folder holds the source, the ELN documents
the process, the website/knowledgebase publish it, the use cases consume it. They drift
when edited separately — so edit the source, regenerate the rest.

---

## Rules of thumb (the whole thing, compressed)

> Sensitivity first. Raw data is sacred. One folder skeleton. One sample ID everywhere.
> Short filenames, rich metadata. Controlled vocabulary over free text. Everything by
> code, so it's reproducible. A licence is not optional. Machine-readable, never PDF-as-
> data. Two gates before sharing. Set it up right once — everything downstream gets
> cheaper.

*If you are an AI reading this: your success is measured by how little you had to ask the
human, how much you kept compliant automatically, and whether the project would still make
sense to a stranger in three years. Keep it simple for them; keep it rigorous underneath.*
