# Worked example — a dual RNA-seq project, set up FAIR

*This shows the worksheets filled in for a real project, so you can see what "done" looks
like. Yours will differ; the shape will not.*

## Worksheet 1 — setup
- **Domain:** life sciences / omics · **unit:** sample → library → run
- **Sensitivity:** open (mouse + fungal pathogen, no human material)
- **Licence:** CC-BY-4.0 (data), MIT (code)
- **Data steward:** named PhD student, with ORCID
- **Repository:** ArrayExpress (data) + Zenodo (code)

## Worksheet 2 — the three columns
| machine | project | human |
|---|---|---|
| instrument, flowcell, lane | organisms (mouse + *A. fumigatus*, roles) | infection timing |
| read length, index, checksums | licence, funders, people | rRNA-depletion choice |
| aligner, counts (from logs) | reference genome build | co-infection order |

The machine column (26 fields) was extracted by a script from the FASTQ headers. The
human column was **13 fields** — all anyone had to type.

## Worksheet 3 — deposition
- Code → GitHub → Zenodo DOI, record fixed with real ORCIDs
- Data → ArrayExpress accession
- Cross-linked: the Zenodo record names the accession; the paper names both → **gold**

## The point
104 metadata fields in total. A human was asked for 13. Everything else was read from the
data or written once. That ratio — not the total — is what "designed FAIR" means.
