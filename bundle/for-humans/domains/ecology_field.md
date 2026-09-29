# Domain: ecology / field / environmental

*Filled example of `_TEMPLATE.md`.*

## 1. Unit of study
Site → observation/sample. Location and time are first-class — an observation without
coordinates and a timestamp is nearly useless.

## 2. Vocabularies
| Field | Vocabulary |
|---|---|
| occurrence records | **Darwin Core** (the standard for biodiversity) |
| taxonomy | GBIF backbone / NCBITaxon |
| environment | ENVO (Environment Ontology) |
| traits | relevant trait ontology |

## 3. Repository
**GBIF** (occurrences) · **PANGAEA** (earth/environmental) · Dryad or Zenodo (general).
DOI issued.

## 4. Machine-readable
GPS coordinates, logger and sensor files, timestamps, sensor calibration, device
metadata. Data-logger output is a rich, ignored source — parse it.

## 5. Human-only
Habitat description, sampling method and effort, taxonomic identification (where not
automated), field conditions, the question the site addresses.

## 6. Sensitivity
Usually open — but **endangered-species locations are restricted** to prevent poaching.
"Open" is the default, not the automatic answer.
