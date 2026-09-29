# The FAIR-in-action bundle — what it is and what feeds it

*This describes the whole bundle we hand to a scientist (human-readable) and to an AI
stack (machine-readable), so every project and every chat is guided the same way. It is
assembled from work done across several project chats — noted below so nothing is
reinvented. All GitHub repositories are now resolved (see the table near the end).*

---

## The one sentence

Everything a scientist or an AI needs to take a project from first measurement to a
deposited, citable **FAIR research data object** — the rules, the definitions, the
metadata schema, the app that fills it, and the RO-Crate that packages it — in one bundle,
readable by people and by machines.

## The bundle, by layer

| Layer | Artifact | Human / Machine | Status |
|---|---|---|---|
| **Principle** | FAIR charter · RDM handout (AG Heinze v0.3) | human | in use |
| **Definition** | FAIR-data-object folder (measurement guidance, object definition, RO-Crate profile) | both | v0.1 |
| **Schema** | metadata schema + MetaDataTemplates | machine | on GitHub (CoreUnitRDM) |
| **Capture** | MetaDataGeneratorNC (Nextcloud) · FAIR-in-action app | both | on GitHub |
| **Packaging** | RO-Crate (`ro-crate-metadata.json`, ro-crate-py) | machine | profile ready; tooling future |
| **Secure handling** | secure-processing-without-a-TRE guideline | human | in use |
| **Deposition** | Zenodo / ArrayExpress / BioImage Archive / EGA + DOI | — | per project |

## What each piece is (and where it came from)

### The metadata schema — LinkML, in Git
A GROWING DATABASE of per-assay schemas, built step by step — one worked example at a time. Each project has its own metadata needs: ArrayExpress/sequencing (rich nested SDRF/IDF, the best current guide), single-cell, triple RNA-seq, imaging (REMBI), hospital (FHIR) each differ. The source of truth for fields, types, requirement levels and controlled vocabulary, per assay. Built
in the **FlowSep** work: a LinkML schema (YAML in Git) that **generates JSON Schema,
Pydantic and SQL DDL from one source**, with a three-level requirement model
(mandatory / recommended / optional) and **terms resolved against OLS at build time — zero
unresolved terms**. This is the "one schema, many renderings" engine the whole bundle
turns on.

- Repositories:
  - **FAIR-in-action toolkit** — https://github.com/johannes-balkenhol/FAIR-IN-ACTION
  - **MetaDataTemplates** (metadata sheets, multiple formats) — https://github.com/CoreUnitRDM/MetaDataTemplates
  - **CoreUnitRDM org** (all group RDM code) — https://github.com/CoreUnitRDM
- Design proven in: the FlowSep imaging-metadata project; the conference poster
  ("controlled vocabulary and value constraints defined in LinkML").

### The metadata generator app
Fills the schema's fields at the point of data creation — the human-facing capture tool.

- Our apps: **MetaDataGeneratorNC** — https://github.com/CoreUnitRDM/MetaDataGeneratorNC
  (PHP, Nextcloud-native, AGPL-3.0) — and the FAIR-in-action app (HTML/JS, schema-driven).

The conference (poster confirmed, Sep 2026) showed **MetaFold** — Dr. Thomas Zobel,
Münster Imaging Network — as the closest and further-along sibling. A **template-driven
desktop tool** whose pitch matches ours exactly: make RDM "as intuitive as creating a new
local folder", capturing rich metadata at the point of data creation. What it already has,
and we should align with rather than rebuild:

- template-based creation of **project folders AND metadata forms together**
- a **category system** — customizable templates per project type
- **predefined, prefilled, reusable** metadata entries (consistent across a group)
- **multi-user / group-level** configuration
- **direct integrations with eLabFTW (ELN) and OMERO**
- **project discovery** — recursive scan + visualization of existing data (retrofit, like our `fairify.py`)
- **filename suggestion** — the opaque-ID / short-name problem Katharina raised
- outputs a local **`metadata.json` + `readme.html`** per project

