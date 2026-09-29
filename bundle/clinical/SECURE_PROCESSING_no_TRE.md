# Secure processing without a TRE — a working baseline

*What to do with sensitive data when no formal Trusted Research Environment (TRE) or
Secure Processing Environment (SPE) is available yet. This is not a substitute for a
TRE, and not a substitute for the data protection officer — it is the defensible minimum
so that "we don't have a TRE" never becomes "so we were careless in the meantime".*

> Confirm the specifics with the UKW / Uni Würzburg data protection officer. This page
> records a workflow to be checked, not a permission to skip the check.

---

## The principle

A TRE is a set of *guarantees* — controlled access, no data egress, audit logging,
pseudonymisation at source. You can honour most of those guarantees by discipline before
you have them enforced by infrastructure. The gap between "no TRE" and "a TRE" is real,
but it is much smaller than the gap between "no TRE" and "data on a laptop".

The order is fixed and non-negotiable:

```
1. minimise      collect and move the least data that answers the question
2. pseudonymise  at source, before any transfer — the key never travels
3. isolate       one controlled location, access-listed, not a personal drive
4. log           who accessed what, when — even a manual logbook counts
5. no egress     results leave; record-level data does not
6. delete        the working copy, on a stated date
```

Each step you cannot yet enforce technically, you enforce by written rule and by naming
who is responsible. A rule with a name against it is weaker than a firewall, but far
stronger than an assumption.

---

## The six controls, and how to meet each without a TRE

### 1. Data minimisation
- Request only the variables the analysis needs — not "the whole record just in case".
- Drop direct identifiers at source: no names, MRNs, full dates (use age or year),
  free-text notes that may carry identity.
- Fewer identifying fields is the single most effective control, and it needs no
  infrastructure at all.

### 2. Pseudonymisation at source
- Done **at UKW, before transfer**. The re-identification key stays at UKW.
- The key never travels with the data and never lands on the analysis machine.
- The person holding the key is named in `docs/legal/`.

### 3. Isolation — the "poor man's TRE"
When there is no TRE, approximate one on the Uni Würzburg HPC:
- A **dedicated project directory** with group-only Unix permissions (`chmod 750`, a
  dedicated group, no world access) — not a personal home directory, not a shared scratch.
- **Encryption at rest** for the sensitive directory (LUKS volume, or an encrypted
  container the project mounts) where the platform allows it.
- **No copies** onto laptops, USB drives, personal cloud, or e-mail. The data lives in
  one place and is worked on in place.
- Access limited to the named people on the DTA — nobody else, however convenient.

### 4. Access logging
- If the platform logs access, turn it on and keep the logs.
- If it does not, keep a **manual access log** in `docs/legal/access_log.md`: who was
  granted access, when, and when it was revoked. Low-tech, but it is the auditable trail
  a TRE would otherwise provide.

### 5. No egress of record-level data
- Only **aggregate / non-identifying** results leave the isolated directory — summary
  statistics, model parameters, figures that cannot re-identify anyone.
- Record-level (per-patient) data never leaves. Not in a plot, not in a supplementary
  table, not in a commit.
- Before anything is shared or published, check it cannot re-identify: small subgroups,
  rare-variant tables, and exact dates are the usual leaks.

### 6. Deletion and retention
- State, at the start, **when the working copy is deleted** — e.g. on project close, or
  a fixed date after publication.
- Keep the archived record for the funder's minimum (DFG: 10 years), in its
  controlled-access repository (EGA), not on the working HPC.
- Record who deletes what, and when, in the access log.

---

## Put it in the project

Add to the standard folder structure (`RDM_handout.docx`):

```
docs/legal/
├── ethics_vote.pdf              the approval
├── DTA.pdf                      UKW ↔ Uni Würzburg data transfer agreement
├── pseudonymisation_SOP.md      how it is done, and who holds the key
├── access_log.md                who accessed the data, when (your manual audit trail)
└── data_handling_plan.md        this page, filled in for the project + DPO sign-off
```

`data/raw_data/` for identifiable data is a **link/reference to the UKW source**, not a
copy — so identifiable record-level data never lands on the HPC at all.

---

## The honest limits

This baseline gives you: minimisation, pseudonymisation, isolation, an audit trail,
egress control, and deletion. It does **not** give you: enforced technical prevention of
egress, certified access control, or the legal weight of an accredited environment.

For some data categories that gap is acceptable with the data protection officer's
sign-off; for others it is not, and a real TRE is required before the data may move.
**That decision is the officer's, not yours and not this document's.** What this page
ensures is that when you ask them, you are proposing a considered workflow — not asking
permission to improvise.

---

## When you do get a TRE

Everything above maps onto it: minimisation and pseudonymisation stay exactly the same;
isolation, logging and egress control become enforced rather than promised. The
`data_handling_plan.md` you wrote for the no-TRE case becomes the description of how you
use the TRE. Nothing is wasted.
