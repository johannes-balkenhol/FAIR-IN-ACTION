# The FAIR Research Data Object — overview

*Part of the FAIR-in-action bundle. This folder answers one question: **what does a
scientist actually produce, so that a measurement becomes a reusable research object** —
and how is that expressed both for a person (student → PI) and for an AI (Claude, any
assistant), identically.*

This is a **living document**. Paste it into conference or meeting notes; bring what you
learn back here. Each version is dated; the newest is in use.

---

## The idea in one line

A **FAIR Research Data Object** is a measurement plus everything needed to understand and
reuse it — data, metadata, provenance, licence — bundled so that both a human and a
machine can open it and know what it is.

The community already has a standard for exactly this bundle: **RO-Crate**
(Research Object Crate). It organizes file-based data with associated metadata, using
Linked Data principles, **in both human- and machine-readable form** — which is precisely
the dual-audience goal here. So we do not invent a format; we adopt RO-Crate and fill it
with our metadata.

## The four pieces in this folder

| # | File | Form | For |
|---|---|---|---|
| 1 | `01_FAIR_measurement_guidance.md` | human, 1 page | the scientist at the instrument |
| 2 | `02_FAIR_data_object_definition.md` | human | student → PI: what counts as "done" |
| 3 | `03_RO-Crate_profile.md` + `ro-crate-metadata.template.json` | machine (+ its human explanation) | Claude / any AI stack |
| 4 | this file | human | whoever maintains the set |

**They are one thing in two renderings.** The metadata a scientist captures (piece 1),
gathered into an object (piece 2), is written down as an RO-Crate (piece 3). The human
reads the guidance; the AI reads the RO-Crate profile; both describe the *same* object.

## How this connects to the rest of FAIR-in-action

```
        our metadata schema  ─────────────┐   (prototype on GitHub — to be professionalised)
        (LinkML / JSON, the source)        │
                 │                          │
      ┌──────────┴──────────┐               ▼
   human handout        RO-Crate profile   metadata generator app
   (RDM_handout.docx)   (this folder)      (fills the fields)
        │                    │                    │
        └──── one object, three renderings ───────┘
                     ↓
            a FAIR data object you can deposit
            (Zenodo / ArrayExpress / EGA … with a DOI or accession)
```

The **metadata schema** and the **generator app** already exist as prototypes (in the
group's GitHub and earlier design work). They are not yet production-grade — the plan is
to professionalise them step by step. For now this folder gives the *definition and the
target*; the tooling grows into it.

## Prior work this builds on (don't reinvent)

- **`scmeta`** — a schema-driven crosswalk prototype (LinkML-style schema → instances →
  converters → app). The pattern for "one schema, many renderings".
- The **institute-stack design**: LinkML schema in Git → eLabFTW templates (auto-filled
  via API) → Snakemake provenance → **RO-Crate (ro-crate-py) as the packaging layer** →
  Nextcloud + GitHub → Zenodo/domain repo. RO-Crate was already chosen as the bundle
  format; this folder makes that choice concrete and teachable.
- The **ArrayExpress / eLabFTW metadata pipeline** work — the real-world test of which
  fields are machine-extractable vs human-supplied.

## Using this — and keeping it alive

1. **Give a scientist** pieces 1 and 2 (human). Give **an AI** piece 3 (machine). Both
   are now guided by the same definition.
2. **After a conference or meeting**, paste the relevant piece into your notes, mark it
   up, and fold the improvements back here as a new dated version.
3. **As the schema and app professionalise**, piece 3's template stops being hand-written
   and starts being *generated* from the schema — the same "generate the renderings from
   one source" move already used for the metadata app.

## Status

**v0.1 — prototype.** Definitions and the RO-Crate profile are usable now and correct
against the RO-Crate 1.1 spec. The link to a live, schema-generated template is future
work. Everything here is open for discussion and improves with use.
