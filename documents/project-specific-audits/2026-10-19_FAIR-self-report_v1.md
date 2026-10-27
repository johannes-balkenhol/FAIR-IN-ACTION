---
title: FAIR Self-Report v1 — projects, bundle, and the road to TRE/SPE + FAIR-gold
home: Projects/FAIR-in-action/documents/project-specific-audits/
status: draft-for-review
method: scanned across project chats (evidence-based); tiers are estimates to be confirmed by the real folder audit
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-19
scope: FlowSep, DECIDE A03/A04/A06/Z02, CAS — with FlowSep + A06 (AG Löffler) as the two BMFTR use cases
---

# FAIR Self-Report v1

**What this is.** You asked me to scan the chats myself, say how FAIR I think each project is and how the bundle worked, then turn that into tailored questions and a plan to improve the bundle. This is that — built from evidence already in your chats (the "Grant use case summary", "RDM use cases", BMFTR grant, FlowSep poster, and the A04/A06 feedback bundle), **not** from a live look at the folders. The tiers below are therefore *estimates from what the chats say*; the **real folder audit** (Part F) confirms or corrects them.

**The tier scale** (your `TIERS.md`): **Bronze** = findable + structured folder + README + raw read-only · **Silver** = ontology-bound metadata schema, validated, licence set · **Gold** = deposited with a PID, packaged as RO-Crate/ARC, reproducible end-to-end.

---

## Part A — The FAIR ranking (per project, from chat evidence)

