# Worksheet 1 — project setup

*Fill this in before collecting data. Fifteen minutes now saves weeks later. Keep it in
the project folder as `docs/project_setup.md` — it is the answer to "why is this set up
this way?"*

Project name: _______________     Date: _______________     You: _______________

---

## 1. Domain and unit of study
Which `domains/` page applies? _______________
(none fits → copy `domains/_TEMPLATE.md` and fill it in first)

Unit of study (what gets a stable ID): _______________

## 2. Sensitivity — decide this FIRST
- [ ] open   - [ ] restricted   - [ ] pseudonymised   - [ ] identifying

Legal basis if not open: _______________

**This governs everything below.** If identifying/pseudonymised: no cloud sync without a
documented basis; deposition is controlled-access, not open.

## 3. Licence
Data licence: _______________ (e.g. CC-BY-4.0, or "restricted — see basis above")
Code licence: _______________ (e.g. MIT)

*Data with no licence is legally unreusable, however open it looks.*

## 4. People
| Role | Name | ORCID |
|---|---|---|
| Lead / PI | | |
| Data steward (answers metadata questions) | | |
| Contributors | | |

*If no data steward is named, nobody answers metadata questions, and they don't get answered.*

## 5. Structure — create this now
```
PROJECT/
├── data/
│   ├── raw/         immutable — lock read-only, checksum, NEVER edit
│   ├── primary/     first processed form (usually what gets deposited)
│   └── processed/   analysis outputs, freely regenerable
├── code/
├── metadata/
├── docs/            this worksheet, the DMP, the SOPs
└── results/
```

Lock and checksum the raw data as soon as it lands:
```
cd data/raw && chmod -R a-w . && find . -type f ! -name checksums.txt -exec md5sum {} + > checksums.txt
```

## 6. Repository — choose now, not at publication
Target: _______________     Identifier type: _______________ (accession / DOI)

*The repository determines which metadata you must collect. Choosing it late means
collecting it late — badly.*

---

Done? You are **bronze**: structured, licensed, checksummed, and set up. That is free —
it is setup, not effort. Now go to worksheet 2.
