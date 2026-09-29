# Domain: life sciences — omics (sequencing, proteomics, flow)

*Filled example of `_TEMPLATE.md`. There is a full software implementation of this one:
github.com/johannes-balkenhol/FAIR-IN-ACTION*

## 1. Unit of study
Sample → extract → library → run → file. A sample is the biological entity; a library
may pool several samples (multiplexing), so **library count ≠ sample count** — the most
common submission error.

## 2. Vocabularies
| Field | Vocabulary |
|---|---|
| organism | NCBITaxon |
| tissue / anatomy | UBERON |
| cell type | CL |
| assay, instrument | EFO / OBI |
| disease | MONDO |
| compound | ChEBI |
Host–pathogen studies list **every** organism with a role (host / pathogen / commensal).

## 3. Repository
GEO or ArrayExpress (sequencing) · PRIDE (proteomics) · FlowRepository (flow) ·
Zenodo for code. Accession for data, DOI for code.

## 4. Machine-readable
Instrument, flowcell, lane, read length, index, checksums — from FASTQ headers.
Cytometer, date, operator, panel — from FCS keywords. Protein/peptide counts — from the
search-engine report. **Two fields the machine cannot get: insert size and run date —
only the sequencing facility knows them.**

## 5. Human-only
Sample identity, condition, infection/treatment and its timing, rRNA-depletion choice,
gating strategy, antibody clones, QC thresholds. ~13–20 fields depending on assay.

## 6. Sensitivity
Usually open (model organisms) or restricted/identifying (human samples → EGA, not GEO).
