<!--
  cRDM / FAIR-in-action — README template for MULTI-CENTER, MULTI-MODAL data projects
  How to use: copy to your project root as README.md, fill every <…> placeholder,
  delete the modality blocks you don't use, keep the structure. Lines in <!-- --> are
  guidance and can be removed. One home per thing; raw data is read-only; link, don't copy.
-->

# <Project title>

<One-sentence plain description a stranger understands: organism/material, question, data types.>

| | |
|---|---|
| **Project ID** | `<YY-N_Acronym>` <!-- the one ID used everywhere: files, folders, metadata, repo --> |
| **Consortium / funder** | `<e.g. SFB 1583 DECIDE · DFG>` / `<grant no.>` |
| **PI(s) · data steward** | `<name>` · `<name, ORCID>` |
| **Centers involved** | `<center A (role) · center B (role)>` <!-- multi-center: name each + what it contributes --> |
| **Status** | `<planning · collecting · analysis · deposition-ready · published>` |
| **FAIR tier** | `<bronze / silver / gold>` (last audit `<date>`) |
| **Human / personal data?** | `<yes/no>` → <!-- if yes, the GDPR + gates section below is mandatory --> |

---

## 1. Data at a glance (modalities)

<!-- One row per modality. This is the multi-modal map: not every rule applies to every row. -->

| Modality | Samples | Raw location (canonical) | Standard | Repository (target) | Access |
|---|---|---|---|---|---|
| `<scRNA-seq>` | `<n>` | `<center/host:path>` | `<IDF/SDRF>` | `<ArrayExpress/EGA>` | `<open/controlled>` |
| `<spatial imaging>` | `<n>` | `<…>` | `<REMBI/OME-NGFF>` | `<BioImage Archive>` | `<open>` |
| `<clinical>` | `<n>` | `<…>` | `<FHIR>` | `<NFDI4Health/EGA>` | `<controlled>` |

**Canonical copy rule:** `<which host holds the authoritative raw data; how other sites mirror; sync direction>`. Raw is **read-only**.

---

## 2. Folder structure

```
<project_id>/
├── README.md                 # this file
├── DMP.(md/pdf)              # data management plan
├── LICENSE                   # data licence (+ note code licence)
├── data/
│   ├── raw_data/             # read-only; or a link to the source host
│   ├── primary_data/         # catalogued, QC'd
│   ├── secondary_data/       # analysis outputs
│   └── meta_data/            # metadata sheets (per modality) + controlled-vocab version
├── documents/                # protocol, ELN exports, decisions
├── scripts/ · analysis/ · results/   # code + workflows (CWL where portable)
└── provenance/               # RO-Crate / checksums / run logs
```

<!-- Mirror this structure across centers so a dataset looks the same everywhere. -->

---

## 3. Metadata & vocabularies

- **Schema:** `<link to the metadata schema / the HTML metadata app that writes it>` — the app is the source of truth; sheets in `data/meta_data/` are its exports.
- **Per-modality standard:** `<scRNA-seq → MAGE-TAB IDF/SDRF; imaging → REMBI; clinical → FHIR>`.
- **Controlled vocabularies (bound, not free text):** `<EFO, CL, UBERON, NCBITaxon, MONDO, PATO, FBbi, SNOMED CT …>` — version `<date>`.
- **One identifier everywhere:** `<the ID pattern; where it is minted — at the instrument, not afterwards>`.
- **Fixity:** SHA-256 for every raw file (`provenance/checksums.sha256`).

---

## 4. Access, GDPR & the gates  <!-- delete if no human/personal data -->

- **Legal basis:** ethics vote `<no.>` · consent scope `<secondary use? sharing? deposition?>` · DPIA `<status>` · record of processing `<status>`.
- **Pseudonymisation:** at source; key stays at `<hospital/center>`; no names/initials/dates in file or folder names.
- **Two-tier access:** `<open layer (e.g. imaging)>` vs `<controlled layer (e.g. clinical) — SPE/controlled-access repo>`.
- **Release control (gates):**
  - **G0 ingress** — legal basis + consent + pseudonymisation confirmed before data move. `<date/owner>`
  - **G1 processing** — secure, in-place; access logged; provenance captured. `<where>`
  - **G2 egress** — go/no-go recorded; metadata travels with the data; then deposit. `<decision log link>`

---

## 5. Reproduce it (analysis)

- **Pipeline:** `<link to scripts/CWL workflow>` — `<qc → … → result>`.
- **Environment:** `<container / env file>` · **compute:** `<HPC/cloud>`.
- **Inputs:** metadata sheet(s) from §3 → `<how they feed the pipeline>`.

---

## 6. Publication & reuse

- **Deposited:** `<repository>` · accession `<ID/DOI>` · `<open / controlled>`.
- **Licence:** data `<CC-BY-4.0>` · code `<MIT>`.
- **Cite as:** `<citation / CITATION.cff>`.
- **Retention:** raw + primary `<10 y post-publication (DFG)>`.
- **Versioned releases:** `<if the dataset grows: release vN + changelog, each citable>`.

---

## 7. Contacts & links

Data steward `<name, email>` · helpdesk `<cRDM helpdesk>` · ELN `<link>` · Nextcloud `<link>` · Git `<link>` · DMP `<link>`.

<!-- FAIR self-assessment: run the evaluate-existing-project tool and paste the tier + date in the header. -->
