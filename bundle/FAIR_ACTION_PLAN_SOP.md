# FAIR action plan — the per-project SOP each project chat executes

*This is the bridge between the FAIR-in-action bundle (the rules) and an individual
project chat (the doing). Give this file — plus `STACK.md` — to any project chat, and it
produces a concrete, ordered, checkable action list for **that** project. Machine-readable
so an AI executes it; human-readable so a person follows it.*

**Naming standard (decided):** every project folder is `DECIDE_<subproject>_<topic>`
(e.g. `DECIDE_A03_TripleRNAseq-SkinMicrobiome`). The PI and people go in the metadata, not
the folder name. Topic uses `CamelCase` words joined by `-`.

---

## How a project chat uses this

1. The project chat is opened with: this file + `STACK.md` + the project's own tree/metadata.
2. It runs the **assessment** (Part 1) → produces the project's current tier.
3. It emits the **action list** (Part 2) → ordered, each item marked `auto` (AI does it),
   `human` (you do it), or `check` (confirm before publish).
4. It writes the result to `documents/planing/FAIR_ACTION_PLAN.md` in the project — so the
   plan lives in the project, not only in a chat.

---

## Part 0 — INTAKE (gather what exists BEFORE assessing)

The bundle adapts to the project, not the reverse. First, collect the project's own
material — read the connected folder, or ask the person for:

- folder tree (as-is) · existing metadata (.sdrf/.idf/sample sheet/docx/notes)
- the experimental protocol (docx / ELN entry / ELN link) — the richest metadata source
- scripts · reports · project plan · current results · manuscript

Extract metadata from what exists — a protocol docx often contains the organism, treatment,
timepoints, library prep, and instrument already. Do NOT ask a human for anything the
project's own files already answer. The size of the [human] list = what the existing
material does NOT contain.

## Part 1 — assessment (the chat runs this first)

For the project, determine and record:

```yaml
project:
  name:            # DECIDE_<subproject>_<topic> — rename if not compliant (see naming SOP)
  assay:           # scRNA-seq | bulk-RNA-seq | dual-RNA-seq | triple-RNA-seq | PacBio | imaging | clinical
  organisms:       # list with roles: host / bacterium / phage / pathogen / fungus
  sensitivity:     # open | restricted | pseudonymised | identifying
  repository:      # ArrayExpress(+ENA) | PRIDE | BioImage-Archive | EGA | Zenodo
  tier_now:        # bronze | silver | gold | not-yet-bronze
```

Then check what exists, using the gold template (E-MTAB-17360) as the reference shape:
structure · README · DMP · LICENSE · checksums · metadata (.sdrf/.idf) · DATAFINDER ·
gates run.

## Part 2 — the action list (ordered, tagged, per project)

The chat emits items only for what's missing. Each item: `[tag] action → where`.

### A. Naming & structure  (do first — it's the foundation)
- `[human]` confirm folder name is `DECIDE_<subproject>_<topic>`; if renaming, **dry-run
  rsync first** (see naming SOP below)
- `[auto]` ensure skeleton: `data/{raw_data,primary_data,secondary_data,meta_data}`,
  `documents/{project_plan,report}`, `scripts/ analysis/ results/ code/ var/`
- `[auto]` lock raw data read-only + verify checksums exist

### B. Metadata  (the core work — the app + schema)
- `[auto]` **build the assay schema** following `for-AI/SOP_build_schema_and_app.md` —
  derive it from the gold template (E-MTAB-17360), adjusted for organism count & library
  type; then generate the project-tailored `metadata_app_<project>.html` the collaborator
  fills. scRNA-seq schema already exists in `for-AI/schemas/`; bulk/dual/triple/PacBio are
  built per project by that SOP.
- `[auto]` prefill: extract `auto` fields (instrument, barcode geometry, library params,
  MD5, file names) from the data / pipeline logs
- `[auto]` inherit `project` fields from the DMP (organism refs, licence, people, protocols)
- `[human]` fill the biological `Characteristics[...]` — the 13 human fields from the gold
  template: organism, age, sex, organism part, individual, cell type, cell line, growth
  condition, disease, developmental stage, stimulus, multiplexing label, library type
