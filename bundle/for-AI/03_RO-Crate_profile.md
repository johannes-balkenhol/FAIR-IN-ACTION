# The RO-Crate profile — the machine-readable form

*This is piece 3: the same FAIR data object as pieces 1–2, written so a machine (or an AI
like Claude) can read it. Give this file, plus `ro-crate-metadata.template.json`, to an AI
stack, and it is guided by the same definition every scientist follows.*

---

## What this is

**RO-Crate** is the community standard for packaging research data with its metadata,
using JSON-LD (a W3C linked-data format) over the schema.org vocabulary. Its core is a
single file, `ro-crate-metadata.json`, that describes the object as a whole and its
parts. It is designed to be read by both people and machines — which is why it is the
right machine-readable form for our FAIR data object.

`ro-crate-metadata.template.json` in this folder is a **fillable, valid RO-Crate 1.1
template** for a measurement-based research data object. Copy it into a project root,
replace the placeholders, and it becomes the machine-readable description of that object.

## The structure, in plain terms

The metadata file is `{"@context": ..., "@graph": [ ... ]}`. The `@graph` is a flat list
of **entities**, each with an `@id` and an `@type`. The important ones:

| Entity | `@type` | What it is |
|---|---|---|
| the descriptor | `CreativeWork` | says "this is an RO-Crate 1.1" and points at the root |
| **the root** | `Dataset` | the object as a whole: title, description, date, **creator**, **licence**, identifier, and `hasPart` listing its files |
| each file | `File` | a data file, with format, checksum, and links to the sample/measurement it came from |
| the sample | `BioSample` | the thing measured; its conditions hang off it as `PropertyValue`s |
| a condition | `PropertyValue` | one field = one value, with a `propertyID` for the controlled-vocabulary term (e.g. `NCBITaxon:9606`) |
| the measurement | `CreateAction` | the provenance: which **instrument**, which **agent** (person), on which **sample**, producing which **file** |
| the instrument | `IndividualProduct` | the device, ideally auto-extracted from the file/log |

The chain **measurement → instrument → sample → raw file** is the provenance that makes
the object reusable: it records who made what, with which device, from which sample.

## How the three renderings line up

Everything in pieces 1–2 maps onto a slot here:

| Human guidance (piece 1) | RO-Crate slot |
|---|---|
| stable sample ID | `BioSample` `@id` + `name` |
| who / what / when / where | `creator`, `CreateAction.agent`, `instrument`, `startTime`, `Organization` |
| conditions | `PropertyValue` entities on the sample |
| controlled vocabulary | `propertyID` on each `PropertyValue` (the CURIE) |
| raw file kept untouched | `File` with `sha256`, marked as the `result` of the measurement |
| licence | root `license` |
| identifier | root `identifier` |

So the scientist fills in piece 1 by habit; the same facts land in these slots; the AI
reads them here. One object, three renderings.

## For an AI stack

When guiding a project, an assistant should:

1. **Read `ro-crate-metadata.template.json`** as the target shape of the object.
2. Help the scientist fill each slot — extracting `auto` fields (instrument, format,
   checksum, dates) from the data, asking only for the human fields (conditions,
   sample identity, licence choice).
3. **Refuse free text where a `propertyID` is expected** — a controlled-vocabulary CURIE,
   or an honest "no term fits", never a guessed one. (A wrong CURIE is worse than free
   text; see the FAIR-in-action design notes.)
4. Emit a valid `ro-crate-metadata.json` for the project.

## Validate a crate

`validate_crate.py` in this folder does a structural check (valid JSON, descriptor
present and conformant, root is a `Dataset` with the required properties, no dangling
references). It is a minimum check, not full RO-Crate validation, but it catches the
common mistakes:

```bash
python3 validate_crate.py path/to/ro-crate-metadata.json
```

For full validation and richer tooling, the community `ro-crate-py` library is the next
step — noted in the institute stack as the packaging layer, and the direction this
profile grows toward.

## Status and the future

This template is hand-written and valid against RO-Crate 1.1. The **future** is to
**generate it from our metadata schema** (the LinkML/JSON schema prototyped on GitHub),
so the human handout, the generator app, and this RO-Crate profile are all emitted from
one source — the same "one schema, many renderings" pattern the metadata app already
uses. Until then, this is the target shape, filled by hand or by the app.

---

*Grounded in the RO-Crate 1.1 specification (researchobject.org/ro-crate). Open for
discussion; improves with use.*
