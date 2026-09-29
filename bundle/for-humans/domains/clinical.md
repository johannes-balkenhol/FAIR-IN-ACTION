> **Local version:** for patient data handled between UKW and Uni Würzburg, use
> `clinical_wuerzburg.md` instead — it adds the pseudonymisation route, the
> approved-environment question, and the EGA deposition path.

# Domain: clinical / diagnostic

*Filled example of `_TEMPLATE.md`. This domain is sensitivity-first — every other
decision follows from it.*

## 1. Unit of study
Patient → encounter → measurement/specimen. The patient is the subject; consent and
legal basis attach at the patient level and propagate down.

## 2. Vocabularies
| Field | Vocabulary |
|---|---|
| clinical findings | SNOMED CT |
| lab tests / observations | LOINC |
| diagnoses | ICD-10 / ICD-11 |
| phenotypes | HPO |
| medications | ATC / RxNorm |

## 3. Repository
**Controlled-access** — EGA (European Genome-phenome Archive) for genomic; institutional
or national trusted research environments for records. Rarely open.

## 4. Machine-readable
Instrument exports and LIMS records: assay values, timestamps, device IDs, reference
ranges. Pull from the LIMS rather than transcribing.

## 5. Human-only
Diagnosis, staging, clinical context, treatment decisions, outcomes — the clinician's
knowledge that is not in any instrument.

## 6. Sensitivity
**Identifying or pseudonymised, essentially always.** Decide the legal basis (consent,
ethics approval, GDPR Article 9 basis) BEFORE any data is collected. This domain never
starts "open".