MetaFold is on GitHub (Münster Imaging Network; NFDI4BIOIMAGE / Cells in Motion context).
Imaging-focused, but every feature above is domain-general. **Strategic question for our
bundle:** adopt/extend MetaFold, or keep our own generator and match its feature set?
Either way it is the reference implementation to measure ours against.

### The FAIR-data-object definition + RO-Crate profile
The `FAIR-data-object/` folder: what a scientist captures (measurement guidance), what
counts as a finished object (definition), and the **RO-Crate 1.1** machine form that packages
it. Grounded in the RO-Crate spec; validated. This is the piece that makes the object
readable by an AI stack identically to a human.

### Secure handling
`SECURE_PROCESSING_no_TRE.md` — the defensible minimum for sensitive data before a TRE/SPE
exists. From the clinical / UKW → Uni Würzburg work.

### Deposition
Repository per data type (ArrayExpress/BioImage Archive/EGA/Zenodo), DOI or accession,
cross-linked. The **PANC ArrayExpress** pipeline is the worked example of the
machine-extractable-vs-human-supplied split.

## How the renderings stay in sync

```
        metadata schema (LinkML, Git)  ── the one source
                     │  generates
     ┌───────────────┼───────────────────┐
     ▼               ▼                    ▼
 JSON Schema     app form fields     RO-Crate profile
 (validation)    (human capture)     (machine package)
     └───────────────┴───────────────────┘
                     ▼
        one FAIR research data object
        → deposited with a DOI / accession
```

The RDM handout is the human face; the RO-Crate profile is the machine face; the schema
generates both. Today some of these are hand-kept in sync; the goal is to **generate the
handout tables and the RO-Crate profile from the schema**, so there is genuinely one
source.

## Contributions pulled from project chats

| From | What it contributed |
|---|---|
| **FlowSep** | the LinkML schema, OLS-at-build-time vocabulary, the three-level requirement model, the versioned-catalogue + correction-loop pattern |
| **Conference (2026)** | **MetaFold** (Zobel, Münster): template-driven desktop capture · eLabFTW+OMERO integration · project discovery · filename suggestion · local metadata.json+readme.html. Plus REMBI/MIxS checklist model; BacDive licence-page model |
| **Infection projects (PANC / DECIDE)** | the machine-vs-human metadata split; the ArrayExpress deposition pipeline; multi-organism / decision-node metadata needs |
| **Institute-stack design** | the end-to-end tool chain, with RO-Crate chosen as the packaging layer |
| **VRC / SOP work** | the tiered sharing/publishing gates; GDPR handling; FAIR self-check |

## The real repositories (resolved)

| Repo | What it is | Lang / licence |
|---|---|---|
| [johannes-balkenhol/FAIR-IN-ACTION](https://github.com/johannes-balkenhol/FAIR-IN-ACTION) | the omics toolkit (model, extractors, app, audit) | Python |
| [CoreUnitRDM/MetaDataGeneratorNC](https://github.com/CoreUnitRDM/MetaDataGeneratorNC) | **the metadata generator app** — Nextcloud-native | PHP · AGPL-3.0 |
| [CoreUnitRDM/MetaDataTemplates](https://github.com/CoreUnitRDM/MetaDataTemplates) | **generate & download metadata sheets** in several formats | Jupyter |
| [CoreUnitRDM/DECIDE_RDM_landingpage](https://github.com/CoreUnitRDM/DECIDE_RDM_landingpage) | DECIDE RDM overview page | CSS |
| [CoreUnitRDM (org)](https://github.com/CoreUnitRDM) | all group RDM code (5 repos) | — |

Two generator paths co-exist and are worth reconciling in the bundle:
**MetaDataGeneratorNC** (PHP, lives in Nextcloud, for wet-lab users) and the
**FAIR-in-action app** (HTML/JS, schema-driven, for omics). Same job, two front-ends —
a candidate for one schema feeding both.

---

*Prototype-stage bundle. The definitions, handout, RO-Crate profile and secure-processing
guideline are usable now; the schema and app are prototypes to professionalise step by
step. Open for discussion; improves with use.*
