# FAIR in Action

Prepare research data so it is reusable — from the first measurement to a citable,
Europe-ready publication. For every discipline: life sciences, medicine, social sciences,
physics, and more. For humans as much as for AI.

Most FAIR guides tell researchers *what* to do and leave them alone with it. This system does
the opposite: it **fills in what it can read from the data and the project itself**, and asks a
person only for what only that person can know. Every project set up this way ends as a clean,
citable, consortium-linkable object.

---

## The two things we hold to — FAIR *and* GDPR compliance

A dataset is only reusable when it is **F**indable, **A**ccessible, **I**nteroperable and
**R**eusable (FAIR), and — for any data about people — only lawful when it is **GDPR-compliant**.
This toolkit treats both as first-class, and it does two things with them, not one:

- it **audits** a project for FAIR and GDPR (and for the release gates), honestly scoring where it stands, and
- it **actively prepares** the project — *fairify* and *gdprify* — doing every step the data and
  the project already allow, and handing back a short list of what only a human can supply.

**The core idea in one sentence:** every metadata field is answered by the **machine** (it is in
the data), by the **project** (decided once), or by a **human** (only they know it) — and only the
last is ever asked. Keeping that human list short — using controlled vocabulary, protecting raw
data, linking everything — makes a project that was set up right cheaper in everything that
follows: analysis, reports, theses, grant applications, and a consortium knowledge graph.

## What the system does — the loop

```
AUDIT (read-only) → FAIRIFY / GDPRIFY (what the data allows) → GAP LIST (what a human must provide)
```

- **FAIR audit** (`agent/`) — reads a project folder read-only and reports its tier
  (**bronze / silver / gold**), the FAIR flags, the GDPR signals, and the release-gate readiness.
  It changes nothing.
- **fairify** — fills what can be filled from the data and the project: modality and organism from
  the files, a metadata schema from the modality profile, **controlled-vocabulary terms** instead
  of free text (via the Ontology Lookup Service), and packaging to **RO-Crate / ARC**. Creation is
  additive only — it never overwrites, moves, renames or deletes.
- **gdprify** — sets sensitivity, scopes access to named groups (never world-readable), keeps raw
  data and any identity mapping out of shared folders and version control, and makes a release a
  *recorded* decision rather than a memory.
- **gap list** — the remainder, each item tagged so a person sees exactly what only they can
  provide: ethics / legal basis, consent scope, instrument model, licence choice, a missing
  accession. **Ethics numbers, consent scopes, accessions and DOIs are never invented** — they are
  always left for a human.

## The chain — decided at the start, not the end

The central idea: the order is fixed at the **start** of a project, not patched on at the end.

```
Data Management Plan → metadata schema → capture app → packaged research object → repository
```

The repository decides which metadata are needed, which data type, which licence, which retention
period. Choose it early and most later questions answer themselves.

## The eleven steps — from the bench to a transferable procedure

The system follows the eleven steps a dataset runs through from the workbench to a controlled,
Europe-ready publication. Steps 1–8 make a dataset ready, step 9 makes the handling repeatable,
steps 10–11 take it beyond the institution.

| # | Step | What the system contributes |
|---|------|------------------------------|
| 1 | Clarify legal basis / ethics (for sensitive data) | `bundle/clinical/` — sensitivity first, data-protection sign-off |
| 2 | Set up the project — structure, naming, DMP | `bundle/STACK.md`, the handout, project init |
| 3 | Choose the metadata schema (per assay / data type) | `profiles/`, the growing schema database |
| 4 | Capture metadata — what the machine can do, automatically | the capture app (`app/metadata_app.html`) |
| 5 | Controlled vocabulary — ontology terms instead of free text | OLS4 binding in the app |
| 6 | Protect raw data — immutable, checked | principle in the handout, `extractors/` |
| 7 | Provenance — which script produced which result | `docs/METADATA_HARMONIZATION.md` |
| 8 | Package — RO-Crate / ARC (the NFDI standard) | `arc/`, `docs/SOP_make_rocrate.md` |
| 9 | Make it repeatable — SOP, then workflow, then automation | the SOPs, the `agent/` |
| 10 | Nationally findable — repository, DOI, controlled access | `docs/SCHEMA_DATABASE_DESIGN.md` (export targets) |
| 11 | Europe-ready — describable for the European catalogue | RO-Crate / ISA as a by-product of the preparation |

