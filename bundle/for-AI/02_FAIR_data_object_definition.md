# What is a FAIR Research Data Object?

*For everyone from student to PI. The definition, the scope, and how you know when you
have one. This is the target a project aims at.*

---

## Definition

A **FAIR Research Data Object** is a self-contained bundle of a research result together
with everything needed to find, access, understand, and reuse it:

- the **data** (raw and/or processed),
- its **metadata** (what it is, who made it, how, under what conditions),
- its **provenance** (the chain from raw measurement to result — instruments, software,
  steps),
- a **licence** (how others may use it),
- and a **persistent identifier** (a DOI or accession, so it can be cited and found).

Bundled so that **both a human and a machine can open it and know what it is.**

That last clause is the whole point. A folder of files a human can *maybe* figure out is
not a research data object. A bundle that *tells you*, in a standard form, what each file
is and how they relate — that is.

## The scope — what's in, what's out

**In scope** (part of the object):
- the measurement data and its processed forms
- the metadata and controlled-vocabulary annotations
- the code/workflow that produced the results
- the documentation (README, data dictionary, protocol links)
- the provenance links (ELN, instrument, analysis environment)
- licence and identifiers

**Out of scope** (referenced, not contained):
- data too large or too sensitive to bundle — **link** to it (e.g. raw data staying at a
  clinic, or a multi-terabyte archive). The object points to it richly; it need not
  physically hold it.
- other people's reference datasets — cite them as external entities.

An object may therefore be a **complete package** or a **manifest that points outward** —
both are valid, as long as the pointers are stable and rich.

## The standard we use: RO-Crate

We do not invent a bundle format. **RO-Crate** (Research Object Crate) is the community
standard for exactly this: it organizes file-based data with associated metadata using
Linked Data, in both human- and machine-readable form, and can describe any resource —
files, URLs, or physical samples — along with the people, instruments, software and
licences involved.

Concretely, an RO-Crate is a folder (or zip) containing your files plus one metadata file,
`ro-crate-metadata.json`, that describes the whole object and its parts. See piece 3 for
the profile and a fillable template.

## How you know you have one — the checklist

A result is a FAIR research data object when:

- [ ] every data file has a stable identifier and lives in a structured folder
- [ ] there is metadata describing what the object is and who made it
- [ ] the conditions and key fields use controlled-vocabulary terms, not free text
- [ ] raw data is preserved untouched (or linked at its stable source)
- [ ] the workflow/code that produced the results is included or linked
- [ ] there is a licence
- [ ] there is (or will be) a persistent identifier — a DOI or a repository accession
- [ ] the whole thing is described in an `ro-crate-metadata.json` so a machine can read it

That maps directly onto the FAIR maturity tiers used across FAIR-in-action: the first
rows are **bronze** (structured + licensed), the middle **silver** (validated metadata +
identifier), the cross-linked machine-readable whole is **gold**.

## Why bother — the one-sentence case

Because a FAIR research data object is the difference between a result that dies with the
student who made it and one that the next person — or the next AI — can pick up, verify,
and build on without emailing anyone.

---

*Open for discussion; improves with use. Existing lab and repository rules take precedence
where they differ.*
