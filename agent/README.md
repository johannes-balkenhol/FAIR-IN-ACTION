# FAIR-auditor — the folder-scanning agent

Two forms of the same thing (the maturity path: automation → app-enforced control):

## 1. `fair_scan.py` — the automation (run it anywhere, no AI)

```bash
python3 fair_scan.py ~/Projects_shared            # tier-map ALL your projects at once
python3 fair_scan.py ~/Projects_shared/DECIDE_A03_MercedesGomez   # one project
```

Read-only. Scores each folder bronze/silver/gold from what's on disk, notes assay signals
(never asserts biology), flags GDPR-suspicious names. Gives you the map of where every
project stands in seconds.

## 2. `.claude/agents/fair-auditor.md` — the Claude Code agent (judgement + action list)

In Claude Code, from your Projects_shared directory:

```
> use the fair-auditor agent to scan all DECIDE_* projects and give me the action list
```

The agent runs the same checks PLUS reads the real metadata files, adds the tiered
[auto]/[human]/[check] action list, and refuses to guess biology (STACK.md §2b). It's
read-only — it reports, you decide.

## Why both

`fair_scan.py` is fast and needs no AI — use it for the overview across 40 projects.
The agent adds the per-project judgement and the concrete next steps — use it to actually
work one project. Together: scan everything with the script, then send the agent at the
ones that need work.

## The workflow this enables

```
fair_scan.py ~/Projects_shared   →  "these 6 are bronze, these 3 not-yet, A03 is silver"
        ↓ pick the ones to finish
fair-auditor agent on each        →  action list per project
        ↓ execute [auto], fill [human]
each project → FAIR + deposited
```