- `[human]` **declare the multiplexing** — if CellPlex/CMO or pooled, library ≠ sample;
  say so (the gold template shows 8 samples → 16 rows)
- `[auto]` convert any PDF sample sheet → structured DATAFINDER rows (no PDF-as-data)
- `[auto]` build `DATAFINDER.csv` at root: every sample → conditions → file pointers → ELN
- `[check]` every ontology field is a real CURIE (EFO/NCBITaxon/UBERON/CL/MONDO), not free text

### C. Multi-organism  (dual/triple RNA-seq — A03, A04, A06)
- `[human]` declare every organism with its role (host / bacterium / phage / fungus)
- `[human]` state the read-partitioning method (competitive / sequential / in-silico)
- `[human]` confirm rRNA depletion, not polyA, for any bacterial component
- `[auto]` record the combined reference build(s) exactly (e.g. GRCm39 + E10 + phage)

### D. Provenance & code
- `[auto]` scripts numbered to the project plan; analysis/ mirrors the numbering
- `[auto]` `environment.yml` / lockfile present (reproducible)
- `[check]` notebooks stripped of heavy outputs before any git commit

### E. Deposition  (the repository chain)
- `[human]` confirm repository from the DMP (ArrayExpress for expression → brokers to ENA)
- `[auto]` generate the MAGE-TAB pair: `idf.txt` + `sdrf.txt` (Annotare-ready)
  — use the existing `make_ae_metadata.py` generator
- `[check]` FASTQs accounted for (ENA gets them via ArrayExpress — one submission)
- `[human]` after acceptance: record the accessions (E-MTAB + ERP/ERR) in README + DMP
- `[auto]` code → Zenodo DOI; then cross-link E-MTAB ↔ ENA ↔ Zenodo ↔ paper

### F. The gates  (before anything leaves)
- `[check]` **G1 (share):** FAIR self-check + GDPR check pass
  — the Before-Sharing checklist is often already in `documents/`
- `[check]` **G2 (publish):** accession + DOI + licence confirmed
- `[human, if sensitive]` clinical/identifying → EGA controlled-access, DPO sign-off, and
  the `clinical/SECURE_PROCESSING_no_TRE.md` minimum until a TRE exists

### G. Package  (the aim)
- `[auto]` assemble the RO-Crate (`ro-crate-metadata.json`) — the machine-readable object
- `[auto]` atlas export (scRNA-seq only): the `.h5ad` obs schema for SCEA/CELLxGENE
  — note: **atlas submission is a separate manual step, not automatic**

---

## Part 3 — the naming SOP (safe rename + rsync)

Renaming a folder that rsync mirrors is the highest-risk operation here. The rule:

```bash
# 1. rename on the HPC (the source of truth)
mv DECIDE_A03_MercedesGomez DECIDE_A03_TripleRNAseq-SkinMicrobiome

# 2. DRY-RUN the sync — changes nothing, shows what WOULD happen. READ every line.
rsync -avn --delete <hpc>/DECIDE_A03_TripleRNAseq-SkinMicrobiome/ <nextcloud>/DECIDE_A03_TripleRNAseq-SkinMicrobiome/

# 3. the OLD name still exists on Nextcloud → it would be orphaned, not deleted, unless you
#    sync the parent with --delete. To move cleanly, rename on BOTH sides, or:
#    - rename on HPC, create the new name on Nextcloud, move content, remove old — deliberately.

# 4. only run the real sync (no -n) after the dry-run output is exactly what you intend.
```

**Never** rename on one side and run `rsync --delete` on the parent — it deletes the
old-named folder from the other side. On 182 GB that is a very bad afternoon.

---

## What the chat writes back

The project chat saves its filled action list to:
```
<project>/documents/planing/FAIR_ACTION_PLAN.md
```
with each item checked off as done, and the accessions/DOIs recorded as they arrive. That
file is the project's FAIR status — the thing a PI or successor reads to know where it
stands.

---

*This SOP is step 1 of the maturity path (the rule). The `[auto]`-tagged items are what
becomes step 2 (automation) and then step 3 (the app enforces them). Every `[auto]` item
is a candidate for a script; every `[check]` is a gate that can become an automated
control.*
