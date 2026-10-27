---
title: FAIR Bundle v-next — the intake-to-gold generator (blueprint)
home: Projects/FAIR-in-action/bundle/for-AI/
status: blueprint-for-review
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-19
decisions_taken: gate scheme = G0/G1/G2 canonical; audit via run-kit (no-preference items)
relates_to: FAIR-self-report_v1_2026-10-19.md · cRDM_Gates_register.md · BMFTR grant O1–O4
---

# FAIR Bundle v-next — intake → generate → grow

**One line.** At project start the bundle asks a few questions, decides **which templates apply** to *this* data, and generates the whole project — folder, README, DMP, metadata schema, capture app, analysis pipelines (CWL), archiving + publishing scripts, RO-Crate — so a human *or* a machine keeps it **FAIR + GDPR, bronze → gold, from the first file to the deposited PID**. Every finished project becomes one RO-Crate in a **growing, queryable knowledge base**.

This turns the bundle from an *auditor* (checks at the end) into a *generator + auditor + gate* (correct from the start, checked throughout, released under control). It's the same maturity logic you already use — **rule → automation → control** — applied to the whole lifecycle.

---

## 1. The flow

```
INTAKE questionnaire
      │  (answers: modality, human-data?, consent, licence, sharing, repo, instruments, multi-centre)
      ▼
APPLICABILITY RESOLVER ──► which templates + standards + gates apply to THIS data
      ▼
GENERATE project:  folder skeleton · README · DMP · metadata schema · capture app · CWL pipelines · archiving + publishing scripts · LICENSE · RO-Crate stub
      ▼
CAPTURE (at source: instrument extractors + ELN template + metadata app)
      ▼
PROCESS  ──► CWL analysis workflows (portable: HPC / cloud / Windmill), provenance recorded
      ▼
GATES   G0 ingress · G1 processing · G2 egress
      ▼
DEPOSIT (repo-specific publishing script) → PID
      ▼
RO-CRATE added to the GROWING KNOWLEDGE BASE (data · documentation · analysis, comparable across projects)
```

The researcher never asks "what metadata do I need?" — the intake answered it. The steward's judgement goes into the *resolver and templates once*, not into every project by hand.

---

## 2. The intake questionnaire — what the bundle asks (and what each answer generates)

| Question | Drives |
|---|---|
| Which **modality / assay**(es)? | assay `profiles/*.yaml`, metadata schema, extractors, CWL pipeline |
| **Human / personal data?** | GDPR path, TRE/SPE **gates**, controlled-access repo, pseudonymisation SOP |
| **Ethics vote + consent scope**? | **G0 ingress gate**; open vs controlled deposition route |
| **Licence** (data / code)? | `LICENSE`, README, deposition metadata |
| **Sharing intent** (open / controlled / in-house only)? | access tier, whether an SPE is required |
| **Target repository**? | publishing script (ArrayExpress/ENA, EGA, PRIDE, BioImage Archive, Zenodo) |
| **Instruments** in use? | which extractors capture auto-metadata (FASTQ, FCS, OME-XML…) |
| **Multi-centre?** | ARC/federation profile, project-context service |
| **Growth** (new samples/year, until when)? | versioned releases + changelog plan |

This is the keystone and it's new — it's the "beginning of the bundle" you described. It extends the existing `bundle/for-humans/worksheets/05_project_intake.md` from a worksheet into a *driver*.

---

## 3. The applicability matrix — "which measurement applies to which data"

Not everything applies to every modality. This table is both the **answer to the intake** and the **seed controlled vocabulary**. (Draft — to refine with you; the chats support these rows.)

| Modality | Metadata standard | Controlled vocabularies | GDPR? | Gate path | Target repo | Schema format |
|---|---|---|---|---|---|---|
| scRNA-seq | MAGE-TAB IDF/SDRF, HubMap | EFO, CL, UBERON, NCBITaxon, MONDO | if human | G0→G1→G2 | ArrayExpress/ENA (open) · EGA (controlled) | SDRF + SQL |
| bulk / dual RNA-seq | MINSEQE, IDF/SDRF | EFO, NCBITaxon, GO | if human | G0→G1→G2 | ArrayExpress + ENA | SDRF + SQL |
| PacBio genome | assembly + run metadata | NCBITaxon, SO | rarely | G1→G2 | ENA | JSON + SQL |
| flow cytometry | MIFlowCyt | OBI, CL, PATO | if human | G0→G1→G2 | FlowRepository | SDRF-like + SQL |
| LC-MS proteomics | MIAPE / SDRF-Proteomics | PSI-MS, PRIDE CV | if human | G0→G1→G2 | PRIDE | SDRF + SQL |
| spatial imaging (cycleHCR) | REMBI, OME-NGFF | FBbi, CL, UBERON | rarely | G1→G2 | BioImage Archive | OME-XML + JSON |
| flow-chamber imaging (**FlowSep**) | REMBI (+clinical) | FBbi, MONDO, PATO, UBERON | **yes** | **G0→G1→G2** | BioImage Archive (open) + EGA/NFDI4Health (clinical) | **SQL** (longitudinal) + JSON-LD |
| clinical / human phenotype | FHIR, GA4GH | SNOMED CT, LOINC, ICD | **yes** | **G0→G1→G2** | EGA / NFDI4Health LDH | FHIR + SQL |

Columns *are* the knowledge-graph edges later (Part 7).

---

## 4. Template library — what the bundle already has vs what's missing

