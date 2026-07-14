# Changelog

All notable changes to the model are recorded here. The model is versioned because
**a project's metadata is only reproducible if the schema it was written against is.**

## [0.1.0] — 2026-07-14 — draft, not yet validated

### Added
- `core_model.yaml` — sample-level core schema, every field tagged `source: auto|project|human`
- Multi-organism with explicit `role` (host / pathogen / commensal) in the **core**, not as an extension
- `infection` as a first-class construct with `time_rel_h` — co-infection has an order, and a flat string cannot express it
- Assay profiles: `scrnaseq`, `bulk-rnaseq`, `proteomics-ms`, `flow-cytometry`
- `app/metadata_app.html` — generated form, OLS4-backed controlled vocabularies
- `TIERS.md` — bronze/silver/gold, every criterion machine-checkable

### Known gaps (do not use in production yet)
- MAGE-TAB nesting is **inferred**, not validated against a real accepted SDRF/IDF
- `export/*.map.yaml` are declared but not written — blocked on PANC E-MTAB-17360
- `extractors/` not implemented — `source: auto` fields are simulated in the app
- `validate.py`, `audit.py`, `gapsheet.py` not implemented