The point: these eleven steps are not a checklist for one dataset. They are the raw material for
**procedures other groups, consortia and sites can adopt**. A solved case becomes an SOP, the SOP
a portable workflow, the workflow an automation.

## Standards we align to — and NFDI

Everything the system produces is built to land on the community standards, so a project is usable
far beyond our own walls:

| Layer | Standard |
|-------|----------|
| Metadata model | ISA (Investigation / Study / Assay) |
| Packaging, machine-readable | RO-Crate |
| Container structure | ARC (NFDI / DataPLANT) |
| Vocabularies | NCBITaxon, UBERON, EFO, MONDO … (life sciences); per field its own |
| Repositories | ArrayExpress / ENA, PRIDE, BioImage Archive, EGA (controlled), Zenodo … |
| Health catalogue | HealthDCAT-AP / EHDS |

**NFDI** — Germany's *Nationale Forschungsdateninfrastruktur* (National Research Data Infrastructure)
— and its domain consortia develop the community guidelines and standards for research-data
management across disciplines. **This toolkit is built to align to them:** the ARC container and
the ISA / RO-Crate packaging follow **DataPLANT**; the clinical and health-data path follows the
practices of **NFDI4Health** and **GHGA** (controlled-access genomics); domain vocabularies follow
the consortium for each field. Aligning to NFDI is what keeps a project nationally findable and
ready for the European layer on top — without a rebuild.

## For whom

**🧑‍🔬 A human (student to PI)** → `bundle/START_HERE.md` → the handout (1–2 pages) → the
worksheets. The capture app asks you only for what only you know.

**🤖 An AI (Claude, ChatGPT, local)** → read and follow `bundle/STACK.md`. For sensitive data use a
local model (`bundle/clinical/LOCAL_AI_for_sensitive_data.md`) — nothing leaves the machine.

**🏛️ A consortium / funding line** → this README plus `docs/` show that the objects produced land
on RO-Crate, ISA and ARC (NFDI / DataPLANT) — Europe-ready, no rebuild.

## What is in the repository

```
bundle/      The standard: handout, STACK.md, SOPs, worksheets, clinical path
profiles/    Metadata schemas per assay (grows out of real submissions)
app/         The capture app (HTML, runs anywhere, no installation)
arc/         ISA model + ARC converter — the packaged research object (NFDI standard)
agent/       FAIR + GDPR auditor — checks a project folder, scores bronze / silver / gold
docs/        Design: schema database, DMP decision tree, harmonisation, RO-Crate, ARC
```

## The capture app — for daily use

`app/metadata_app.html` — open it in the browser, no installation, runs on Linux, Windows, Mac.

- Open, fill, close, reopen → filled fields stay (autosave in the browser).
- **Save a template** — start the next experiment run from the last one's values and change only
  what differs.
- **Open a data folder** (Chrome / Edge) — the app sees your raw files and writes the metadata as
  `<project>.meta.json` next to the raw data. An old experiment can be annotated the same way:
  open the folder → the app loads what is already there → you add the rest.
- Only the **amber** fields need filling; the rest is already there — and still editable, in case
  the machine got it wrong.
- **Export** to ArrayExpress, GEO, ENA, RO-Crate, or as a gap sheet for colleagues.

What the browser app deliberately does not do, and where other tools help: author / title / abstract
in DataCite format is produced by the LMU DataCite generator; for deeply OS-integrated folder
workflows there are desktop tools such as MetaFold. This app stays deliberately
platform-independent HTML.

## Readiness is not conformity

The European Health Data Space (Regulation (EU) 2025/327) applies from 2029 and its technical
specifications are still taking shape. The goal is a dataset that can be shaped into whatever final
form is required — not a claim of conformity today.

## License & contact

MIT (code) · CC-BY-4.0 (standard / documentation). See `LICENSE` and `CITATION.cff`.
Core Unit Research Data Management (cRDM), University of Würzburg — coreunitrdm@uni-wuerzburg.de
