# FAIR tiers — bronze / silver / gold

**Design rule: every check below is computable by `audit.py`. No judgement calls, no opinions.**
If a criterion cannot be checked by a script, it does not belong on this page.

---

## 🥉 Bronze — *the project is findable and legally reusable*

| # | Check | How it is checked |
|---|---|---|
| B1 | Standard folder structure (`data/{raw,primary,processed}`, `docs/`, `code/`) | path test |
| B2 | `project.yaml` present and parses against `core_model.yaml` | schema parse |
| B3 | Raw data locked (`chmod a-w`) and checksummed | `checksums.txt` exists, spot-check |
| B4 | All `source: auto` fields populated (extractors have run) | field count |
| B5 | All `source: project` fields populated | field count |
| B6 | `LICENSE` present | file test |
| B7 | `README.md` with a data-availability section | regex |
| B8 | Code in a public git repository | remote reachable |

**Bronze is free.** Everything in it is either scaffolded by `init_project.sh` or extracted automatically. A project that is not bronze is not neglected — it is unscaffolded.

---

## 🥈 Silver — *a human has supplied what only a human knows, and it validates*

| # | Check | How it is checked |
|---|---|---|
| S1 | All `source: human` required fields filled (gap-sheet returned and merged) | field count |
| S2 | Every ontology term resolves to a real CURIE | ontology lookup |
| S3 | No free text where a controlled vocabulary is declared | enum test |
| S4 | Every organism has a `role` (host / pathogen / …) | schema test |
| S5 | Data has a repository **accession** | accession resolves |
| S6 | Code has a persistent **DOI** (Zenodo) | DOI resolves |
| S7 | `CITATION.cff` present and DOI-populated | parse |
| S8 | Repository export validates (SDRF/IDF passes the checker) | `validate.py --export` |
| S9 | DMP exists | file test |

**Silver is the real bar.** It is the point at which someone else could reuse the data without emailing you.

---

## 🥇 Gold — *the research object is machine-traversable and has been reused*

| # | Check | How it is checked |
|---|---|---|
| G1 | **Cross-linked identifiers**: code DOI → data accession → paper DOI, *and back* | fetch each record, assert `related_identifiers` |
| G2 | **ORCIDs complete** on the Zenodo record (not the GitHub username autofill) | fetch record, assert ORCID present per author |
| G3 | Environment pinned and reproducible (lockfile / container) | file test |
| G4 | Notebook outputs stripped; repo lean | `nbstripout --verify`, repo size |
| G5 | Analysis reruns end-to-end from raw + code alone | CI run |
| G6 | **Reused**: the model/config has been inherited by a second project | config lineage |

**G1 and G2 are the ones everyone skips**, and they are the cheapest gold points available — Zenodo mints the DOI automatically, but autofills the author as your GitHub username and leaves `related_identifiers` empty. Fixing that is ten minutes and converts a pile of separate records into an actual research object. **That is the "I" in FAIR, and it is the only criterion here that no amount of tidy READMEs will earn you.**

**G6 is the business case.** A model that has been reused has demonstrably paid for itself; one that hasn't is still a hypothesis.

---

## Not on this page (deliberately)

- Anything requiring judgement ("is the README *good*?")
- Anything about scientific quality — FAIR is orthogonal to whether the experiment was any good
- Anything a curator must decide

## Mapping to external rubrics

Not yet done. If cRDM/DFG requires alignment to **F-UJI** or **FAIRsharing**, these tiers should be *mapped* to them, not replaced by them — the tiers exist to be actionable on a Tuesday afternoon, which generic FAIR scores are not.
