# Domain: clinical genomics — Würzburg (UKW → Uni Würzburg)

*Filled example of `_TEMPLATE.md` for patient-derived sequencing data handled between
UKW (Universitätsklinikum Würzburg) and Uni Würzburg. **Sensitivity-first**: every other
decision below is downstream of the data-protection setup, so it comes first here.*

> ⚠ **Nothing in this page is a substitute for the data protection officer.** It records
> the intended workflow so it can be checked, not so it can skip the check. Confirm the
> pseudonymisation routine, the transfer, and the analysis location with the UKW/Uni
> Würzburg Datenschutzbeauftragte(r) **before** any patient data moves.

---

## 0. Sensitivity and legal basis — decide this before anything else

| Question | This project | Confirm with |
|---|---|---|
| Data category | Patient DNA sequence → **pseudonymised** (coded; key held at UKW) | Data protection officer |
| Ethics vote | Presumed in place | The clinical collaborator |
| Data transfer agreement (DTA) | Presumed in place (UKW ↔ Uni Würzburg) | The clinical collaborator + legal |
| Re-identification | Controlled; key stays at UKW, never travels with the data | Data protection officer |
| GDPR Art. 9 basis | Required (health + genetic data) | Data protection officer |

**Genetic data is special-category data under GDPR Article 9**, and pseudonymised genetic
data is still personal data — it can in principle be re-identified. Treat it as
restricted throughout, not as "basically anonymous".

## 1. Unit of study
Patient → sample → sequencing run. The **patient** is the subject; consent and legal
basis attach at patient level and propagate down. The pseudonym (not the name, MRN, or
date of birth) is the ID that appears in every filename and metadata row.

## 2. Vocabularies
| Field | Vocabulary |
|---|---|
| clinical findings | SNOMED CT |
| lab tests / observations | LOINC |
| diagnoses | ICD-10-GM (the German modification) |
| phenotypes | HPO (Human Phenotype Ontology) |
| genomic variants | HGVS nomenclature; ClinVar / gnomAD for annotation |
| organism | NCBITaxon (human = NCBITaxon:9606) |

## 3. Repository
- **Controlled-access only.** For genomic patient data: the **European Genome-phenome
  Archive (EGA)**, never GEO/ArrayExpress (those are open).
- Summary statistics and non-identifying derived results may go to an open repository
  *if* the ethics vote and consent permit — check both.
- Code → Zenodo (the code carries no patient data, so it is open and gets a DOI).

## 4. Machine-readable (extract, never type)
From the FASTQ/BAM/VCF and the run reports: instrument, flowcell, lane, read length,
coverage, reference build, pipeline and tool versions, checksums. Pull these with a
script exactly as for any sequencing project.

**Do not put any identifying field in this layer** — the machine reads technical
metadata, not patient identity.

## 5. Human-only
The clinical variables that are the point of the study: diagnosis, phenotype, treatment,
outcome, family history. These come from the clinician and the clinical record, mapped to
the vocabularies in §2 — **never as free text**, and never carrying a direct identifier.

## 6. The physical route — this is the part that must be right

```
UKW (clinic)                          Uni Würzburg HPC
┌────────────────────┐                ┌──────────────────────┐
│ patient sample     │                │                      │
│   ↓ sequence       │                │  analysis happens    │
│   ↓ PSEUDONYMISE   │  ── move ──▶   │  HERE, on the        │
│ (key stays here) ──┼── key NEVER ──▶│  pseudonymised data   │
│                    │    leaves      │                      │
└────────────────────┘                └──────────────────────┘
```

- Pseudonymisation happens **at UKW, at source**, before any transfer.
- The **re-identification key never leaves UKW** and never travels with the data.
- Only pseudonymised data moves to the Uni Würzburg HPC, under the DTA.
- Analysis is done on the HPC on the pseudonymised data. Confirm whether the HPC is an
  approved location for this data category — if a formal TRE/SPE is required, that must be
  established before transfer, not after.

**Open question for this project (flag to data protection):** is the Uni Würzburg HPC an
approved processing environment for pseudonymised genetic data, or is a dedicated Trusted
Research Environment / Secure Processing Environment (TRE/SPE) required? Do not assume; ask.

**Until that is answered — and it may be that no TRE is available yet — follow
`handout/SECURE_PROCESSING_no_TRE.md`.** It is the defensible minimum: minimise,
pseudonymise at source, isolate on the HPC, log access, no record-level egress, delete on
a stated date. Not a substitute for a TRE, but far better than improvising while you wait
for one.

## Folder note
Use the standard structure (`handout/RDM_handout.docx`), with two clinical additions:
- `data/raw_data/` at UKW is the identifiable source — it may be a **link/reference**, not
  a copy, so identifiable data never lands on the HPC.
- Add `docs/legal/` for the ethics vote, the DTA, the consent template, and the
  pseudonymisation SOP. These are project metadata too.

---

## What the TRE/SPE guideline will become

This project is the first to walk the UKW → Uni Würzburg route, so what you decide here
becomes the reusable guideline for the next clinical project. Capture, as you go, in
`docs/legal/`:

1. **The approved route** — exactly where pseudonymisation happens, how data is
   transferred, which environment analysis runs in, once data protection confirms it.
2. **What must stay at UKW** — the key, and any identifiable field.
3. **The environment's controls** — access control, audit logging, no-egress rules on the
   HPC/TRE, whether results can leave and in what form.
4. **Deletion / retention** — when the working copy on the HPC is deleted; DFG minimum
   retention for the archived record.

Once confirmed and used twice, lift it out of this project into its own
`clinical_wuerzburg_TRE.md` guideline for the group.
