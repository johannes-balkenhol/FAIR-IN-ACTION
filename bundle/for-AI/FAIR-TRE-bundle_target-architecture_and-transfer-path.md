---
title: FAIR-TRE bundle — target architecture & transfer path (platform-agnostic)
home: Projects/FAIR-in-action/bundle/for-AI/  (extends ARCHITECTURE.md)
status: architecture-vision
owner_role: Data Steward (Co-Lead)
owner_person: Johannes / Hamidreza
date: 2026-10-22
source: VRC architecture figures (services+gates · manifest wiring · three-case current state)
relates_to: FAIR-bundle_gates-spec · FAIR-bundle-vnext_blueprint · BMFTR grant O1–O4
---

# FAIR-TRE bundle — target architecture & transfer path

**The principle.** The bundle is a set of **transferable components** (each with a contract + an implementation + a conformance test). It runs *today* as plain folders, scripts and SOPs, and it ports **unchanged** onto a full TRE/SPE platform like the VRC below. The platform is what a site *installs* (non-transferable); the components are what the bundle *carries*. "Platform-agnostic" and "transferable to a platform like this" are the same statement read in two directions.

**One rule holds the whole thing together:** the project **manifest = `ro-crate-metadata.json`**, written once at approval, read by every service, and the thing the gates act on. Each service writes its own part; at G2 the manifest *is* the research object. Nobody edits it by hand — one validating library does, and that library is itself a transferable component.

---

## 1. Reference platform (the VRC) — what we prepare for

| Layer | What it is | Gate role |
|---|---|---|
| **Identity (IdP)** | OIDC + SAML federated into DFN-AAI; 2FA; roles + project membership arrive as token claims from the manifest; no local accounts | the single entry point |
| **Firewalled zone** | no route in from outside; **no outbound network from compute containers** | makes "analysis to the data" enforceable |
| **Manifest** | `ro-crate-metadata.json` — the spine every service reads and writes its part of | what every gate acts on |
| **DATA · Nextcloud** | the 10→20→30→40 folder-state machine (§2) | G0/G1/G2 enforced in folder permissions |
| **COMPUTATION** | JupyterHub (raw read-only mount, results only to `outputs/`, no egress) · GitLab (code, images, pipeline defs) · **Windmill** (every check is a containerised CWL/Nextflow workflow — the checks transfer, the engine does not) · storage/backup (versioned, checksum-verified) | G1 provenance |
| **DOCUMENTATION · METADATA** | eLabFTW (protocol + release request; entry locked + RFC-3161 timestamped) · metadata collection app (FHIR/biological/technical → folder + manifest at capture) · schema catalogue + validators (a dataset passes/fails without human judgement) · HealthDCAT-AP crosswalk | G0 green-validator; G2 locked-doc precondition |
| **Gate service** | the decision layer — **does not exist yet; it is what the project builds.** Trigger from a folder event or API → checks run as workflows → decision appended to the manifest → copy into `40_released`. The only component allowed to write `40_released`. | G0 · G1 · G2 |
| **Audit store** | one store, three sources (app logs · IdP events · gate decision records); append-only; **≥ 1 year** (EHDS Art. 73(1)(e)); read access separated so the Art. 73(3) third-party audit has something to read | evidence |
| **Egress** | only through G2 → other centres, or repositories (domain archive · NFDI4Health LDH · controlled-access); the manifest travels as the research object | G2 |

---

## 2. The folder-state machine — where a gate is physically enforced

```
instrument ──G0──► 10_incoming ─────► 20_working ──G1──► 30_release-requested ──G2──► 40_released
(metadata at      (holding: complete-  (raw READ-ONLY,     (dropping a file here      (ONLY the gate
 recording)        ness+metadata+       derived writable;    IS the request; put-in     service may write;
                   pseudonymisation      membership from      not take-out)              group reads)
                   verified; write,      the manifest)
                   not read across)
```

Enforcement lives in **the folder permission, the network and the token** — not in a document. The **write monopoly on `40_released`** is what makes G2 non-optional: there is no second path into that folder. This machine runs on plain folders + ACLs **today**, with no platform — that is the platform-agnostic on-ramp.

---

## 3. The manifest is the spine — who writes which part

