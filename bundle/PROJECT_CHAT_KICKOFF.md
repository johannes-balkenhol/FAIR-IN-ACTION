# Kickoff — paste this into an individual project chat

*Open a chat for ONE project (e.g. DECIDE_A03). Upload `STACK.md`,
`FAIR_ACTION_PLAN_SOP.md`, and the project's tree + key metadata files. Then paste:*

```
This is a single DECIDE project I want to make FAIR and GDPR-compliant and prepare
for deposition. Follow FAIR_ACTION_PLAN_SOP.md.

Project: DECIDE_<subproject>_<topic>
Assay: <scRNA-seq | bulk/dual/triple-RNA-seq | PacBio | imaging | clinical>
Organisms: <list with roles — host/bacterium/phage/fungus>
Sensitivity: <open | pseudonymised | identifying>
Repository: <ArrayExpress+ENA | EGA | Zenodo | BioImage-Archive>

Do this:
1. Assess the project (Part 1) and tell me its current tier.
2. Emit the ordered action list (Part 2) — only what's missing — with each item
   tagged [auto] (you do it), [human] (I do it), or [check] (confirm before publish).
3. Do the [auto] items you safely can from the files I gave you.
4. Hand me the [human] items as a short list, each with why it's needed.
5. Write the result to documents/planing/FAIR_ACTION_PLAN.md.

Reference: E-MTAB-17360 is my completed, correct scRNA-seq submission — use its shape
(13 biological characteristics, the multiplexing/library≠sample handling, the 10 named
protocols) as the template. For expression data, ArrayExpress is the target and it
brokers raw reads to ENA automatically.

Naming: if the folder isn't DECIDE_<subproject>_<topic>, propose the rename but warn me
to dry-run rsync first — never rename-then-sync blind.
```

## The workflow across chats

```
THIS chat (FAIR-in-action)          →  generates the bundle: STACK.md, the SOP,
                                        the schemas, the RO-Crate target
        │  (rules, human + machine readable)
        ▼
each PROJECT chat                    →  runs FAIR_ACTION_PLAN_SOP.md on ONE project,
(DECIDE_A03, A04, A06, …)               emits + executes its action list, writes
                                        FAIR_ACTION_PLAN.md back into the project
        │  (the doing)
        ▼
the PROJECT folder                   →  becomes FAIR + GDPR-compliant, deposited,
                                        RO-Crate-packaged — a clean node in the
                                        eventual consortium knowledge graph
```

**One bundle generates the rules. Each project chat applies them. The folder ends FAIR.**
That is the whole system, and it's what makes it scale across all your DECIDE projects
without redoing the thinking each time.
