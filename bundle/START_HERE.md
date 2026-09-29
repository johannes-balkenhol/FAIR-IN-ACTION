# START HERE — FAIR in action

**v1.8 · 2026-09-29**

*You were given this bundle to make a research project FAIR- and GDPR-compliant — the easy
way, whether you're a student with no training or an AI assistant. Read the line that
matches you and go.*

---

## → I am a STUDENT / researcher (a person)

1. Open **`handout/RDM_handout_v3.docx`** — the whole standard on 1–2 pages. Read it once.
2. Open **`HOW_TO_USE.md`** — it shows exactly what to do, with a real worked example.
3. To actually do the work, you have two options:
   - **With an AI (easiest):** open a chat with Claude or ChatGPT, upload this whole
     bundle (or at least `STACK.md`), and say: *"Follow STACK.md. I want to make my
     project FAIR — it's a [new / existing] project."* The AI walks you through it and
     asks you only what it can't work out itself.
   - **By hand:** work through `for-humans/worksheets/` in order (00 → 04). The checklist
     `00_checklist.md` tells you where you stand; `04_evaluate_existing_project.md` scores
     an existing folder.
4. Sensitive / patient data? Read **`clinical/`** first. The rule: decide sensitivity
   before anything else, and confirm with your data protection officer.

**That's it. You answer the few things only you know; the bundle (and the AI) do the rest.**

---

## → I am an AI (Claude, ChatGPT, Gemini…)

Read **`STACK.md`** and follow it — it is your full rulebook. (If you are Claude, you may
have auto-loaded `CLAUDE.md`, which points you there.) Ask the person first whether the
project is NEW or EXISTING, then follow STACK.md §A or §B. Full walkthrough in
`HOW_TO_USE.md`.

---

## → I just want to hand this to someone (student, collaborator, or an AI)

Give them the whole bundle and point them at this file. That's enough — this page routes
a human to the handout + worksheets, and an AI to STACK.md. Nothing else needs explaining.

For a specific project, also give them the project's own files (metadata, sample sheet,
folder tree) — see `HOW_TO_USE.md` for the exact list.

---

## Scan many projects at once (the auditor agent)

`claude-code-agent/` — a **FAIR-auditor** that scans project folders and scores each
bronze/silver/gold with the steps to improve. Run `fair_scan.py ~/Projects_shared` for a
tier-map of every project in seconds, or use the Claude Code `fair-auditor` agent for the
full per-project action list. Read-only — it reports, never modifies.

## The schema database + git

`for-AI/schemas/SCHEMA_DATABASE_DESIGN.md` — the growing, topic-wise metadata-schema
database (one per assay), ontology-bound, multi-repository export, RO-Crate. `GIT_CONNECTION.md`
— how to move all of this into git and end the zip cycle.

## What's in the bundle

```
START_HERE.md      ← you are here (routes human vs AI)
CLAUDE.md          ← makes Claude auto-load the rules
HOW_TO_USE.md      ← the end-to-end walkthrough + worked example (read this second)
STACK.md           ← the rulebook an AI follows
handout/           ← the 1–2 page standard (for humans)
for-humans/        ← charter · worksheets (setup→metadata→deposition→evaluate) · domains
for-AI/            ← architecture · schemas (+ gold template) · RO-Crate · the build SOPs
clinical/          ← sensitive-data handling (read first if patient data)
FAIR_ACTION_PLAN_SOP.md · PROJECT_CHAT_KICKOFF.md  ← for running a project chat
```

## The one idea

Every piece of metadata is answered by the **machine** (it's in the data), the **project**
(written once), or a **human** (only you know it). Only the last is ever asked of a person.
Keep that list short, use controlled vocabulary, lock the raw data, link everything — and a
project set up right once makes everything downstream (analysis, reports, theses, grants)
cheaper.

---

## For the Würzburg / cRDM group

`STACK.md` §V maps every step onto the real tools — eLabFTW, Nextcloud, JupyterHub/HPC,
GitHub, the metadata app, the SOPs, the use-case registry. An outsider ignores §V.
