# FAIR from the start — a charter for any scientific project

*Attach this single file to any new Claude Project — omics, imaging, clinical,
ecology, whatever the domain. It states what "make this FAIR" means in general.
The domain-specific detail (which file formats, which ontologies, which repository)
is layered on top per project; this is the part that does not change.*

Reference framework (an omics implementation of these ideas):
github.com/johannes-balkenhol/FAIR-IN-ACTION

---

## The one idea

Every piece of metadata is answered by one of three sources. Tag each field by which:

- **machine** — already in the data or its files (instrument settings, dimensions,
  timestamps, checksums, acquisition parameters). Read it. Never ask a person.
- **project** — the same for every sample, written once at the start (organism/subject,
  licence, people, funding, ethics). Inherited everywhere.
- **human** — only a person knows it (treatment, condition, timepoint, field site,
  clinical variable). **These are the only fields anyone is ever asked to fill in.**

The whole discipline is: **shrink the "human" list to the irreducible minimum, then
make that pleasant to fill.** If someone is being asked for something the machine
already recorded, the tooling is broken, not the person.

This holds regardless of domain. A microscope image, a soil-core measurement, a
patient record and a sequencing run all split their metadata this way.

## What FAIR actually requires (the letters)

- **Findable** — a persistent identifier (DOI/accession), and rich enough metadata
  that someone can find the data without already knowing it exists.
- **Accessible** — retrievable by that identifier, under stated conditions. "Accessible"
  includes "access is controlled but the rules are explicit" — sensitive data is still
  FAIR if the gate is documented.
- **Interoperable** — controlled vocabularies and shared formats, so the data joins to
  other data. This is where free text goes to die: "lung" as text connects to nothing;
  `UBERON:0002048` connects to every other study that used it.
- **Reusable** — a clear licence, full provenance, and enough context that a stranger
  can reuse the data without emailing you.

FAIR is about the **metadata and the machine-readability**, not about being open. Closed
data can be exemplary FAIR; open data can be terrible FAIR.

## Principles that hold for every domain

1. **Decide sensitivity first.** Open / restricted / pseudonymised / identifying. It
   governs where the data may live, whether it may touch the cloud, and what licence is
   possible. Everything else depends on it. Decide it before the data arrives.

2. **Raw data is immutable.** The unprocessed data is the only irreplaceable thing.
   Lock it read-only, checksum it, never edit in place. Everything else regenerates.

3. **A licence is not optional.** Data with no licence is legally unreusable, however
   open it looks. Choose one at the start.

4. **Controlled vocabulary over free text, always.** Where a standard vocabulary exists
   for a field, use its exact term. A *wrong* controlled term is worse than free text —
   free text admits it is unusable; a wrong term is confidently wrong and gets believed.
   If no term fits, record it as an explicit named characteristic and say so — never
   force a wrong one.

5. **Structure the identity of the thing.** Whatever the unit of study — sample, image,
   patient, site, specimen — give it a stable ID that appears in every filename and every
   metadata row, and model its real relationships (one subject → many samples → many
   measurements) rather than flattening them.

6. **Provenance is metadata.** How the data was produced — protocol, instrument,
   software version, operator, date, processing steps — is part of the record, not a
   separate methods paragraph written later. Capture it as you go.

7. **Persistent identifiers, cross-linked.** Data gets an accession; code gets a DOI
   (nearly free — one toggle, every release). The gold move is linking them: the code
   points at the data, the data at the paper, and back. Separate identifiers are a start;
   a traversable graph is the "I" in FAIR.

8. **Every check should be mechanical.** "Is the metadata good?" is not auditable.
   "Does every required field have a value from the controlled vocabulary?" is. Design
   the criteria so a script, not a person's judgement, decides whether they pass.

## The maturity ladder (domain-independent)

- **🥉 Bronze** — structured folder, licence, README with a data-availability section,
  raw data checksummed, machine-readable fields extracted. This is *free*: it is setup,
  not effort. A project that is not bronze has not been neglected — it has not been set up.
- **🥈 Silver** — the human-only fields are filled and validate against a vocabulary;
  there is a persistent identifier. This is the real bar: the point where someone else
  can reuse the data without contacting you.
- **🥇 Gold** — identifiers cross-linked, contributors properly credited (ORCIDs),
  environment pinned so the analysis re-runs, and — the real test — the setup reused by
  a second project.

## How to run a project by this charter

1. **State the domain and the unit of study** before anything else. "Imaging, unit =
   field of view." "Ecology, unit = trapping site." This determines the file formats,
   the relevant vocabularies (below), and the repository.
2. **Decide sensitivity**, then licence.
3. **Scaffold** the structure: raw / processed / code / metadata / docs, with raw locked.
4. **Extract** every machine field from the data before asking anyone anything.
5. **Ask a human** only for what remains, with each field explaining why it is needed.
6. **Validate** against the vocabulary; **deposit**; **cross-link** the identifiers.

## Domain-specific layers (attach the relevant one per project)

The charter above is constant. What changes per domain:

| Domain | Unit | Vocabularies | Repository | Machine-readable from |
|---|---|---|---|---|
| Sequencing / omics | sample → library → run | NCBITaxon, UBERON, CL, EFO, MONDO | ArrayExpress, GEO, PRIDE | FASTQ headers, run reports |
| **Imaging / microscopy** | image / field of view | **OME** data model, chemical/marker vocabularies, imaging-method terms | **BioImage Archive**, IDR | **OME-TIFF/metadata, acquisition software** |
| Clinical / diagnostic | patient → encounter → measurement | SNOMED CT, LOINC, ICD, HPO | controlled-access (EGA), institutional | instrument exports, LIMS |
| Ecology / traits | site → observation | Darwin Core, ENVO, trait ontologies | GBIF, PANGAEA, Dryad | logger files, GPS, sensor metadata |

When starting a project, ask which row applies, then work out that domain's specifics
against the general principles above. **The principles do not bend; the vocabularies and
formats are filled in per domain.**

> For an imaging project specifically: the unit is the image; provenance means the full
> acquisition chain (objective, channels, exposure, pixel size, stage position — most of
> it already in the OME metadata and never to be re-typed); the "human" fields are the
> biological condition and the analysis/segmentation parameters; the repository is the
> BioImage Archive; and the interoperability vocabulary is the OME model plus whatever
> ontology names the specimen and the markers. Everything else in this charter applies
> unchanged.
