# Repository mappings

One file per target: `core_model.yaml` field → repository field.

Adding a repository must never require touching the model. If it does, the model
is leaking repository assumptions and needs fixing.

| Target | Mapping | Status |
|---|---|---|
| ArrayExpress (MAGE-TAB SDRF + IDF) | `arrayexpress.map.yaml` | ❌ blocked on a real accepted E-MTAB to reverse-engineer the nesting |
| GEO | `geo.map.yaml` | ❌ |
| ENA | `ena.map.yaml` | ❌ |
| PRIDE (SDRF-Proteomics) | `pride.map.yaml` | ❌ |
| FlowRepository (MIFlowCyt) | `miflowcyt.map.yaml` | ❌ |
| CELLxGENE / Infection Atlas (Z02) | `cellxgene.map.yaml`, `atlas_z02.map.yaml` | ❌ |
| DataCite / data catalogue | `datacite.map.yaml` | ❌ |
| nf-core samplesheets | `nfcore_*.map.yaml` | ❌ |

**These are deliberately unwritten rather than guessed.** Writing the ArrayExpress
mapping from imagination, when a real accepted submission exists on disk, would bake
our assumptions in as if they were facts.
