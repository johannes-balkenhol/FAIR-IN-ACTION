# Connecting FAIR-in-action to git (and ending the zip cycle)

Your Nextcloud folder currently holds only zips:
```
FAIR-in-action/
├── 2026-09-28_FAIR-in-action_v1.6.1.zip
├── 2026-08-31_..._DECIDE-A06-...zip
├── README.md · README_SEND.md
└── _archive/
```

The bundle, the schemas, and the app should live in **git**, not as zips. Git is the
source of truth; Nextcloud holds data, not code. Here is the clean connection.

## The target repo layout

```
github.com/johannes-balkenhol/FAIR-IN-ACTION
├── app/
│   └── metadata_app.html          the collection app (already here)
├── schemas/                       the growing schema database
│   ├── SCHEMA_DATABASE_DESIGN.md
│   ├── _gold-template_E-MTAB-17360/
│   ├── arrayexpress-scrnaseq/
│   ├── triple-rnaseq/             (A03 — added by the A03 chat)
│   └── …                          one folder per assay, grows per project
├── bundle/                        the FAIR-in-action bundle (STACK, SOPs, handout, …)
│   └── (everything currently in the zip)
├── agent/                         the fair-auditor agent + fair_scan.py
├── .claude/agents/fair-auditor.md
└── README.md
```

## Do this ONCE (from the HPC, where git works and Nextcloud isn't in the way)

```bash
# on the HPC — you already have Projects_shared with the generators
cd ~/Projects_shared
git clone https://github.com/johannes-balkenhol/FAIR-IN-ACTION.git
cd FAIR-IN-ACTION

# unpack the current bundle into bundle/
mkdir -p bundle schemas agent
# (copy the bundle contents in — from the v1.6.1 zip, extracted on the HPC)

# move the existing HPC generators into the repo where they belong
cp ~/Projects_shared/make_ae_metadata.py ~/Projects_shared/make_metadata.py \
   ~/Projects_shared/make_primary_h5ad.py agent/ 2>/dev/null || true

git add -A
git commit -m "Bundle v1.6.1, schema database, fair-auditor agent"
git push
```

## From then on — no more zips

```bash
git pull            # get the latest bundle/schemas/app anywhere
git add schemas/triple-rnaseq && git commit -m "A03 triple schema" && git push
```

## The Nextcloud ↔ git boundary (the rule that keeps it clean)

- **git** holds: the bundle, schemas, app, agent, generators — everything that is *code or
  standard*.
- **Nextcloud** holds: project *data*, shared files, the human-facing handout copy.
- They connect through the README (links) and `.gitignore` (Nextcloud paths git-ignored).
- **Never `git clone` into a Nextcloud-synced folder** — `.git` + sync = corruption. Clone
  on the HPC (native disk), let Nextcloud mirror only the non-`.git` outputs if needed.

## Why this ends the pain

Every friction this month — `files.zip`, rename cycles, failed unzips, the virus flag —
came from moving the bundle as a downloaded zip through Nextcloud+WSL. Git transfers don't
download-scan, don't need renaming, don't re-sync under you. **The bundle becomes
`git pull`, and the schema database grows by `git commit` — versioned, shared, clean.**
