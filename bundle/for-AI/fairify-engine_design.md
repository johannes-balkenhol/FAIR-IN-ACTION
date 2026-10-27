---
title: FAIR-in-Action — the fairify / gdprify engine (design)
home: Projects/FAIR-in-action/bundle/for-AI/
status: design
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-27
relates_to: core_model.yaml · profiles/ · ols_check.py · cv_cache.json · arc/ · gapsheet.py · validate.py
---

# The fairify / gdprify engine

**The flow:** `audit (FAIR + GDPR + gates) → auto-fairify/gdprify what the DATA ALLOWS → emit the gap list of what the experimenter must still provide.`
Every item ends in one of three buckets: **[auto]** done by the engine · **[data]** done from data present · **[request]** the experimenter must supply it.

## 1. One source of truth — the metadata SQL schema

`core_model.yaml` is the schema. Emit it **once** as **SQL DDL** — the relational store you want: `project · sample · assay · file · term` (+ the longitudinal growth you described). Everything else is **generated** from it, never maintained twice. This is the join layer *and* the queryable store that later feeds the knowledge graph.

## 2. Crosswalk — one source → every target format

| Target | When | Produced from `core_model` via |
|---|---|---|
| **JSON / YAML** | always (exchange + manifest) | direct serialisation |
| **SDRF / IDF (MAGE-TAB)** | ArrayExpress + ENA | `arc/sdrf_to_isa.py` (exists) |
| **FHIR** | clinical variables (EHDS / NFDI4Health) | FHIR emitter *(build)* |
| **REMBI + OME-NGFF** | imaging → **BioImage Archive / IDR (EMBL-EBI)** | imaging profile *(build)* |
| **MIFlowCyt** | flow cytometry → FlowRepository | profile *(build)* |
| **SDRF-Proteomics** | PRIDE | profile *(build)* |
| **JSON-LD / RO-Crate `@context`** | the package | RO-Crate profile (exists) |

Which target applies is decided by the **applicability matrix** (modality → standard → repository), already in the blueprint + `profiles/`.

## 3. Ontology binding — current terms → community-accepted

`ols_check.py` + `cv_cache.json` + `build_cv_cache.py` connect to the **Ontology Lookup Service**; `cv_review.py` is the human sign-off. Flow: extract the project's terms → propose **community CURIEs** (MONDO, UBERON, CL, NCBITaxon, EFO, OBI, PATO, FBbi; SNOMED CT / LOINC / ICD for clinical) → auto-bind the unambiguous ones, **[request]** a human confirm the rest. (This is your "current ontologies → community-accepted ontologies".)

## 4. Package — RO-Crate / ARC that can walk (Five Safes)

`arc/` (`make_arc.py`, `isa_model.py`, `fair_to_arc.sh`) + `bundle/for-AI/ro-crate-metadata.template.json` + `validate_crate.py` build the **transferable component**: data + documentation + provenance as **one RO-Crate** (**ARC** for omics, **Five Safes RO-Crate** on the clinical route). That object is what moves between sites under federated-TRE — the data stay, the crate walks.

## 5. gdprify (the GDPR half)

From the audit: set `sensitive`, apply **named-group ACLs** (not world/`users`), pseudonymise the **file tree**, keep the donor-map out of shared/git, set retention. **[auto]** the filesystem-doable parts (perms, sensitive flag, tree scan); **[request]** ethics number, consent scope, DPIA — a human/legal step, never invented.

## 6. Gates — the third audit, and "gate-ready"

`gate_audit`: **G0 ingress** (legal basis / consent / pseudonymisation present?) · **G1 processing** (pipeline version + provenance recorded?) · **G2 egress** (a recorded release decision?). Report gate-readiness; **[auto]** what's doable, **[request]** the rest. Rising G0/G1/G2 coverage over re-runs = the good direction.

## 7. The output — the gap list (what you asked for)

`gapsheet.py` → **`gaps.csv`** (machine) + **`FAIR_GDPR_TODO.md`** (human), every row tagged `[auto] / [data] / [request]`. The `[request]` rows are exactly "the list of missing things the experimenter must provide" — ethics #, consent scope, instrument model, licence choice, a missing accession, etc.

## 8. Have vs build

**Have:** `core_model.yaml` · `profiles/` · `ols_check.py`+`cv_cache.json`+`build_cv_cache.py`+`cv_review.py` · `arc/` · `validate_crate.py` · `gapsheet.py` · `audit.py` · `validate.py` · the FAIR/GDPR audit · `prepare_project.sh`.
**Build:** (a) **SQL DDL emitter** from `core_model`; (b) the **crosswalk emitters** (core_model → SDRF/FHIR/REMBI/JSON-LD) wired per the applicability matrix; (c) the **`fairify` orchestrator** (extract → ontology-map → emit → package → gap-list); (d) **`gate_audit.py`**; (e) a live **OLS refresh** for `cv_cache`.

## 9. The one rule (again)

**One stable ID per entity (`samples.tsv`)** — the join key the SQL schema and every crosswalk depend on. No shared IDs → no crosswalk, no package, no graph.
