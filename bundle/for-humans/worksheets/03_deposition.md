# Worksheet 3 — deposition and identifiers

*Making the data findable and citable. The half that is nearly free, and the half that
is not.*

## Code — nearly free, do it always
1. Put the analysis code in a public git repository.
2. Link the repository to Zenodo (or your institutional equivalent) — once.
3. Make a release with a version tag → a **DOI** is minted automatically.
4. **Fix the auto-generated record**: real author names, ORCIDs, a proper title. The
   automatic version usually credits a username. This step is the one everyone skips.

## Data — the expensive half
1. Prepare the metadata (worksheet 2) in the format your repository wants.
2. Submit through the repository's portal.
3. A curator loop may take days — build it into the timeline; do not leave it to the
   week before submission.
4. Receive the **accession**.

## The gold move — cross-link
Make the identifiers point at each other:
- the code DOI → names the data accession
- the data accession → names the paper and the code
- the paper → names both

Separate identifiers are a start. A **traversable graph** — where a machine can go from
paper to data to code and back — is the "I" (Interoperable) in FAIR, and it is what turns
a pile of files into a research object. Ten minutes' work; the difference between silver
and gold.

## Sensitive data is still FAIR
If your data is restricted or identifying, it does **not** go to an open repository — it
goes to a controlled-access one (e.g. EGA), and the access conditions are documented.
Controlled data with explicit, documented access rules is exemplary FAIR. "FAIR" is not
"open".

---

Done and cross-linked, with a pinned environment and the setup reused by a second
project? That is **gold**.
