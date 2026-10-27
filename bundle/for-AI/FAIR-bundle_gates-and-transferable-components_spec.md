---
title: FAIR bundle — Gates & transferable-components spec (grant-aligned)
home: Projects/FAIR-in-action/bundle/for-AI/
status: spec-for-build
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-19
source: BMFTR grant briefing (gate model, transferable-component test, standards, verified citations)
supersedes: the G-labels used in FAIR-bundle-vnext_blueprint + cRDM_Gates_register (see §6)
---

# Gates & transferable components — bundle spec

Canonical, grant-aligned. This is the "control" layer of the FAIR-in-action bundle: the gates, the test for what may leave the lab as a reusable component, the standards to dock onto, and the record the gates must write.

## 1. The three gates — each matures in three layers

Every gate grows: **Procedure (SOP) → Agreement (legal basis) → Control (software that enforces the procedure and logs the decision).** A site can enter at any layer. **Interim rule where no Control exists: the software goes to the data — the data do not move, and only a quality / error report comes back.**

| Gate | Controls | Procedure (SOP) | Agreement (legal) | Control (software + log) |
|---|---|---|---|---|
| **G0 Ingress** | arrival, as far upstream as possible (at the instrument) | class, legal basis, consent scope captured on arrival → holding area | ethics vote, consent scope, record of processing | completeness + metadata + pseudonymisation check before anything moves |
| **G1 Sharing** | with whom data may be shared, where an analysis may run | who/where rules; capture which pipeline version ran on which inputs | data-use / sharing agreement | access logged; provenance of pipeline-version × inputs recorded |
| **G2 Release** | what leaves as result, deposit, or return to the treating physician | output review: decision, justification, and **what was *not* checked** | EHDS **Art. 73(2)** output control | release record written; after release the result is no longer bound to the environment |

## 2. Test for a "transferable component"

A component is transferable **only** if it has: **(a) a contract** (schema, API, or profile), **(b) an implementation**, **(c) a conformance test a second site can run itself.** Without (c) it is just code that runs here.

**Valid handover forms** (anything shipped must be one of these):
1. container image + its configuration
2. versioned schema + machine-readable validator
3. specification + its SOP
4. workflows as CWL / Nextflow definitions with their images, in a public workflow registry
5. checks (release, audit) as scripts that run as a workflow
6. documents: SOPs, agreements, DMP + needs-assessment templates, minimum-requirements catalogue

**Never ship as a component** (the environment, not a part): storage, network zones & firewalling, the IdP install, HPC/GPU, the Nextcloud / eLabFTW / GitLab instances, the container platform.

## 3. Standards to dock onto (be conformant, don't subordinate the bundle to them)

- **Packaging:** RO-Crate; **Five Safes RO-Crate** on the clinical route, **ARC** for omics.
- **TRE-FX** (DARE UK) — reference implementation for "analysis to the data" between TREs (Submission / TRE-Polling / Controlled layers). Reference it as a *family*, don't adopt it as our architecture.
- **ACRO / SACRO** — established output-checking / disclosure-control family, semi-automatic inside the analysis call. This is where the release-check is built.
- **HealthDCAT-AP** — dataset description.
- **Implementing Reg (EU) 2026/2098** (18.09.2026): **27 minimum metadata elements** for dataset descriptions under **EHDS Art. 77(4)**, HealthDCAT-AP as frame, applicable **26.03.2029**. *(Pull the official title from EUR-Lex before citing in running text.)*
- **EHDS = Reg (EU) 2025/327:** Art. 73(1)(e) logs ≥ 1 year · 73(2) only non-personal results downloadable · 73(3) periodic third-party audit · 73(5) Commission specifications from 2029 · 75 HealthData@EU · 77 catalogue description · 78 data-quality label.
- **Domain schemas:** FHIR (clinical), REMBI / OME-NGFF (imaging), MAGE-TAB (genomics), MIFlowCyt (flow cytometry); **MII core dataset** for care data, **NFDI4Health** for the research route.

## 4. The decision / audit record (what the gates write)

A single schema, written at each gate, retained **≥ 1 year** (Art. 73(1)(e)):

`gate · dataset_or_result_id · actor (role) · timestamp · criteria_version · decision {yes | no | ask-human} · justification · what_stayed_unchecked · downstream_binding` (G2: result = unbound).

This is the **release-gate record** the self-report named as the single biggest missing thing — the audit reaches "deposition-ready", this records the go/no-go and carries it with the data.

## 5. What the bundle therefore ships (build list)

1. **A validator per schema**, versioned — the conformance test, not just the schema.
2. **Every delivery in one of the six handover forms** (§2), or it does not count as a component.
3. **Gate SOP templates**, split in the three layers (§1), so a site can start at any maturity.
4. **A HealthDCAT-AP crosswalk** (27 elements / Art. 77(4)) — then the EHDS catalogue description falls out as a by-product.
5. **The release-check in the ACRO/SACRO family**, semi-automatic in the analysis call, measured against the human baseline: *false-negatives = safety-critical · false-positives = usability · review effort per exported result = operational metric.*
6. **The decision/audit-record schema** (§4).
7. **Workflows + images published to a public registry**; acceptance = runs unchanged at a second site.

## 6. Reconciliation

Earlier bundle docs used **G1 "processing" / G2 "egress"**. Canonical (this spec, from the grant) is **G1 Sharing / G2 Release**, with **G0 Ingress** unchanged. On your word I propagate the corrected labels across `FAIR-bundle-vnext_blueprint`, `cRDM_Gates_register`, and the forthcoming BMFTR realization doc so all three read the same.
