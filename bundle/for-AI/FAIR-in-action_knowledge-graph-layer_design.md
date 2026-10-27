---
title: FAIR-in-Action — the knowledge-graph layer (design)
home: Projects/FAIR-in-action/bundle/for-AI/
status: design
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-25
relates_to: core_model.yaml · profiles/ · cv_cache.json · arc/ · export/ · FAIR-bundle-vnext_blueprint
---

# The knowledge-graph layer

The goal: **every project meets one standard, each in its own way, and together they form a queryable knowledge graph that shows the gain.** This note shows that the graph is a thin layer on what the bundle already has, defines its schema, and names the "plus X" beyond standards.

## 1. The principle — one standard, many profiles

- **One baseline everyone meets** → comparability. That's the FAIR tier ladder (`TIERS.md`) + the shared **`core_model.yaml`**.
- **Each project's own requirements** → fit. That's the per-modality **`profiles/*.yaml`** (scRNA-seq, bulk-rnaseq, pacbio-genome, flow-cytometry, proteomics-ms…).
- **"Same standard, different requirements" = core + profile.** This is already your architecture — and it is *exactly* the precondition for the graph: a shared core and vocabulary-bound fields are what let two different projects link. Without the common core there is nothing to join on.

## 2. What the bundle already has (≈80% of the graph)

| Graph need | Already in the bundle |
|---|---|
| the schema (entity types + fields) | **`core_model.yaml`** (24 KB) |
| per-modality requirements | **`profiles/*.yaml`** |
| vocabulary binding (the edges) | **`cv_cache.json` · `build_cv_cache.py` · `ols_check.py` · `cv_review.py`** |
| checks | `validate.py` · `audit.py` · `fairlib.py` · `gapsheet.py` |
| the per-project unit (data+docs+annotation together) | **`arc/` · `ARC_and_RO-Crate.md` · `export/`** (RO-Crate / ARC) |
| capture | `app/` · `build_app.py` |

The graph layer adds only: *index the crates → build the graph → view it.*

## 3. The graph schema

**Nodes:** `Project · Biosample · Assay · Organism · Disease/Condition · Tissue · CellType · Analysis/Workflow · Feature/Result · Person(ORCID) · Instrument · Repository(accession/DOI)`.

**Edges — all drawn from the vocabularies you already bind:**
`Project —has_sample→ Biosample` · `Biosample —organism→ NCBITaxon` · `Biosample —disease→ MONDO` · `Biosample —tissue→ UBERON` · `Biosample —cell_type→ CL` · `Project —assay→ EFO/OBI` · `Analysis —produces→ Feature` · `Project —deposited_in→ Repository`.

**The comparability edges** are the shared terms: two projects that both touch **MONDO:sepsis**, **NCBITaxon:*C. difficile***, a shared **UBERON** tissue or a shared pathway become **linked nodes**. That link *is* the gain — it's what turns a pile of folders into a map.

## 4. The build pipeline, and the "plus X"

```
project → RO-Crate (vocab-bound metadata, one stable ID per entity)
        → crate index (all projects' crates)
        → build graph (nodes + edges from the core_model's bound fields)
        → visualization (filter by ontology term)
```

Standards get you most of the way; **"plus X" is the part beyond the standards:**
- **(X1) One stable ID per entity, carried across projects** — the `experiment_id` / `samples.tsv` lesson. No shared IDs → no joins → no graph.
- **(X2) The RO-Crate as the graph's unit** — data, documentation and annotation travel together, so each project contributes one self-describing node-set (and becomes transportable under federated-TRE at the same time).
- **(X3) A crate registry/index** — one list of every project's crate, local or on HPC.
- **(X4) A graph store + viz** — JSON-LD/RDF into a small store, or `networkx` → a self-contained HTML force-directed view.
- **(X5) The applicability matrix** — which standard/profile applies to which modality (from the blueprint) — this is the map that keeps "one standard, many profiles" coherent as the graph grows.

Note the dependency: the graph is only as good as X1. The single most valuable prep step is enforcing one stable ID per entity at capture — which the audit + the metadata app already push toward.

## 5. Showing the gain — two kinds

- **Operational gain** (adoption): the VRC Nextcloud has onboarded **~380 users since Apr 2025**, with onboarding spikes (Jun 2025: 54, Apr 2026: 46, Jun 2026: 29). One panel of a "gain" dashboard.
- **Scientific gain** (the graph itself): cross-project **reuse and comparison made visible** — which projects share a disease, organism, cell type or pathway; which DECIDE subprojects could feed one atlas or one decision-node analysis; where a method built for one project transfers to another. This is the argument a reviewer (and a PI) can see at a glance.

## 6. Build order (small, concrete — each reuses existing files)

1. **`crate_index.py`** — walk the project roots, collect each project's RO-Crate / `project.yaml`.
2. **`build_graph.py`** — crate metadata → nodes + edges, binding to the `core_model.yaml` vocab fields + `cv_cache.json`. Emits JSON-LD (+ a `networkx` graph).
3. **`graph_view.html`** — a self-contained force-directed view; filter by ontology term; click a term to see every project that touches it.

Nothing new is added to the standards — the graph is read out of metadata the projects already carry.

## 7. To build a real one

Send me a few real `project.yaml` / crate files (the `DECIDE_A0x` ones are ideal, since they share organisms and conditions) **or** the `fair_gdpr_audit.py --json` output across the roots. With real metadata I'll build `crate_index.py` + `build_graph.py` and a demo `graph_view.html` so you can see the first cross-project links — the proof of the gain.
