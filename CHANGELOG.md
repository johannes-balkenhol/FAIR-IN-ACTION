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

### Added (later the same day)
- `fairlib.py` — shared loader; every script reads the model through one code path
- `gapsheet.py` — CSV/Markdown sheet of only the `source: human` fields still empty
- `validate.py` — schema, enum, ontology-CURIE and organism-role checks, plus a
  `<FILL IN>` placeholder grep. Added because a placeholder survived a commit into
  this repository's own `CITATION.cff`: `$EDITOR` was unset, the editor never opened,
  and nobody noticed. A machine-detectable defect should be detected by a machine.
- `audit.py` — bronze/silver/gold from `TIERS.md`; refuses to score a repo marked
  `is_toolkit: true`

### Known gaps (do not use in production yet)
- MAGE-TAB nesting is **inferred**, not validated against a real accepted SDRF/IDF
- `export/*.map.yaml` are declared but not written — blocked on PANC E-MTAB-17360
- `extractors/` not implemented — `source: auto` fields are simulated in the app

## [0.2.1] — 2026-07-14 — the ontology cache nearly shipped wrong terms

### Fixed
- **Exact-match-first ontology lookup.** The cache builder went straight to a ranked
  fuzzy search, and OLS obligingly ranked a more specific *child* above the term
  asked for. Every one of these labels exists exactly; we simply never asked:

  | asked for | got |
  |---|---|
  | `skin` | `pedal digit skin` |
  | `nucleic acid sequencing` | `nucleic acid extraction` |
  | `COVID-19` | `post-COVID-19 disorder` |
  | `Clostridioides difficile infection` | `…, non-human animal` |

### Removed
- **PR (Protein Ontology) as the flow-marker vocabulary.** 14 of 14 seeds failed,
  and the near-misses were worse than the misses:

  | asked for | cached |
  |---|---|
  | `CD4` | `PR:P16070-10` — CD44 antigen isoform h10 — **a different protein** |
  | `CD8a` | `PR:F1NXT4` — uncharacterized protein, **chicken** |
  | `CD45` | an isoform, not the antigen |

  PR names protein *entities*; immunologists name antibody *targets*. Different
  vocabularies; no query tuning bridges them. `CD4 → CD44` would have entered a
  panel, an SDRF and a submission looking authoritative.

### Added
- `cv_review.py` — shows every non-exact match before it ships; `--prune` keeps only
  exact ones. **This is the check that caught the above.**
- `MARKER` — a hand-curated vocabulary of 35 flow markers. Not an ontology, and it
  does not pretend to be. An honest controlled list beats a confident wrong CURIE.
- **RRID promoted** to the real antibody identifier in the flow profile. `RRID:AB_xxxxx`
  resolves vendor, clone and lot lineage — which is what actually needs identifying.
- The app labels unverified (fuzzy) cached terms **`unverified`** in red, so a fuzzy
  hit can never masquerade as an authority.

### The lesson, recorded because it will recur
A wrong CURIE is worse than free text. Free text announces its uselessness; a wrong
CURIE is *confidently* wrong and will be believed — by a curator, by an atlas, by
whoever reuses the data in five years. Every automated vocabulary lookup needs a
human review step, and the review step needs to make wrongness *visible* rather than
leaving it silent.
