# Domain: imaging / microscopy

*Filled example of `_TEMPLATE.md`.*

## 1. Unit of study
Image / field of view. One specimen → many fields of view → many channels/z-planes/timepoints.
Model the acquisition hierarchy; do not flatten a z-stack into "an image".

## 2. Vocabularies
| Field | Vocabulary |
|---|---|
| data model | **OME** (Open Microscopy Environment) — the backbone |
| specimen anatomy | UBERON / domain anatomy ontology |
| marker / stain | ChEBI, or a protein/antibody vocabulary |
| imaging method | Biological Imaging Methods Ontology (FBbi) |

## 3. Repository
**BioImage Archive** (general) or **IDR** (curated, high-value studies). Accession issued.

## 4. Machine-readable
Objective, numerical aperture, channels, exposure, pixel size, stage position,
timestamps, bit depth — **nearly all of it is already in the OME metadata** written by the
acquisition software. Extract it; never re-type it.

## 5. Human-only
The biological condition, the specimen preparation, and the analysis/segmentation
parameters (which are not in the image and must be recorded separately).

## 6. Sensitivity
Open for most model-system imaging; identifying for medical imaging of patients
(faces, whole-body scans) — treat as clinical.
