# FAIR showcase

**The projects that prove the framework — and what each one contributes to it.**

These are not tidy folders held up as examples of virtue. Each one taught the model something specific, and the column that matters is **What it proves**, not the tier.

> **Links, never copies.** Nothing here duplicates data. This page points; it does not hold.

Consortium-level showcase: **[DECIDE — Use cases & subprojects](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html)**

---

## The evidence base

| # | Project | What it proves | Contributed to | Tier |
|---|---|---|---|---|
| 1 | **PlateletWeb 2.0 / platelet proteome** | A pipeline config can be *derived* from a data model instead of hand-written. The architectural blueprint. | `core_model.yaml`, `project.yaml` | 🥇 |
| 2 | **Chen 2024 DIA** *(Omics integration)* | **The business case.** A working DIA pipeline — 6,519 proteins — derived from PlateletWeb's model in days, not months. Reuse is the return on the FAIR investment. | `profiles/proteomics-ms.yaml`, gold criterion **G6** | 🥇 |
| 3 | **FlowSep** | Controlled vocabularies are not bureaucracy — they are what connects your data to community databases. Free text connects to nothing. | `profiles/flow-cytometry.yaml`, the OLS4 vocabulary layer, the audit logic | 🥇 |
| 4 | **PANC_cancer** — PDAC 3D SISmuc scRNA-seq | The **full deposition lifecycle**: ArrayExpress `E-MTAB-17360` · Zenodo `10.5281/zenodo.21353935` · MIT · `CITATION.cff` · HPC↔Nextcloud archive. Also taught us that *library ≠ sample*. | `profiles/scrnaseq.yaml`, `export/arrayexpress.map.yaml`, the identifier tiers | 🥈➕ |
| 5 | **[A03 · Gomez de Agüero](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#a03)** — triple RNA-seq | **Multi-organism metadata.** Host · bacteria · virus in one sample. This is why `organisms` is a list with `role`, in the core, from day one. | `core_model.yaml` (organism roles), `profiles/bulk-rnaseq.yaml` (read partitioning) | 🥈 |
| 6 | **[A04 · Faber](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#a06)** — epithelial co-infection | Co-infection has an **order and an interval**. A flat treatment string cannot express "pathogen A at −24 h, pathogen B at 0 h". | `core_model.yaml` → `sample.infection` | 🥈 |
| 7 | **A04 — *C. difficile* organoid + butyrate** | Assay and model variety: organoids, metabolite treatment. Stress-tests `growth_condition` and `CHEBI` bindings. | `core_model.yaml` (factors) | 🥈/🥉 |
| 8 | **A03 — organoid bulk RNA-seq (Omar)** | Bulk variety. The simplest case — and therefore the check that the model is not over-fitted to single-cell. | `profiles/bulk-rnaseq.yaml` | 🥉 |
| 9 | **[C03 · Ibrahim](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#c03)** — MFA for scRNA-seq | Multi-factor designs. Confirms that `factors` must be a **declared list**, not free text, or the analysis framework cannot consume them. | `core_model.yaml` → `sample.factors` | 🥈 |
| 10 | **[Z02 · Saliba](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#atlas)** — Infection Atlas | **The consumer.** Atlas ingestion is what cell-level metadata is *for* — `cell_type_ontology`, `batch_key`, raw counts. It is the reason scRNA-seq has an atlas export, not just a repository export. | `profiles/scrnaseq.yaml` (cell block), `export/atlas_z02.map.yaml` | 🥈 |
| 11 | **[Z02 · cycleHCR](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#cyclehcr)** — spatial imaging | The gap. Spatial/imaging has **no profile yet** and no repository target wired (BioImage Archive). Honest open front. | *(profile needed)* | — |
| 12 | **A06 — Beilhack & Löffler** — alveolar macrophages / *A. fumigatus* | **The greenfield test.** The first project scaffolded *by* the framework rather than retrofitted into it. Host + fungus = the dual-organism core, used in anger. | *(consumer — validates everything above)* | 🎯 target 🥈 at inception |

**Legend** — 🥇 gold · 🥈 silver · 🥉 bronze · 🎯 target. Criteria: **[TIERS.md](../TIERS.md)**

---

## ⚠️ Two honest caveats

**1. These tiers are proposed, not measured.** `audit.py` is not written yet. Every tier above is a judgement from what the project *contains*, not a score the script produced. **Run the audit before publishing a single label** — a showcase that mislabels its own examples destroys the thing it is advertising.

**2. Publishing tiers on colleagues' projects has social consequences.** A public 🥉 next to someone's name lands differently than you intend, however carefully you frame it. Options, in order of decency:

- Show tiers only for **your own** projects; list the others by **contribution** without a tier.
- Or make tiers **opt-in** — ask each project owner first.
- Or reframe entirely: *"what this project taught the model"* is a compliment, and it is the more interesting column anyway.

---

## ⚠️ Naming error to fix before this is shared

The DECIDE website lists **[Faber as "A06"](https://www.decide.biozentrum.uni-wuerzburg.de/use_cases.html#a06)**. Faber is **A04**. The real **A06** is Beilhack & Löffler — *alveolar macrophages as initial immune contact in invasive Aspergillus infection*.

The anchor `#a06` on the public site therefore points at the wrong subproject. Fix in three places, or the error becomes citable:

- [ ] `use_cases.html` on the DECIDE site
- [ ] Project folders under `~/Projects_shared`
- [ ] Row 6 above (the link intentionally still uses the site's broken `#a06` anchor — update it once the site is fixed)

---

## The paired case study (for PIs who ask "why bother?")

|  | Project | Role |
|---|---|---|
| **Source** | PlateletWeb proteome | The data model and the config-driven pipeline |
| **Reuse** | Chen 2024 DIA | New dataset · same model · **6,519 proteins, in days** |

That is the argument. Not "FAIR is good practice" — *the next dataset takes days instead of months.*

---

## Adding your project

1. Scaffold or retrofit it with `project.yaml`.
2. Run the audit *(when it exists)*.
3. Open a merge request adding a row here — with the **What it proves** column filled in.

If a project cannot fill that column, it is a *user* of the framework, not a showcase for it. That is not a lesser thing; it is simply a different page.
