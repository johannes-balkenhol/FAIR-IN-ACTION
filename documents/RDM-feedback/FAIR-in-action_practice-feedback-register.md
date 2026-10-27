---
title: FAIR-in-Action — Practice-Feedback Register
home: Projects/FAIR-in-action/documents/RDM-feedback/
status: living-register
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-25
purpose: real-session lessons ("what actually broke") → concrete bundle changes. Grows as feedback arrives.
sources_so_far: A06-CXCL10 (2026-10-06, ALM bulk RNA-seq analysis session) · A04 epithelial-coinfection + butyrate (2026-01-08 / 2026-10-08, bulk RNA-seq FAIR structuring)
---

# FAIR-in-Action — Practice-Feedback Register

Two real sessions have now fed back. They agree strongly, and five of the lessons are **new** to the bundle. This register turns them into changes with a home, and tracks which projects still owe feedback.

## A. Lessons → bundle changes (merged, deduplicated)

| # | What broke (lesson) | Evidence | Bundle change | Lands in | Pri |
|---|---|---|---|---|---|
| 1 | **Input/provenance check came too late** | CAALFM pathogen genes slipped into the host analysis → **49 tables wrong**, found only by a collaborator | **Mandatory step-00 assert** (expected ID-namespace e.g. "ENSG=human", expected dimensions) that **stops the pipeline** on deviation | scaffold step-00 + validator (an *analysis-level* G0 check) | **HIGH** |
| 2 | **No Git for code** | all session code (fix, scripts 28–34) only local on HPC — no history, no backup | **git init + .gitignore** (exclude `data/ analysis/ *.zip`) as a **non-optional** scaffold step; code committed, not copied | scaffold; the biggest open **R** gap | **HIGH** |
| 3 | **Provenance not carried in artifacts** | "Glycolysis" meant KEGG or Hallmark in adjacent panels — same name, different values | every **table header + figure caption carries** DB + version + contrast + shrunk/raw | output convention + a caption check | **HIGH** |
| 4 | **Outputs lost / mixed versions** | manuscript v1–v9 with figures composed from mixed panel versions; **v4 figures + docx lost to an ephemeral cloud container**, never on HPC | **single source of truth**: figures composed **fresh from `analysis/`**, never a manual intermediate; **outputs persist to HPC**, never a throwaway session; build-date/checksum compare | build convention + persistence rule | **HIGH** |
| 5 | **Transfers fragile** | wrong ZIPs, empty folders from `rm -rf` before upload confirmed, 423 file-locks, rclone auto-created wrong target; old Nextcloud folders survived purge (404); partial sync (721 MB vs 1.98 GB) | **self-checking transfer scripts**: verify count/checksum **before** delete and **before** sync; never remove source until target confirmed | transfer SOP + script (same *verify-before-delete* rule as the cRDM cleanup) | **HIGH** |
| 6 | **Canonical repo architecture not realised** | code not under FAIR names, a `coninfection` typo repo, no cross-links | scaffold wires the layout: **GitHub = code** (+ CITATION.cff, .zenodo.json) · **Nextcloud = processed + results** · **ENA = raw** · **Zenodo = DOI** · **RO-Crate/ARC wraps all**, PIDs cross-linked | scaffold + README template | MED |
| 7 | **SDRF sample-ID alignment = the recurring Silver-blocker** | A04 SDRF 4-row skeleton vs 12 real h5ad samples; BAM-suffix join | **canonical `samples.tsv`** as the single ID source; SDRF built from it; join-check script | scaffold + validator | MED |
| 8 | **Metadata only in one format** | A04 target: one source → many outputs | `project.yaml` + `metadata/auto.yaml` → emit SDRF / IDF / metadata.json / RO-Crate; **parse `.eln`** (RO-Crate based) to auto-fill protocol fields | schema emitters + .eln extractor | MED |

Items 1–5 are new and sharp. 1 is an analysis-level ingress check (G0 logic applied inside the pipeline); 2–5 are the capture/provenance/reproducibility layer that the self-report flagged in the abstract — now with concrete failure cases behind them.

## B. GDPR / human-data items → a checklist in the scaffold (fillable `project.yaml` fields)