| Project | Modality | Data location (laptop ↔ HPC) | Bundle used? | Est. tier | Gap to next tier |
|---|---|---|---|---|---|
| **FlowSep** *(BMFTR #1, Schulze)* | flow-chamber imaging + clinical | both; HPC has flowsep2 / _jeesu_main / -sync / _sync_backup — **mirror state messy** | partial (DMP, LinkML schema, lifecycle) | **Silver−** | schema not wired to data; DMP §5 (ethics/consent/DPIA) open; no SPE; no licence file; no deposition |
| **A06 Löffler ALM** *(BMFTR #2)* | dual RNA-seq, 4 human donors / 32 samples | HPC `DECIDE_A06_fungi-coinfection`; on-prem only | yes (DMP, samples.tsv, check_sample_ids.py, gap-sheet) | **Bronze→Silver** | ethics vote #, consent scope, DPIA, pseudonym log all OPEN; controlled-access route (EGA) undecided; analysis not started |
| **A03 Gomez** triple RNA-seq ±phage | bulk/triple RNA-seq, mouse organoid | both; raw read-only Nextcloud, HPC working copy | yes (full skeleton, git, 6-stage pipeline, IDF/SDRF) | **Silver** | SDRF Source Name rebuild V_1…V_18; host genome version, instrument/strandedness; not deposited |
| **A04-1 Faber** C.diff + butyrate | bulk RNA-seq, organoid, 18 samples | HPC-only raw (87 GB), not synced | yes (SDRF, primary h5ad script) | **Bronze/Silver** | README was stale (described A03); licence open; not deposited |
| **A04-2 Faber/Westermann** Bt/Cd co-infection | network-flow RNA-seq, 12 samples, HT29 | both; raw external | yes (showcase template, Sankey provenance) | **Silver (proposed)** | SDRF 4→12 from real h5ad names; **ENA accession missing → reproducibility chain open** |
| **Z02 cycleHCR** (Beste) | spatial imaging, 100 GB–1 TB/exp | HPC (`DECIDE_Z02_cycleHCR`) | partial (DMP + publication SOP) | **no tier** | **imaging assay profile missing** from bundle; no BioImage Archive export |
| **Z02 Infection Atlas** (Saliba) | integration | HPC | partial | **Silver (proposed)** | no public release; depends on ingested datasets |
| **Z02 CellWhisperer** (Beste) | on-prem LLM | HPC (VPN-bound) | n/a | **pilot** | source pub + access route unpublished; VPN-bound |
| **CAS / Castanospermine** | drug–protein | laptop + HPC | unknown | **unassessed** | not covered in FAIR chats; needs intake |
| **B01 Rudel** Chlamydia | — | not documented | no | **not prepped** | FAIR folder "in preparation" |

**Reading it:** the two BMFTR flagships are the *least* mature on paper — A06 blocked on GDPR/legal, FlowSep blocked on wiring + legal — while the mouse/organoid omics cases (A03, A04) are furthest along precisely because they carry no personal-data burden. That asymmetry is the real story for the grant: the hard cases are hard for legal/TRE reasons, not FAIR-tooling reasons.

---

## Part B — How FAIR I think each flagship really is

**FlowSep.** The FAIR *design* is strong — `flowsep.linkml.yaml` (REMBI-aligned), two-tier access (open imaging / controlled clinical), lifecycle-organised, SHA-256 fixity, planned MONDO/PATO/UBERON/FBbi binding. But three things are *design, not deployment*: the schema isn't connected to the data, there is no SPE (Nextcloud ACLs ≠ an SPE — the analyst still holds a copy), and DMP §5 (ethics, consent, DPIA, VVT) is still "to be determined" while patient data already sits on Nextcloud and HPC. There's also a canonical-catalogue problem: four documents quote four dataset sizes (1217 / 1190 / 1164 / 1051) because no catalogue version is frozen. **Honest tier: Silver-minus by design, Bronze in deployment.**

**A06 (AG Löffler ALM).** Correctly scaffolded (DMP, `samples.tsv` as the single ID source — the lesson learned from A03/A04, `check_sample_ids.py`, ontology-field YAML, gap-sheet). But it is **primary human material (4 donors, 32 samples)**, so GDPR is triggered and everything legal is open: ethics vote number, consent scope for sharing, DPIA/processing record, pseudonymisation log, FEX transfer from UKW. Deposition must go controlled-access (EGA) unless consent explicitly covers open ArrayExpress. Analysis hasn't started. **Honest tier: Bronze, with a clear Silver path once legal is closed.**

Both are single-centre at UKW and multimodal, not yet multi-centre (that comes via the GFDI cohort) — worth stating plainly in the grant rather than blurring.

---

## Part C — How the bundle worked (and didn't)

**What worked**
- The **maturity logic** — *rule (SOP/checklist) → automation (scripts/auditor) → control (the app enforces the schema)* — is exactly the grant's RSE job description. The bundle already embodies it: `schemas/` (LinkML as one source → JSON Schema/Pydantic/SQL), `app/` (schema-driven capture), `agent/fair_scan.py` (read-only bronze/silver/gold auditor), RO-Crate profile.
- **Reuse across modalities** worked: the FAIR skill carried from sequencing to imaging by adding an assay profile. Bronze/Silver/Gold layering, metadata sidecar, publication procedure are modality-independent.
- The **three-tier metadata model** (auto from headers / project-once / ≤20 human fields) matches a real tolerance for manual work.

**What didn't**
- **`samples.tsv`/naming fixed too late.** All three ID-alignment failures (A03, A04, A06) trace to names not being fixed *before* collection.
- **Metadata reconstructed after the fact** instead of captured at the bench. Labfolder→SDRF automation was *designed but never implemented*.
- **No imaging assay profile** → cycleHCR and FlowSep can't be tiered.
- **Nothing has actually been deposited yet**; licences not fixed per dataset.
- **The single biggest gap:** *there is no release gate.* The audit gets data to "deposition-ready", but nothing records the go/no-go decision or carries the metadata record with the data as it moves. "Release-control: nothing built." This is the exact seam where FAIR meets your TRE/SPE **gates** — and it's grant objective **O1**.
- **Portability:** everything is VPN-bound HPC + cRDM Nextcloud + a single steward with write access → it would break at another institution.

---

## Part D — Bottlenecks, ranked (road to all-TRE/SPE, FAIR-gold)

1. **No release/egress gate.** The thing that turns "deposition-ready" into a recorded, auditable go/no-go that carries the metadata. (= grant O1; TRE/SPE G2.)
2. **Legal gate for human data unbuilt.** A06 + FlowSep both stall here: ethics/consent/DPIA/pseudonym-log. Nothing downstream moves until this ingress gate exists. (= TRE/SPE G0.)
3. **Capture-at-source missing.** Labfolder→schema automation; names minted at the instrument, not afterwards.
4. **Deposition never completed end-to-end.** No PID exists for any dataset → no project has reached Gold.
5. **Imaging profile missing** from the bundle (blocks two flagships-adjacent datasets).
6. **No single project-context** read by every service (= grant O3) → metadata re-entered per tool.
7. **Mirror/location chaos.** laptop ↔ HPC copies in unknown sync states (FlowSep especially) → "which copy is canonical" is unanswered, which undermines Findable.
8. **Vocabularies written but not wired** (validate_terms.py exists, not enforced).

Items 1–2 are the spine: they are your TRE/SPE **gates**, and they are the bundle's missing "control" layer. Everything else is Silver→Gold mechanics.

---

## Part E — Tailored questions, per project (the "ask the chats" part)

These are the gaps a FAIR audit can't resolve by itself — the judgement calls. Answers feed Part D and the bundle's next version.

**FlowSep** — (1) Which ethics approval governs the clinical layer, and does consent cover secondary use + deposition? (2) Is the canonical catalogue frozen as v1 yet (one dataset-size everywhere)? (3) Is the LinkML schema wired to the data, or still a sidecar? (4) Final metadata store — `.sql` relational (your lean), OME, or JSON-LD — and the motivated decision? (5) Which of the 226 analysis features become schema fields vs stay in results?

**A06 (Löffler ALM)** — (1) Ethics vote number + consent scope (open vs controlled)? (2) Is a DPIA / processing record started? (3) EGA controlled-access vs split deposition — decided by DPO + ethics, not us: who signs? (4) Pseudonymisation log + FEX transfer from UKW in place? (5) Is the analysis plan written?

**A03 Gomez** — (1) Host genome version + instrument/strandedness confirmed? (2) SDRF Source Names rebuilt V_1…V_18 from a canonical table? (3) Licence fixed (CC-BY-4.0 data / MIT code)? (4) Target repo + ready to deposit?

**A04 (both)** — (1) Is the README still describing the wrong project anywhere? (2) A04-2: **ENA accession for the external raw** — obtained? (3) SDRF expanded 4→12 from real h5ad names? (4) Licence set? (5) Cell-line provenance recorded?

**Z02 cycleHCR** — (1) What imaging profile does the bundle need (OME-NGFF fields, BioImage Archive)? (2) Is the DMP's publication SOP actually run on an experiment yet?

**Cross-cutting** — (1) For each project: which copy is canonical (laptop / HPC / cloud) and what's the sync rule? (2) Which data types actually require which measurement? (this is the controlled-vocabulary / "applicability matrix" you want — not everything applies to every modality.)

---

## Part F — The program, and what I need next

This self-report is **Phase 1**. The rest, in order:

1. **Phase 1 — self-report** *(this doc)*.
2. **Phase 2 — real folder audit.** I can't reach the HPC or the laptop from here, so either:
   - run the bundle's own auditor on both roots and send me the JSON:
     `python3 Projects/FAIR-in-action/agent/fair_scan.py <root> --json > audit_<host>_2026-10-19.json` on **laptop** `/mnt/d/Research` and **HPC** `/storage/users/job37yv/Projects`; **or**
   - paste `tree -L 2 -D` of both roots and I'll build the auditor to match what's really there.
   This replaces the estimated tiers in Part A with measured ones and maps the mirror state.
3. **Phase 3 — answer Part E**, then I consolidate the ranked bottlenecks.
4. **Phase 4 — bundle v-next:** the **gates** (G0 legal-ingress / G1 processing-share / G2 egress-publish) as human+machine SOP + automation (Windmill looks right — platform-agnostic, runs in Nextcloud or standalone), closing bottlenecks 1–2.
5. **Phase 5 — BMFTR realization doc:** the four aims (O1 gates, O2 FAIR+GDPR research object, O3 one project context, O4 enablement), work packages, TRE/SPE measures, gates, and FAIR-gold — each *as realized in FlowSep + A06*.
6. **Phase 6 — knowledge-graph vision:** controlled vocab + applicability matrix → a schema linking data · documentation · analysis (RO-Crate/ARC), with FlowSep's 226-feature set as the seed relational schema.

**One decision before Phase 4:** the **gate numbering is still unresolved** in your own docs — the RDM handout defines **G1/G2** (sharing, publication); the grant architecture uses **G0/G1/G2** (ingress, processing, egress). The bundle, the grant, and the gates SOP must all use one scheme. My recommendation: adopt **G0 ingress (legal/consent) · G1 processing (secure, in-place) · G2 egress (release/publish)** — it's the superset, and the handout's two gates map onto G1→G2. Confirm and I'll make it consistent everywhere.
