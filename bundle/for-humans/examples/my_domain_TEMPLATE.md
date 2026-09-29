# Domain: _______________

*Copy this file, rename it for your field (e.g. `neuroscience_ephys.md`), and answer the
six questions. That is all a "domain" is — the general charter, made specific to your
work. If you answer these six, you can run a FAIR project in any field.*

---

## 1. What is the unit of study?

*The thing that gets a stable ID and one row of metadata. Everything else hangs off it.*

> Examples: a sequencing sample · a microscope field of view · a patient encounter ·
> a trapping site · a synthesised compound · a survey respondent · an EEG session.

**Ours:** _______________

And its relationships (one ___ has many ___):

> e.g. one subject → many sessions → many recordings

**Ours:** _______________

---

## 2. Which controlled vocabularies apply?

*Where a standard term exists for a field, using it is what makes your data joinable to
everyone else's. Free text joins to nothing. List the vocabularies your field uses.*

> Examples: NCBITaxon (organisms) · UBERON (anatomy) · SNOMED CT (clinical) ·
> Darwin Core (biodiversity) · ChEBI (chemicals) · HPO (phenotypes) ·
> your instrument vendor's controlled terms.

**Ours:**

| Field it controls | Vocabulary |
|---|---|
| | |
| | |

If your field has **no** standard vocabulary for something, say so explicitly and use a
consistent internal list — never invent a term that looks official but isn't.

---

## 3. Which repository will the data go to?

*Chosen at the START, not at publication — it determines the metadata you must collect.*

> Examples: GEO/ArrayExpress · PRIDE · BioImage Archive · EGA (controlled) · GBIF ·
> PANGAEA · Zenodo (general-purpose, when nothing specific fits) · an institutional
> repository.

**Ours:** _______________

Persistent identifier it issues: _______________ (accession / DOI / other)

---

## 4. What can the machine read automatically?

*List everything already inside your data files or their metadata. You will write a small
script to extract these, and then nobody types them by hand, ever.*

> Examples: instrument model, acquisition date, operator, dimensions, exposure, pixel
> size, read length, channel names, GPS coordinates, sensor calibration, checksums.

**Ours:** _______________

Where it lives (file header, sidecar, export log): _______________

---

## 5. What can only a human supply?

*The irreducible list. Keep it short. If something here could actually be read from the
data, move it to question 4.*

> Examples: the experimental condition, the treatment and dose, the timepoint, the
> clinical diagnosis, the field-site habitat, the hypothesis a sample tests.

**Ours:** _______________

For each, write one sentence saying **why it is needed** — people fill fields in properly
when they know what the field is for.

---

## 6. How sensitive is the data?

*This governs where the data may live, whether it may touch the cloud, and what licence
is possible. Decide it before the data arrives.*

- [ ] **open** — no restrictions
- [ ] **restricted** — access-controlled, but shareable under terms
- [ ] **pseudonymised** — identifiers removed, re-identification controlled
- [ ] **identifying** — contains personal/identifying data; strict handling

**Ours:** _______________

Legal basis if not open (ethics approval, consent, data-protection basis): _______________

---

## That's the domain defined

With these six answered, the charter's general steps become concrete for your field:

1. scaffold the structure, lock the raw data (from the charter — same everywhere)
2. write the extractor for your question-4 fields
3. build the fill-in list from your question-5 fields
4. validate against your question-2 vocabularies
5. deposit to your question-3 repository and cross-link the identifiers

Keep this file with the project. It is the one-page answer to "why is the data set up
this way?" — and the starting point for the next project in your field.
