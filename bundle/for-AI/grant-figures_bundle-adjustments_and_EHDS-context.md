---
title: Grant figures → FAIR-in-action + GDPR bundle adjustments (and the EHDS/national context they supply)
home: Projects/FAIR-in-action/bundle/for-AI/ + a new compliance/ note
status: adjustment-note
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-25
source: BMFTR grant conceptual figures (FAIR↔environment map · service-by-service architecture · abstract flow · network & state-of-the-art)
relates_to: FAIR-TRE-bundle_target-architecture · FAIR-bundle_gates-spec · FAIR-bundle-vnext_blueprint · README_TEMPLATE
---

# What the grant figures change in the bundle

Most of the figures confirm the architecture we already wrote. Four of them add or sharpen things worth folding in — and they fall mainly on the **GDPR/compliance** side, which is what the figures are strongest on.

## 0. The one principle to put at the front

> **Accessible ≠ open.** "Accessible" means the **conditions of access are stated and machine-readable** — which is exactly why FAIR and a locked environment are **not in conflict**. A dataset can be fully FAIR and never leave the SPE.

And the terminology the figures settle: **TRE = SPE = SDE** (trusted research environment = secure processing environment = secure data environment). For a German/EU audience the legal term is **SPE**. Put this principle at the top of the README template, the GDPR note, and the architecture intro — it is the sentence that resolves the "FAIR vs security" tension the abstract opens with (8% of papers claim data availability, 2% deliver).

## 1. The spine, as one sentence (adopt as the bundle's narrative)

> The DMP says **what will be recorded** → metadata are captured against a **schema + controlled vocabulary** and checked by a **validator** — that check **is G0** → the data **rest in the environment and do not move** → the analysis arrives as a **container run by a workflow**, and **G1** records which version ran on what → data, code, documentation and provenance are bundled as an **RO-Crate** (an **ARC** for omics) → at **G2** the release decision is **written into that same package** → its description is **crosswalked to HealthDCAT-AP** and appears in the **EHDS catalogue**.

"One source, several targets." This is the clean through-line for the bundle's `START_HERE` / overview.

## 2. New content to ADD — the EHDS & national compliance context

This is the genuinely new material the figures supply, and it belongs in the GDPR-compliance side of the bundle (suggest a new `bundle/compliance/EHDS-and-national-context.md`).

**European frame — EHDS, Regulation (EU) 2025/327 (applies 26 Mar 2029):**
- **SPE mandatory** for secondary use; **only reviewed results may leave** (Art. 73(2)).
- **Identifiable logs ≥ 1 year** + **periodic third-party audit** (Art. 73(1)(e), 73(3)).
- **Dataset catalogue:** 27 minimum metadata elements, HealthDCAT-AP, **Art. 77** with Implementing Reg (EU) 2026/2098; **quality label Art. 78**.
- **Health Data Access Bodies** — one+ per member state; TEHDAS2 supplies the technical spec.

**National — what exists in Germany today:**
- **MII / NUM** — the health research data infrastructure: the **core dataset in FHIR**, the **broad consent**, the **use-and-access governance**.
- **FDPG** — the national portal: feasibility query across sites → data request → contract. **The known bottleneck** (several months to a specified project).
- **NFDI4Health** — the *other* door, for study/cohort data (not care data): study hub for descriptions, local data hubs for controlled sharing.

**Local — who holds and operates:**
- **Use-and-Access Committee** (approves a project, keeps authority ~1 month) · **Trusted Third Party** (pseudonymous linkage) · **DIZ / Health Data Platform** (integrates care data into the FHIR core dataset; controlled ingress/egress; **not interactive**) · **SMI** (hosts: servers, container platform, network zones, security, monitoring, backup) · **cRDM** (the research side: schemas, procedures, stewardship, the VRC pilot).

**Two routes, and where they split** (put in the architecture's egress section):
- **Clinical route (care data):** cohort found in FDPG → UAC approves → DIZ extracts from the core dataset → TTP pseudonymises → processing in the SPE → results leave through release control.
- **Research route (everything not in the core dataset — imaging, flow, omics):** described in the NFDI4Health study hub; controlled part in a local data hub under a DUA; open part in a domain repository.
- The research object keeps the two halves **linked through the manifest** — the open part in a domain repo, the controlled part under agreement.

## 3. Small corrections to the architecture doc

- **Workflow engines:** add **Snakemake** and **"tailored apps"** (we had CWL/Nextflow only).
- **Services:** add **EuroOffice · Talk · Deck** (editing, communication, task boards) and name **"Schema catalogue + DMP templates"** as its own service (controlled vocabularies, project profiles).
- **Output checking:** name the **ACRO / SACRO** family explicitly on the boundary (already in the gates spec — keep the architecture consistent with it).
- **Application profile:** add the definition — *a schema tailored to one domain; HealthDCAT-AP is literally that word.* Put it in the schema layer and the applicability matrix.

## 4. The acceptance criterion, made explicit

From the abstract figure: **a component counts as delivered once it runs unchanged at a second centre, and the gates are adapted per use case.** This is the (c) "conformance test a second site runs itself" from the gates spec — state it the same way in the architecture's transfer path.

## 5. "What is still missing" = the bundle's build backlog (identical across figures)

1. **The interactive environment** — a place where several centres work on sensitive data that stay in place (the pilot does non-sensitive only).
2. **One account per researcher** — federated identity, roles carried from one project description into every service (the condition for extending the pilot).
3. **The recorded release decision** — output checking exists for tabular results, not for imaging or high-dimensional molecular output; today every check is a person whose reasoning is not retained.
4. **A research object for the rest** — the core dataset is the semantic model for care data; everything outside it needs an object carrying documentation, provenance and vocabulary with the data.
5. **The route into the EHDS catalogue** — the crosswalk, so the Art. 77 description falls out of metadata already carried rather than being written again in 2029.

Items 2–4 are grant O3/O1/O2 and the self-report's top bottlenecks — the figures just confirm the priority.

## 6. Where each change lands

| Change | Bundle file |
|---|---|
| "Accessible ≠ open" + TRE=SPE=SDE | README_TEMPLATE · ARCHITECTURE intro · new compliance note |
| EHDS + national + local context | **new** `bundle/compliance/EHDS-and-national-context.md` |
| Two routes (clinical/research) + manifest link | ARCHITECTURE (egress) · compliance note |
| Application-profile + HealthDCAT-AP crosswalk | applicability matrix · schema layer |
| Snakemake, tailored apps, EuroOffice/Talk/Deck, schema-catalogue service | ARCHITECTURE §1 |
| Acceptance = runs unchanged at a 2nd centre | gates spec §2 (keep) · ARCHITECTURE transfer path |
| "What's missing" backlog | self-report bottlenecks · blueprint build order |

---

**Offer:** on your word I apply these as edits to `ARCHITECTURE`, the gates spec, and the applicability matrix, and split §2 out as the new `compliance/EHDS-and-national-context.md` so the GDPR side of the bundle has its own grounded reference.
