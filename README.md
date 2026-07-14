<!-- Badges go live on first Zenodo release. Leaving them visible-but-empty is
     deliberate: an unfilled badge is a to-do you cannot ignore. -->
[![DOI](https://img.shields.io/badge/DOI-pending%20first%20release-lightgrey)](#citing-this)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Model](https://img.shields.io/badge/core%20model-v0.1.0--draft-orange)](core_model.yaml)

# FAIR in action

**A metadata model you can run, not a policy you have to read.**

Most FAIR guidance tells researchers *what* to do and leaves them to do it. This does the opposite: it works out what can be filled in **for** them, fills it, and then asks only for what nobody else could possibly know.

> In the current core model, a researcher is asked for **31% of the fields**. The machine reads 30% from the data itself. The project config supplies the other 39% once, at project start, and never again.

That number is the entire thesis. Everything in this repository exists to keep it low.

---

## The idea in one diagram

Every field in the model carries a `source:` tag. That single annotation generates everything downstream — nothing here is hand-maintained.

```
                       core_model.yaml
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
  source: auto         source: project      source: human
  read from your       written once in      the ONLY thing
  actual data files    project.yaml         a person is asked
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
        ┌──────────┬─────────┼─────────┬──────────┐
        ▼          ▼         ▼         ▼          ▼
   gap-sheet   capture   validator  exporters   audit
   (CSV)        app                 AE · GEO    bronze
                                    PRIDE       silver
                                    Atlas       gold
```

**One model. One app. Many assays.** Assay-specific details live in thin *profiles* that overlay the core — they never repeat it, so `organism`, `factors` and `identifiers` cannot drift apart between assays.

---

## Quick start

```bash
git clone https://github.com/johannes-balkenhol/FAIR-IN-ACTION.git
cd FAIR-in-action

# 1. open the metadata capture app in a browser
xdg-open app/metadata_app.html          # or just double-click it

# 2. choose your assay profile, fill ONLY the amber rows
# 3. export → project.yaml, gap-sheet, or a repository submission
```

Nothing to install. The app is a single self-contained HTML file — it runs offline on HPC, on a laptop, or from a shared drive.

Rebuilding the app after changing the model:

```bash
python3 build_app.py     # regenerates app/metadata_app.html from the YAML
```

**The app is generated. Never edit it by hand.** Change the model, rebuild.

### On the command line

```bash
python3 gapsheet.py --profile scrnaseq -o gaps.csv    # what only YOU can answer
python3 validate.py --profile scrnaseq --online       # schema + ontology check
python3 audit.py    --profile scrnaseq --path .       # bronze / silver / gold
python3 validate.py --self                            # check the toolkit itself
```

---

## What is in here

| Path | What it is |
|---|---|
| [`core_model.yaml`](core_model.yaml) | The schema. Sample-level, nested, ontology-bound, `source:`-tagged. Multi-organism with roles is **core**, not an add-on. |
| [`profiles/`](profiles/) | Assay overlays — [scRNA-seq](profiles/scrnaseq.yaml), [bulk/dual RNA-seq](profiles/bulk-rnaseq.yaml), [proteomics MS/MS](profiles/proteomics-ms.yaml), [flow cytometry](profiles/flow-cytometry.yaml). Each declares only what differs. |
| [`project.yaml.template`](project.yaml.template) | ~20 lines. **The only file where project specifics are allowed.** |
| [`app/metadata_app.html`](app/metadata_app.html) | The capture app. Categorised key–value form, prefilled standards, OLS4-backed vocabularies, multi-format export. |
| [`TIERS.md`](TIERS.md) | Bronze / silver / gold. Every criterion machine-checkable — no judgement calls. |
| [`showcase/`](showcase/README.md) | The projects that prove it works, and their tiers. |
| [`fairlib.py`](fairlib.py) | The one place the model is loaded. Every script goes through it, so they cannot drift apart. |
| [`gapsheet.py`](gapsheet.py) | Emits **only** the `source: human` fields still empty. The sheet you actually email someone. |
| [`validate.py`](validate.py) | Schema, controlled vocabularies, ontology CURIEs, organism roles — and a `<FILL IN>` check, because one survived a commit into this repo's own `CITATION.cff`. |
| [`audit.py`](audit.py) | Bronze / silver / gold, straight from `TIERS.md`. Refuses to score this repo — the ruler is not measured by its own rules. |
| [`build_app.py`](build_app.py) | Model → app. |
| `export/`, `extractors/` | Repository mappings and per-assay extractors. **Not yet written** — see *Status*. |

---

## Controlled vocabularies

Terms are resolved live against **[EBI OLS4](https://www.ebi.ac.uk/ols4)**, with a bundled cache for offline use.

`NCBITaxon` organism · `UBERON` tissue · `CL` cell type · `EFO`/`OBI` assay & instrument · `MONDO` disease · `CHEBI` compound · `PR` antibody antigen · `MS` mass spectrometer

**Do not download ontologies.** They are large and they go stale. Query the API; cache the terms you actually use. If no term matches, the app **refuses free text** and tells you to ask for the vocabulary to be extended. That refusal is the point — free text is exactly what breaks cross-study search, and it is easiest to prevent at the moment of typing.

---

## Design decisions worth arguing with

Three calls are load-bearing. If any is wrong, say so — they are cheap to change now and expensive later.

1. **Library ≠ sample.** `library.extract_refs` is a *list*, and multiplexing is declared in `project.yaml` before data exists. Pooled designs (CMO, hashing) have fewer libraries than samples, and getting this wrong invalidates an entire submission. It has cost us days.
2. **Infection is not a treatment string.** Co-infection has an *order* and an *interval*: `time_rel_h: -24` for the prior pathogen, `0` for the challenge. A flat `treatment: "LPS + Aspergillus"` cannot express that, and the design of half our subprojects depends on it.
3. **Profiles may redefine the chain.** Core defaults to `sample → extract → library → assay → file`. Mass spectrometry has no library; flow cytometry has no library. Profiles override `chain:`. The core provides a default, not a law.

---

## Status — read before you rely on this

**v0.1.0-draft. Usable for capture; not yet usable for submission.**

| Component | State |
|---|---|
| Core model + 4 assay profiles | ✅ written, parse-checked |
| Metadata capture app | ✅ working |
| Tier definitions | ✅ written |
| MAGE-TAB / SDRF nesting | ⚠️ **inferred, not verified** against an accepted submission |
| `export/*.map.yaml` | ❌ not written — blocked on a real E-MTAB to reverse-engineer |
| `extractors/` | ❌ not written — `source: auto` fields are *simulated* in the app |
| `gapsheet.py`, `validate.py`, `audit.py` | ✅ written and tested |

The honest summary: **the model is designed from evidence where we had evidence, and from imagination where we did not.** The exporters are deliberately unwritten rather than guessed.

---

## Showcase — projects that prove it

Ten projects, from a config-driven pipeline that was reused in days, to a full deposition lifecycle with a live accession and DOI. Tiers and links: **[showcase/README.md](showcase/README.md)**

Related consortium showcase: **[DECIDE — Use cases & subprojects](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html)**

---

## How this fits the rest of DECIDE / cRDM

| This toolkit | The consortium resource |
|---|---|
| `TIERS.md` | [FAIR Self-Check](https://www.decide.biozentrum.uni-wuerzburg.de/fair_self_check.html) |
| `core_model.yaml`, `profiles/` | [Metadata Templates](https://www.decide.biozentrum.uni-wuerzburg.de/metadata_templates.html) · [About Metadata](https://www.decide.biozentrum.uni-wuerzburg.de/about_metadata.html) |
| `project.yaml.template` | [How to start a project](https://www.decide.biozentrum.uni-wuerzburg.de/phd_onboarding_blueprint.html) |
| Export → Atlas ingest config | [Infection Atlas](https://www.decide.biozentrum.uni-wuerzburg.de/infection_atlas.html) |
| Deposition targets | [Sharing & Publishing Checklist](https://www.decide.biozentrum.uni-wuerzburg.de/checklist_sharing_publishing.html) |
| Sensitivity routing | [GDPR & Sensitive Data](https://www.decide.biozentrum.uni-wuerzburg.de/sop_gdpr_sensitive_data.html) |

---

## Contributing

The model is a **shared vocabulary**, so changes to `core_model.yaml` affect every project that has already used it.

- **Adding a field to a profile** — open a merge request. Cheap, local, welcome.
- **Adding or changing a core field** — open an issue first. Bump `model_version`. Record it in [`CHANGELOG.md`](CHANGELOG.md).
- **Never** add a project-specific field to core. If a field names a project, it belongs in that project's `project.yaml`.
- **Never** hand-edit `app/metadata_app.html`. Change the model; run `build_app.py`.

A field is only worth adding if you can write its `why:` — one sentence, addressed to the researcher, explaining what breaks without it. If you cannot write the `why:`, do not add the field.

---

## Citing this

Not yet citable — the Zenodo DOI is minted on the first tagged release. See [`CITATION.cff`](CITATION.cff).

## Contact

Core Unit Research Data Management (cRDM), Universität Würzburg — <coreunitrdm@uni-wuerzburg.de>

---

*This repository is a toolkit, not a project: `.fairignore` marks it so the audit script does not score the ruler by its own rules.*