**Already in the bundle** (map, don't rebuild): `project.yaml.template`; `profiles/*.yaml` (5 assays); `schemas/` LinkML (one source); `app/` metadata capture app; `arc/` ISA↔ARC; `extractors/` (fastq, fcs); `bundle/` human+machine SOPs incl. `05_project_intake.md`, `04_evaluate_existing_project.md`, `SOP_build_schema_and_app.md`, RO-Crate profile + `validate_crate.py`; `agent/fair_scan.py` auditor; `documents/SOP_make_rocrate.md`, DMP decision tree.

**Missing (the build list):**
1. **Applicability matrix + intake driver** (Parts 2–3) — new.
2. **Generator** — intake answers → emits folder + README + DMP + schema + LICENSE + RO-Crate stub from `project.yaml.template`.
3. **Schema emitters** — LinkML → SQL DDL + SDRF/IDF + JSON-LD/RO-Crate context (JSON Schema/Pydantic may already exist).
4. **CWL analysis pipelines** — turn existing pipelines into portable workflows (Part 6).
5. **Archiving + publishing scripts** — per target repo, driven by the intake's repo choice.
6. **Gates** — G0/G1/G2 SOP + automation (Part 8).
7. **RO-Crate index** — the growing knowledge base (Part 7).
8. **ELN templates** wired to the schema (Labfolder/eLabFTW → SDRF), closing the "capture at source" bottleneck.

---

## 5. Metadata schema — one source, many formats

Keep **LinkML as the single source of truth**; emit whatever the step needs: **SQL DDL** (growing longitudinal collections — FlowSep, clinical), **SDRF/IDF** (ArrayExpress/PRIDE deposition), **JSON Schema/Pydantic** (validation + the capture app), **JSON-LD / RO-Crate `@context`** (the knowledge base). One schema, format chosen per destination — exactly the flexibility you asked for. Decision rule baked into the resolver: *longitudinal/relational → SQL; deposition → SDRF; packaging → JSON-LD.*

---

## 6. Analysis as CWL (portable, provenance-recorded)

Convert the pipelines you already run into **CWL tools + workflows**, so they run unchanged on HPC, cloud, or Windmill and are recorded in each project's RO-Crate provenance. Metadata sheets become CWL `inputs`. Start with the two BMFTR exemplars:
- **A03/A04 RNA-seq**: `qc → trim → align → quant → DE → pathway` (6 stages already scripted).
- **FlowSep imaging**: `catalogue → QC → feature-extraction (226 features) → ICC/models`.

These two become the reference CWL workflows the generator hands to every new project of that modality.

---

## 7. The growing knowledge base (RO-Crate / ARC → knowledge graph)

Each finished project = **one RO-Crate** (data + documentation + analysis + provenance, vocab-bound). Index the crates → a **queryable catalogue**. Because every project was generated from the same applicability matrix and controlled vocabularies, projects become **comparable**: you can ask "all DECIDE scRNA-seq with human donors and a decision-node analysis", or compare documentation/analysis across subprojects. FlowSep's **226-feature set** is the seed relational schema for the analysis layer. This is the knowledge-graph vision — reachable precisely *because* intake standardised every project at creation, not afterwards.

---

## 8. Gates — decided: G0 / G1 / G2

- **G0 ingress** — legal basis, consent scope, pseudonymisation at source, record of processing. *Nothing moves without this.* (A06 + FlowSep blocker.)
- **G1 processing** — secure, in-place; access logged; provenance captured; no record-level egress.
- **G2 egress** — release/publish; the metadata record travels *with* the data; a go/no-go decision is **recorded** (the missing "release gate"); then the publishing script runs.

Human + machine-readable SOP, automated with **Windmill** (platform-agnostic — runs in Nextcloud or standalone, so you stay flexible). The handout's two gates map onto **G1→G2**; G0 is the ingress gate the grant architecture adds. Registered as gate **G4-FAIR / G5-Security** cross-link in `cRDM_Gates_register.md`, and as grant objective **O1**.

---

## 9. Build order (each step = one grant objective + one self-report bottleneck)

| # | Build | Closes bottleneck | Grant |
|---|---|---|---|
| 1 | Applicability matrix + intake driver | #6 one-context, #8 vocab | O3 |
| 2 | Generator (scaffold + README + DMP + schema + LICENSE + RO-Crate stub) | #3 capture, #7 mirror | O2 |
| 3 | Schema emitters (SQL / SDRF / JSON-LD) | #8 | O2 |
| 4 | CWL-ify A03 + FlowSep pipelines | #4 deposition path | O2 |
| 5 | Gates G0/G1/G2 SOP + Windmill | **#1 release gate, #2 legal gate** | **O1** |
| 6 | Publishing + archiving scripts per repo | #4 | O2 |
| 7 | RO-Crate index = knowledge base | — (the vision) | O2/O3 |
| — | Enablement: ELN templates, worksheets, quarterly training | #3 | O4 |

Step 5 is the spine (it's what no project has yet, and it's the grant's lead objective). Steps 1–2 are the keystone that makes "FAIR from the beginning" real.

---

## Decisions I took (you marked no preference)

- **Gate scheme:** **G0/G1/G2**, canonical in the bundle, the grant, and the gates register.
- **Folder audit input:** I've written a **run-kit** (`fair_portfolio_manifest.sh`) — run it on the laptop and the HPC when convenient; it emits a manifest per host, I diff them for the real tiers + the laptop↔HPC mirror state. No rush; the blueprint doesn't depend on it.

**What I'd build first, on your go:** items 1–2 (the applicability matrix + intake driver + generator). To build them against your real bundle rather than blind, send me four files: `project.yaml.template`, one `profiles/*.yaml`, `agent/fair_scan.py`, and `bundle/for-humans/worksheets/05_project_intake.md`.