- **Ethics vote / approval reference** — filled *before* any deposition (GEO/ArrayExpress require it; A06 manuscript still has `[REF]`).
- **donor_id → identity mapping** — never in the shared folder or Git; kept in a secured area. Check each project for a stray mapping.
- **Raw-data access circle** — documented and restricted to the consortium (276 GB of pseudonymised *human* sequence data in A06's shared folder).
- **Retention / deletion concept** — a date in `project.yaml` / DMP.

These are the project-level, fillable version of the EHDS/GDPR context note.

## C. What worked — keep (the bundle is validated here)

- **111 possible fields → ~20 human questions** per project (the three-tier auto/project/human model earns its keep).
- **Numbered analysis steps** (`00_ 12_ 13_ …`) + consistent folder tree + **README-per-folder** = blind navigation.
- **Open formats throughout** (.tsv/.png/.md/.docx); **standard gene sets** (MSigDB Hallmark) not ad-hoc lists.
- **Per-step scripts** with explicit inputs/outputs + method header.
- **Multi-organism `role:` entries**; **co-infection time ordering** (`time_rel_h`, not a flat treatment string); **EFO vs OBI** protocol distinction (prevents silent IDF failures); structured **`gaps.csv`** instead of open-ended data requests.

## D. Coverage — what feedback is still missing (and the questions it answers)

| Modality / project | Feedback yet? | What it would surface | Key questions |
|---|---|---|---|
| bulk / dual RNA-seq (A04, A06) | ✅ have | capture, provenance, transfer, Git | *covered above* |
| **imaging** (FlowSep, cycleHCR) | ❌ none | the **missing imaging assay profile**; OME-NGFF/REMBI capture; 100 GB–1 TB/experiment handling | does the structure hold at TB scale? what breaks in capture? |
| **clinical / human-data path** (ALM myeloid) | ⚠ partial (grant chat) | the **G0 legal gate** + **recorded release decision** in practice; TA/clinician usability | TA-unaided run? is the release decision recorded? |
| **single-cell / atlas** (Z02) | ❌ none | provenance when **ingesting many public sources**; controlled vocab at integration; CellWhisperer egress | how does provenance travel across merged sources? |
| **flow cytometry** | ❌ none | MIFlowCyt capture; FlowRepository deposition | — |
| **proteomics (LC-MS)** | ❌ none | SDRF-Proteomics; PRIDE | — |
| **metadata app usability** | ❌ none | the TA/clinician intuitive test (grant **O4**) | can a non-specialist use it without the steward? |

## E. Can I pull feedback from the chats directly?

**Yes.** For any project with a working chat I can `conversation_search` + read it and generate the same *what-worked / what-broke / bundle-change* feedback in this format — the way the self-report was built. The highest-value next pulls, because they cover the biggest gaps above:

1. **FlowSep** (imaging gap — the missing assay profile, TB-scale capture).
2. **ALM / myeloid clinical chat** (the legal gate + the recorded release decision + TA usability — the clinical case the grant leans on).
3. **Z02 cycleHCR / CellWhisperer** (imaging + secure egress).

Say which, and I'll generate them straight into this register — no need to wait for someone to write a feedback doc by hand.

---

## F. Chat-pulled feedback (2026-10-25)

Generated by reading the project chats directly (FlowSep / ALM / Z02), in the same what-worked / what-broke / lesson format.

### F1 · FlowSep — sepsis flow-chamber imaging (the imaging gap)

**Worked** — the **metadata-collection app enforces the schema at capture** ("born FAIR": controlled fields, shear/chip/coating ChEBI-linked, auto-generates the experiment ID, units shown) · numbered HPC notebooks (00→05) where every figure regenerates from code · **SHA-256 fixity** over 1,217 raw files (found 22 duplicate acquisitions; the stable identity across 8 date formats) · **LinkML single source** already generates JSON Schema + Pydantic + SQL DDL.

**Broke** — **`experiment_id` doesn't exist in the pipeline**, so every row fails validation twice; of 38 schema fields vs 29 catalogue columns, **only 3 names match** — the crosswalk *is* the work · **the schema was never loaded** (no `.db`/`.sqlite`/`.parquet` anywhere — schema exists, nothing in it) · **catalogue-version chaos**: 36 catalogue files, six tables all named `qc_passed_data_v2` with 301/378/381/949/998/1090 rows across three schemas → the numbers disagree across poster/manuscript (1217/1201/1164/1051) · no imaging assay profile packaged · GDPR: **donor initials + acquisition dates in ~200 raw directory names** (pseudonymisation holds in the tables, not the file tree); DMP §5 (ethics/consent/DPIA/VVT) still open; no LICENSE; not an SPE (a copy travels to the university cloud).

**New bundle lessons** — (a) **the layering rule**: image format (OME-NGFF) ≠ study store (relational/SQLite) ≠ exchange (JSON-LD) ≠ deposition (REMBI tabular) — don't let them compete; (b) **package the imaging assay profile** from FlowSep's produced fields (`pixel_area_um2, n_z_planes, duration_s, width_px`) as the REMBI extension — this *fills the known imaging gap* (shared with Z02); (c) **mint `experiment_id` from the SHA-256 at capture** = the imaging version of "ID at the instrument / canonical samples.tsv"; (d) **a schema not loaded is not wired** — the validator must run on real rows (reinforces A06 lesson #1); (e) **freeze one canonical catalogue** (keyed table, not N CSVs) — kills the version chaos and the number disagreement; (f) GDPR: **pseudonymise the file tree too** (initials/dates out of folder names) — a concrete scaffold check.

### F2 · ALM — myeloid panel diagnostics (the clinical gap)

**Worked** — **browser app, no upload** → usable before any clearance (analysis-to-the-data) · second analysis chain raw reads→reviewed variant table **<3 min/sample**, versions + reference builds **pinned** (reproduces from recorded state alone) · **synthetic truth 30/30** variants over 5 reps, accurate ~2pp down to a 3% fraction · surfaced two defects invisible vs the vendor (amplicon caller discarding true variants; systematic artefact) · **7/9** external variants reproduced; replaced a ~3,000 €/case external contract.

**Broke** — **the release decision is a personal judgement, not a recorded/checkable one** (the G2 control gap, the keystone) · **no approved processing environment** for the data (DIZ confirmed) · variants not in a standard format (VCF), versions not formally recorded · ethics vote #, consent scope, secondary-use/deposition coverage OPEN · **2 variants not reproduced** (explain or document) · **TA/clinician-unaided usability (O4) not yet tested**.

**New bundle lessons** — (a) **the recorded release-decision schema (G2 record) is the keystone, and ALM is the testbed** — tabular variant tables are where to build and benchmark the release check first (does the gate match the reviewer, how much faster; false-neg vs two-reviewer disagreement); (b) **the no-upload browser-app pattern** is a transferable component form for "analysis to the data, usable pre-clearance"; (c) **pin versions + reference builds** as a scaffold default; (d) **synthetic-truth validation** (known allele fractions → recovery %) as a bundle test pattern; (e) the legal-ingress checklist (G0) must gate *before* processing.

### F3 · Z02 — cycleHCR spatial imaging + CellWhisperer (imaging + egress)

**Worked** — **raw read-only, steward-only-write** on cycleHCR (the discipline done right) · DMP + publication procedure written; **`metadata.yaml` sidecar records data accession + code DOI**; "freeze notebook + env in a Zenodo release" · collaborative analysis on shared HPC JupyterHub · **CellWhisperer secure-by-design** — on-prem LLM, nothing leaves institutional compute.

**Broke** — **no imaging profile, no BioImage Archive export** (same gap as FlowSep) · 100 GB–1 TB per experiment; **500 GB ingest with no external disk allowed — transfer path unresolved** · containerise-and-freeze **designed, not yet applied** · source publication + access route `<FILL IN>`; VPN-bound (portability) · **release-control: nothing built**.

**New bundle lessons** — (a) **one imaging profile serves both FlowSep and cycleHCR** — build it once; (b) **the self-checking transfer scripts must handle TB-scale / no-external-disk** — a documented large-file ingest path, not just the small-file case; (c) **an AI assistant that can read project data is itself an egress channel** → the **G2 release gate must cover LLM/assistant outputs**, not only files (new scope for the gates spec); (d) **raw-read-only + steward-only-write** is a good default to generalise from cycleHCR; (e) make **containerise + freeze-env** the real reproducibility default.

### Coverage update

imaging (FlowSep, cycleHCR) → now **⚠ pulled from chat** (profile gap + experiment_id/schema-not-loaded + TB transfer) · clinical/ALM → **✅ pulled** (G2 record + O4 usability are the open proofs) · Z02 → **⚠ pulled** (imaging + AI-egress). Still fully open: **flow cytometry**, **proteomics (LC-MS)**, and a real **metadata-app usability (O4) test**.

---

## G. HPC Projects root — landscape feedback (from `ls -l`, 2026-10-25)

Read from the pasted listing of `/storage/users/job37yv/Projects` (no live HPC access). This is *landscape* feedback — what the directory shape itself says about FAIR/GDPR, and what the bundle should prevent from the start.

**Done well (visible):** the DECIDE projects carry FAIR-ish names (`DECIDE_A03_… A04_… A06_… Z02_cycleHCR`); a reusable scaffold exists (`2026-09-29_FAIR-folder-SOP.zip`, `new-RNAseq-project` bundle); `MetadataTemplates/`, `cRDM/`, a metadata app (`DECIDE A04 — Metadata Collection.html`); PANC_cancer (the one completed deposition) is here.

**Visible problems — the bundle should make these impossible:**

1. **Duplication / version sprawl → Findable fails, no single source of truth.**
   - FlowSep ×6: `flowsep · flowsep2 · flowsep2_jeesu_main · flowsep-sync · FlowSep_Vishnu_2025 · _sync_backup_flowsep2` — which is canonical? (the mirror chaos the self-report flagged, now visible).
   - Carboxylase/CarboDB ×~11: `CarboxyPred_Clean · _Final · _Final_baseline_v1 · _v2 · CarboDB-App-v2 · _v3 · _motifs_collab · CarboxylaseDatabase · carboxylase_project · Carboxylase_Server.git · Carboxylase_Aparna`.
   - WaveSheet ×6: `_bench_v2 · _LocalPathfinding(+2 zips) · _terolocal · _terolocal_v2 · _tero_v4 · _tero_v5`.
   - `Clean/Final/baseline/v2` in folder names = exactly the "version tags belong in metadata, not the folder name; one source of truth" lesson (register A#4).

2. **The manifest is detached from its data — the opposite of the core aim.** `butyrate_project.yaml` and `coinfection_project.yaml` sit **loose at the root**, while their data live in `DECIDE_A04_butyrate-organoid/` and `DECIDE_A04_epithelial-coinfection/`. Data + documentation + **manifest must travel together** (the RO-Crate/project-description principle) — here they're separated at the top level. This is the single clearest anti-example of what the bundle exists to enforce.

3. **Loose files at root** that belong inside a project or in `_archive`: `00_setup_*.sh`, `diag_resonance.py`, `n2_hpc.py`, `files.zip`, `*.tar.gz`, `WaveSheet_*.zip`, `run_neuro.out`, `setup_dry.log`, `DECIDE A04 — Metadata Collection.html` (note the spaces in the name).

4. **Mixed naming conventions** in one directory: hyphen (`epithelial-coinfection`), underscore (`Sepidermidis_RNAseq`), CamelCase (`CarboxyPred`), spaces (`DECIDE A04 — …`).

**GDPR signal — from the permission bits (to verify, but visible):** the access circle for sensitive/human projects looks too broad.
- `DECIDE_A06_fungi-coinfection` → `drwxrwxr-x … users` and `flowsep2` → `drwxrwxr-x … users`: readable by the **whole HPC `users` group**, not a consortium-scoped group. A06 is primary human material; FlowSep is pseudonymised human imaging — the access circle should be a named group, not everyone on the cluster.
- Contrast the ones done right: `flowsep` `drwxrws--- job37yv` (private, setgid), `DECIDE_A04_butyrate-organoid` `drwxrwx--- job37yv` (private), `DECIDE_Z02_cycleHCR` `drwxr-sr-x cyclehcr-users` (dedicated group). The pattern exists — it just isn't applied consistently to the sensitive ones.

**Bundle lessons (make these automatic from the start):**
- (a) **One home + version discipline enforced** — run the same structure gate (the cRDM `audit_structure.py` idea) on the Projects root; a new version never spawns a `_Final_v2` sibling, it's a tag inside the project.
- (b) **`project.yaml`/manifest MUST live inside its project** — the scaffold places it there and the audit flags any detached one; this is the enforceable form of "data + docs + annotation + manifest travel together", and it's the precondition for a project being **transportable** under federated-TRE (a sprawling 6-folder FlowSep can't travel; one self-contained crate can).
- (c) **Access-circle as a scaffold default + an audit check on mode bits** — a sensitive project is created with a named group, not `users`; the GDPR checklist (register B) gets a machine check: "sensitive → not group/world readable by `users`".
- (d) **No loose files at root; naming convention enforced at scaffold time** (no spaces, one scheme).

**To turn this into real per-project tiers:** run `fair_portfolio_manifest.sh` on this root (and the laptop root) — it adds README/DMP/project.yaml/git columns + the tier per project, and the laptop↔HPC mirror diff that would resolve the FlowSep ×6 question. I'll convert the output into per-project register rows.
