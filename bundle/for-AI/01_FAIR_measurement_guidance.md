# Making a measurement FAIR — at the instrument

*One page for any scientist, any field. What to do **when you take a measurement** so its
output is reusable from the start — not reconstructed painfully at the end. Do these six
things and your data is already most of the way to a FAIR research data object.*

---

## The one habit

**Capture the context at the moment of measurement, not later.** The machine, the
settings, the sample, the conditions, the date — all of it is known *now* and forgotten
*later*. A measurement without its context is a number nobody can reuse.

Ask, for every measurement: *if a stranger found this file in three years, what would they
need to know to trust and reuse it?* Write that down as you go.

---

## The six things to capture

### 1. Identify the sample — once, with a stable ID
Give the thing you measured a short, stable identifier. Use it in the filename, the lab
notebook, and the metadata. Everything about the sample is found through this ID.
*(One ID, everywhere — see the RDM handout.)*

### 2. Record who, what, when, where
- **Who** did the measurement (a person, ideally with an ORCID)
- **What** instrument / method, including model and settings
- **When** — the date and time (batch effects are dated)
- **Where** — the site, facility, or lab

Most of this the instrument already writes into the file or its log. **Do not re-type
what the machine records** — export it. Only add what the machine cannot know.

### 3. Describe the conditions — the variables you are studying
The treatment, dose, timepoint, concentration, temperature, patient group — whatever the
experiment varies. These are the fields only a human knows, and they are the point of the
measurement. Record them against the sample ID, in a table: one column per field.

### 4. Use the right words — controlled vocabulary
Where a standard term exists for something (an organism, a tissue, a disease, a
chemical, a method), use the **exact** standard term, not free text. "lung" typed by hand
connects to nothing; the ontology term `UBERON:0002048` connects to every other study
that used it. If no standard term fits, say so plainly — never invent one that looks
official.

### 5. Keep the raw output untouched
The unprocessed measurement is the ground truth. Store it read-only, checksum it, and
never edit it in place. Everything else — cleaning, analysis, figures — is regenerated
from it by code.

### 6. Keep it machine-readable
Save in open, structured formats a script can parse: CSV, JSON, plain text, or the
instrument's open export — **not** a PDF or a screenshot for data (fine for a final
report, useless as a data carrier, because tables and figures inside a PDF cannot be
parsed). If your electronic lab notebook can export structured metadata (eLabFTW exports
JSON, CSV, and the cross-ELN `.eln` format), use that export as the record — not a
printout.

---

## What you end up with

If you do the six, each measurement arrives with: a stable ID, its who/what/when/where,
its conditions in controlled vocabulary, an untouched raw file, and everything in
parseable formats. **That is a FAIR measurement** — and gathering a project's worth of
them, with a licence and a description, is a FAIR research data object (piece 2).

---

## The one-minute version

> Give the sample an ID. Record who/what/when/where — export what the machine knows,
> add what it doesn't. Write the conditions in standard terms. Lock the raw file.
> Save everything a script can read. Do it *now*, not later.

*Open for discussion — improves with use. Existing lab rules take precedence where they
differ.*
