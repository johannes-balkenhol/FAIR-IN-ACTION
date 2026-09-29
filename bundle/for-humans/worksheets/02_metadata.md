# Worksheet 2 — metadata capture

*The core discipline: the machine reads what it can, you fill only what is left.*

## Step 1 — list the three sources

Go through every piece of information about your data and put it in one column:

| **machine** (read it) | **project** (write once) | **human** (only you know) |
|---|---|---|
| instrument, dates | organism/subject | condition |
| dimensions, checksums | licence, people | treatment, dose |
| acquisition parameters | funding, ethics | timepoint, site |
| _______________ | _______________ | _______________ |

*(Your `domains/` page lists the usual contents of each column for your field.)*

## Step 2 — extract the machine column

Write a small script that reads those fields from your data files. Run it. **Nobody types
these by hand.** If you catch yourself copying an instrument model into a spreadsheet,
that field is in the wrong column.

The omics implementation does this for FASTQ and FCS files — see FAIR-IN-ACTION for the
pattern to copy.

## Step 3 — fill the human column, with reasons

For each human-only field, write one line: **field | allowed values | why it is needed**.
The "why" matters — people fill fields in properly when they know what the field is for.

Then fill them. This should be a short list. If it is long, you have machine or project
fields hiding in it — move them.

## Step 4 — use controlled vocabulary

For any field where a standard term exists (organism, anatomy, disease, method…), use the
**exact** term, not free text. Free text — "lung" typed by hand — connects to nothing.
The controlled term connects to every other study that used it.

**A wrong controlled term is worse than free text.** Free text admits it is unusable; a
wrong term is confidently wrong and gets believed. If no term fits, record it as a named
characteristic and say so — never force a wrong one.

## Step 5 — capture provenance as you go

Protocol, software version, operator, date, processing steps — this is metadata, not a
methods paragraph to reconstruct later. Write it down when it happens.

---

Done? The human-only fields are filled and validate against a vocabulary. Combined with a
persistent identifier (worksheet 3), that is **silver** — the point where someone else can
reuse your data without emailing you.
