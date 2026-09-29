# Project intake — what does this project already have?

*Fill this in (or have the AI fill it from the connected folder) BEFORE making a FAIR
action plan. The bundle adapts to your project using what already exists — this intake is
how it learns what that is, so it doesn't re-ask what your files already answer.*

Project: _______________   Assay: _______________   Chat/person doing intake: __________

## 1. Structure — what's the folder like now?
- [ ] paste the folder tree (`tree -L 3` or a listing)
- existing structure: ☐ already follows a skeleton  ☐ partial  ☐ ad hoc / messy
- notes: _______________

## 2. Metadata — in what forms does it already exist?
- [ ] `.sdrf` / `.idf` (structured) — where: _______________
- [ ] a sample sheet — format: ☐ tsv/csv ☐ xlsx ☐ **PDF** ☐ docx
- [ ] `samples.tsv` / config with sample info
- [ ] unstructured notes / a metadata TODO
- [ ] **metadata inside the experimental protocol** (see §3)
- what's the sample ID scheme? _______________

## 3. Experimental protocol — the richest metadata source
- [ ] a methods / protocol document — format: ☐ docx ☐ md ☐ pdf
- [ ] an **ELN entry** — link: _______________
- [ ] an **ELN export** (.eln file)
- the protocol already contains (tick what's in it): ☐ organism(s) ☐ treatment/condition
      ☐ timepoints ☐ library prep ☐ instrument ☐ reference genome ☐ dissociation/prep
- → these should be EXTRACTED, not re-asked

## 4. Supporting material
- [ ] scripts / pipeline — where: _______________
- [ ] `environment.yml` / lockfile (reproducibility)
- [ ] reports / current results
- [ ] a project plan
- [ ] a manuscript / draft (often has the study description ready to reuse)
- [ ] checksums (md5)

## 5. Sensitivity
- any patient / identifying data? ☐ no ☐ yes → go to `clinical/` first
- ethics / consent / DTA present? _______________

## 6. What's ONLY in someone's head?
*The genuinely missing human input — the short list that isn't in any file:*
- _______________
- _______________

---

**Result:** the FAIR action plan asks the human ONLY for §6. Everything in §1–5 is adapted
from what the project already has. That's the bundle fitting the project, not the reverse.