| Manifest part | Written by |
|---|---|
| project context (members, roles, permitted resources, usage + release conditions) | project-context service |
| dataset descriptors (clinical FHIR, biological, technical, against controlled vocabularies) | metadata collection app |
| provenance actions (inputs + checksums, parameters, outputs, image digest, commit) | JupyterHub run · Windmill |
| documentation (eLabFTW entry id, locked + RFC-3161 timestamped) | eLabFTW |
| code (commit, image digest, release tag, DOI per release) | GitLab |
| gate decisions (who, when, criteria version, grounds, what stayed unchecked) | gate service |

Packaging at G2 is a **validation step, not an export** — because every service already wrote into the manifest as it worked.

---

## 4. Component → service → handover form (the platform-agnostic map)

This is the table that makes the bundle portable: each component names the service it lands on *and* the form it travels in (one of the six from the gates spec), with a conformance test a second site runs itself.

| Bundle component | Lands on | Handover form | Conformance test |
|---|---|---|---|
| Metadata schema(s) + validator | metadata app · schema catalogue | versioned schema + machine validator | a foreign dataset passes/fails without a human |
| Metadata collection app | DOCUMENTATION layer | container image + config | writes a valid manifest part on a second site |
| Folder-state machine (10/20/30/40 + ACLs) | Nextcloud (or plain folders) | spec + SOP | permissions deny the forbidden move |
| Manifest profile + validating library | the spine | versioned schema + validator | round-trips a crate; rejects a hand-edit |
| Gate SOPs (3 layers: procedure/agreement/control) | gate service | documents + spec | a site can enter at any layer |
| Release check (ACRO/SACRO) | Windmill | check-as-workflow | error rates measured vs human baseline |
| Analysis pipelines | JupyterHub · Windmill · GitLab | CWL/Nextflow + images in a public registry | runs unchanged at the second site |
| HealthDCAT-AP crosswalk | metadata layer | spec + script | emits the 27 Art. 77(4) elements |
| Decision/audit-record schema | audit store | versioned schema | a third party can read the log |

**Never shipped as a component** (the environment, which each site installs): the IdP, Nextcloud/eLabFTW/GitLab/JupyterHub instances, storage, network zones + firewalling, HPC/GPU, Windmill the engine, the container platform.

---

## 5. Enforcement ladder

- **Enforced from day one, at no cost:** read-only mounts · no egress from compute · write monopoly on `40_released` · public links off · 2FA at the provider.
- **Staged, per gate and per output class:** *advisory* (the check runs, nobody is stopped) → *required but overridable* (the override is recorded with its reason) → *blocking*.

A site adopts the ladder at whatever rung it can sustain — the bundle does not require the top rung to be useful.

---

## 6. Transfer path — porting the bundle onto a platform like this

1. **Install the environment** (§4 "never shipped") — the site's own IdP, Nextcloud, JupyterHub, GitLab, eLabFTW, Windmill, storage, and a gate service. Non-transferable by design.
2. **Carry the components** (§4 table) in their handover forms.
3. **Acceptance** = each component's conformance test passes on the new site, and at least one workflow runs unchanged at the second site. Until then it is "code that runs here", not a component.

The manifest profile + validating library is the first thing to port: everything else hangs off it.

---

## 7. Where we stand (the three-case view)

Across FlowSep, ALM (Löffler) and the third (data-integration-centre) case, read the columns downwards and the picture is the same: the **procedure** layer is largely in place and was built **without funding**; the **agreement** layer is partial; the **control** layer is **absent everywhere**. That absence — not the infrastructure — is what the project builds. What is missing is identical in both live cases: **a recorded, checkable release decision**, plus, for the clinical case, **an approved environment to make it in**. That is grant objective **O1**, and the gate service in §1 is its implementation.

---

## 8. What to put in the bundle now (to "prepare for this")

1. **This architecture** as `ARCHITECTURE.md` — the target every component aims at.
2. **The folder-state-machine spec** (10/20/30/40 + the permission rules) as a template a site applies on **plain folders today** — the platform-agnostic on-ramp, usable before any TRE exists.
3. **The manifest profile + validating library** — the one component everything else depends on.
4. **Every other component kept in a handover form + conformance test** (§4), so the day a platform like the VRC exists, the bundle moves onto it without a rewrite.
