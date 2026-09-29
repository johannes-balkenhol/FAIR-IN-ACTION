# README template — for multi-center, multi-modal projects

*This is the README outline every project should follow, designed for the hard case: data
spread across centers, across modalities (sequencing + imaging + clinical…), and across
places (cloud + git + HPC + ELN). A good README is the **map** that makes such a project
navigable — the cure for "it's half in Nextcloud, half in git, and I can't find anything."*

**How to use:** copy the block below into your project root as `README.md` and fill every
section. The point is that a stranger — a new PhD, a PI, an AI, future-you — can open this
one file and find *everything*, wherever it physically lives.

---

```markdown
# <PROJECT NAME>

<!-- One paragraph: what was studied, in whom/what, why, and by which centers. -->

**Consortium / centers:** <e.g. UKW + Uni Würzburg + partner site>
**Contact / data steward:** <name · ORCID · email — the person who answers questions>
**Status:** <planning | collecting | analysing | published>
**Sensitivity:** <open | restricted | pseudonymised | identifying>  ← if not open, read docs/legal/

---

## 1. Where everything lives  ← THE MAP (fill this richly)

The single most important section. Every part of this project, and where to find it —
across cloud, git, HPC, and the ELN. Use the same sample IDs everywhere.

| What | Where it lives | Link / path |
|---|---|---|
| Raw data | <cloud / archive / stays at center X> | <Nextcloud path or accession> |
| Processed data | <cloud / HPC> | <path> |
| Metadata / DATAFINDER | this repo | `DATAFINDER.csv` |
| Metadata collection app | <git> | <repo URL · e.g. app/metadata_app.html> |
| Analysis code / notebooks | <git> | <repo URL> |
| Pipeline / workflow | <git> | <path · CWL/Snakemake/Nextflow> |
| Intermediate results | <HPC / cloud> | `analysis/` · <path> |
| Final results / figures | this repo | `results/` |
| Lab notebook (ELN) | eLabFTW | <entry URL(s) — same sample IDs> |
| Analysis server | HPC / JupyterHub | <URL> |
| Published dataset | repository | <accession / DOI> |
| Code archive | Zenodo | <DOI> |
| Publication | journal | <DOI, once it exists> |

> If a row is "not yet", write "pending". An empty map is why projects get lost.

---

## 2. Data — by modality  ← for multi-modal projects

One block per data type. Each modality has its own metadata standard and repository.

### <Modality 1 — e.g. bulk/dual RNA-seq>
- **Samples:** <n> · **Organisms:** <host + pathogen(s), with roles>
- **Metadata standard:** ArrayExpress SDRF/IDF (MAGE-TAB)
- **Repository:** ArrayExpress · **Accession:** <E-MTAB-…>
- **Schema used:** <link to the per-assay schema the app filled>
- **Key fields only-a-human knew:** <e.g. rRNA depletion, read partitioning, MOI>

### <Modality 2 — e.g. imaging>
- **Metadata standard:** REMBI · **Repository:** BioImage Archive
- <same structure>

### <Modality 3 — e.g. clinical>
- **Metadata standard:** FHIR + LOINC + SNOMED CT (MII)
- **Repository:** controlled-access (EGA) · **Access:** <conditions>
- <same structure — and see docs/legal/>

*Different modalities, different standards, one project. The DATAFINDER links them by
sample ID.*

---

## 3. Centers — who did what  ← for multi-center projects

| Center | Contributed | Data stays / moves | Agreement |
|---|---|---|---|
| <Center A> | <samples / sequencing> | <stays at A / moves to B under DTA> | <DTA ref> |
| <Center B> | <analysis> | — | — |

The rule for sensitive multi-center data: **identifying data stays at its source center;
only pseudonymised data moves, under a data transfer agreement.**

---

## 4. Structure

```
<project>/
├── README.md            this file — the map
├── DMP.md               data management plan
├── LICENSE
├── DATAFINDER.csv       every sample → its files, conditions, ELN entry (all modalities)
├── data/{raw_data,primary_data,secondary_data,meta_data}/
├── documents/{project_plan,report}/
├── scripts/  analysis/  code/  results/  var/
```

## 5. How to run / reproduce

<Step by step: environment, data access, pipeline order. A stranger should be able to
regenerate the results from raw + code alone.>

```
<clone / environment setup>
<data access instructions>
<pipeline: step 1 → 2 → 3, numbered to scripts/>
```

## 6. Metadata

- **Sample ID scheme:** <pattern — the ID used in filenames, ELN, and every link>
- **DATAFINDER:** `DATAFINDER.csv` — the searchable index of all samples
- **Schemas:** <which per-assay schema(s) the metadata app used>
- **Controlled vocabularies:** <NCBITaxon, UBERON, CL, MONDO, LOINC, SNOMED… as used>

## 7. Compliance

- **FAIR self-check:** <passed / gaps> — see `worksheets/04_evaluate_existing_project.md`
- **GDPR:** <N/A / handled — see docs/legal/>
- **Gates:** G1 (share): <status> · G2 (publish): <status>

## 8. Licence & citation

- **Data licence:** <e.g. CC-BY-4.0 / restricted>
- **Code licence:** <e.g. MIT>
- **Cite as:** <CITATION.cff / DOI>
```

---

## Why this outline, specifically

- **Section 1 (the map) is the fix for "I can't find anything."** A project split across
  cloud/git/HPC/ELN is only navigable if one file says where each piece is. This is that
  file. Fill it richly and link both ways.
- **Section 2 (by modality) handles multi-modal** — each data type keeps its own standard
  (ArrayExpress vs REMBI vs FHIR) without the project fragmenting, because the DATAFINDER
  links them by shared sample ID.
- **Section 3 (centers) handles multi-center** — especially the sensitive-data rule that
  identifying data stays put and only pseudonymised data moves.
- **The same sample ID threads through all of it** — that's what lets one query ("where is
  everything about sample S07?") resolve across every modality, center, and system.

*A README like this is not paperwork — it is the difference between a project a successor
can pick up in an afternoon and one that dies when the student leaves.*
