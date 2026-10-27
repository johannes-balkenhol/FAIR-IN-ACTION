# Kickoff — paste this into an individual project chat

*Open a chat for ONE project (e.g. DECIDE_A03). Upload `STACK.md`,
`FAIR_ACTION_PLAN_SOP.md`, the tools (`agent/fair_gdpr_audit.py`,
`agent/prepare_project.sh`), and the project's tree + key metadata files. Then paste:*

```
This is a single project I want to make FAIR and GDPR-compliant and prepare
for deposition. Follow FAIR_ACTION_PLAN_SOP.md.

Project: <name>
Assay: <scRNA-seq | bulk/dual/triple-RNA-seq | PacBio | imaging | flow | proteomics | clinical>
Organisms: <list with roles — host/bacterium/phage/fungus>
Sensitivity: <open | pseudonymised | identifying>
Repository: <ArrayExpress+ENA | EGA | Zenodo | BioImage-Archive | PRIDE | FlowRepository>

Do this, in order:
1. AUDIT (read-only): run agent/fair_gdpr_audit.py on the project and tell me its
   current tier, the flags, and any GDPR signals. Change nothing yet.
2. PREPARE (additive, safe): run agent/prepare_project.sh <project> go — it creates
   only what is missing (project.yaml, README, metadata/, git, FAIR_GDPR_TODO.md)
   and never moves/renames/deletes anything.
3. FILL what you can infer from the project's own files: modality (from file types),
   organism, a one-line README, a PROPOSED licence. Mark unverifiable items TODO.
   Never invent ethics/consent numbers, accessions or DOIs.
4. Emit the ordered action list (Part 2) — only what's missing — each item tagged
   [auto] (you do it), [human] (I do it), or [check] (confirm before publish).
5. Do the [auto] items you safely can; hand me the [human] items with why each is needed.
6. Write the result to documents/planing/FAIR_ACTION_PLAN.md (and update FAIR_GDPR_TODO.md).

Reference: E-MTAB-17360 is my completed, correct scRNA-seq submission — use its shape
(13 biological characteristics, the multiplexing/library≠sample handling, the 10 named
protocols) as the template. For expression data, ArrayExpress is the target and it
brokers raw reads to ENA automatically.

Naming / reorganising: if the folder isn't the convention, PROPOSE the rename/moves as a
DRY-RUN list and wait for my OK — never rename-then-sync blind (it breaks analysis paths).
```

## The safety contract (for the AI)

- **Audit + fill = automatic.** **Create = additive only** (never overwrites existing files).
- **Move / rename / delete = preview-first, human-approved.** Never silent.
- **Never fabricate** identifiers, ethics numbers, consent scopes, accessions or DOIs —
  mark them `TODO` for a human.

## The one rule that makes projects comparable later (the knowledge graph)

**One stable ID per entity (sample/experiment), carried across projects (`samples.tsv`).**
It is the join key — without it there are no joins and no graph. Enforce it at capture.

## The workflow across chats

```
THIS chat (FAIR-in-action)          →  maintains the bundle: STACK.md, the SOP,
                                        the schemas, the tools, the RO-Crate target
        │  (rules + tools, human + machine + AI readable)
        ▼
each PROJECT chat                    →  AUDIT → PREPARE → FILL → REPORT on ONE project,
(DECIDE_A03, A04, A06, …)               emits + executes its action list, writes
                                        FAIR_ACTION_PLAN.md + FAIR_GDPR_TODO.md back
        │  (the doing)
        ▼
the PROJECT folder                   →  becomes FAIR + GDPR-compliant, deposited,
                                        RO-Crate-packaged — a clean node in the
                                        eventual consortium knowledge graph
```

**One bundle generates the rules and the tools. Each project chat applies them. The folder
ends FAIR.** That is the whole system, and it scales across all your projects without
redoing the thinking each time.
