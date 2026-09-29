# Evaluate your project — FAIR & GDPR self-check

*For a student or researcher with an **existing** project folder. Go through this by hand,
tick what's true, and read your score at the end. It tells you how FAIR and GDPR-compliant
your project already is, and exactly what to fix next. No tools needed — just look at your
folder.*

Project: _______________     Date: _______________     Checked by: _______________

---

## Part 0 — SENSITIVE DATA (do this first)

**Is any data in this project from patients, or from identifiable people?**  ☐ No  ☐ Yes

If **yes**, answer these before anything else. A "no" here is a problem to fix *now*, not
later:

- [ ] The data is pseudonymised or anonymised (no names, no patient IDs, no full dates)
- [ ] No identifying information sits in any filename
- [ ] No identifying data is in a shared cloud folder or a public git repository
- [ ] The re-identification key (if any) is stored separately, not with the data
- [ ] There is an ethics vote / data-use agreement for this data
- [ ] You know who your data protection officer is, and the handling is approved

> ⚠ **If any of the middle three are unticked, stop and fix them today** — identifying
> data in the open is the one problem that can't wait. See `clinical/`.

---

## Part 1 — BRONZE: is it set up? (this should be free)

**Structure**
- [ ] There is a clear folder for raw data, separate from processed data
- [ ] Raw data has not been edited by hand (it's the untouched original)
- [ ] There is a README file that explains what the project is
- [ ] There is a licence, or you know what licence the data will have
- [ ] Code and data are separated (code in git or a code/ folder, data elsewhere)

**Findability**
- [ ] Files have consistent, descriptive names (not "final_v2_REAL_final.xlsx")
- [ ] The naming follows a pattern (e.g. date_sample_type) — not ad hoc
- [ ] You can tell, from a filename alone, roughly what a file contains
- [ ] There is a table/sheet somewhere listing the samples and where each lives

**Count your Part 1 ticks: ____ / 9**

---

## Part 2 — SILVER: could someone else reuse it?

**Metadata**
- [ ] Each sample/measurement has its conditions recorded (treatment, timepoint, etc.)
- [ ] Standard terms are used where they exist (e.g. an organism name that matches a
      database, not free text) — or you note where none fits
- [ ] The metadata is in an open format (CSV/Excel/JSON), not locked inside a PDF
- [ ] Someone could match a data file to its metadata without asking you

**Provenance**
- [ ] The code/scripts that produced the results are saved
- [ ] The steps are numbered or ordered so the pipeline can be followed
- [ ] Software versions / environment are recorded somewhere
- [ ] Intermediate results are findable, not just the final figures

**Identifiers**
- [ ] The data has (or is planned to have) a repository accession or DOI
- [ ] There is a data management plan (DMP), even a short one

**Count your Part 2 ticks: ____ / 10**

---

## Part 3 — GOLD: is it a connected, reusable object?

- [ ] Code, data, and the paper (if any) point at each other (cross-linked IDs)
- [ ] Contributors are credited with ORCIDs
- [ ] The environment is pinned so the analysis re-runs (lockfile / container)
- [ ] Notebooks don't carry huge stored outputs (they're stripped / lean)
- [ ] The project could be packaged as an RO-Crate (a described, portable bundle)
- [ ] Another project has reused this project's structure or schema

**Count your Part 3 ticks: ____ / 6**

---

## Your score

| Tier | You have it if… | Your result |
|---|---|---|
| 🥉 **Bronze** | Part 0 clean (or N/A) **and** Part 1 ≥ 7/9 | ☐ |
| 🥈 **Silver** | Bronze **and** Part 2 ≥ 8/10 | ☐ |
| 🥇 **Gold** | Silver **and** Part 3 ≥ 4/6 | ☐ |

- **Not yet Bronze?** You're not behind — you're un-set-up. Bronze is mostly free: a
  README, a licence, separating raw data, consistent names. Fix Part 1 first.
- **Bronze but not Silver?** The gap is metadata and provenance — the things that let
  someone *else* use your data. This is the real bar.
- **Silver reaching for Gold?** Cross-link your identifiers and package an RO-Crate. See
  `for-AI/` and the RO-Crate template.

---

## What to fix first (write your top 3)

Look at your lowest-scoring section and pick the three easiest high-impact fixes:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

**The order that usually works:** Part 0 safety issues → a real README → separate & lock
raw data → the sample/metadata table → controlled vocabulary → identifiers.

---

*Then hand this filled-in sheet, plus your folder, to an AI with `STACK.md` (front door
§B) — it will do the fixes it safely can and hand you back the human-only gaps. This
checklist tells you where you stand; STACK.md helps you move.*
