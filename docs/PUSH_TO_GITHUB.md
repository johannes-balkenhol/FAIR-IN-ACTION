# Pushing the bundle, app, and schemas to GitHub

*Recommended over sharing the .zip — GitHub renders text safely, scans uploads, and a
`git clone` doesn't trip the download virus-scanner that flagged the .zip (which contains
only text + one small python validator — a false positive).*

## Where things go in the FAIR-IN-ACTION repo

```
FAIR-IN-ACTION/
├── app/
│   └── metadata_app.html          the HTML metadata app (already here — the one to build on)
├── schemas/                       ← NEW: the per-assay schema database
│   ├── README.md                  the step-by-step build method
│   └── arrayexpress-scrnaseq/     schema #1, derived from a real accepted submission
│       ├── idf.tsv  sdrf.tsv       the ground-truth MAGE-TAB files
│       ├── arrayexpress_scrnaseq_schema.json
│       └── README.md
├── bundle/                        ← NEW: the FAIR-in-action bundle (START_HERE, STACK, etc.)
│   ├── START_HERE.md  STACK.md  VERSION
│   ├── for-humans/  for-AI/  clinical/  handout/
└── README.md                      repo overview, links to app + bundle + schemas
```

## Commands (from your HPC checkout, not the Nextcloud folder)

```bash
cd ~/Projects_shared/cRDM/Projects/FAIR-in-action    # the GIT checkout
git pull

# add the bundle (unzip the v1.3 bundle into bundle/ first)
mkdir -p bundle && cp -r <unzipped FAIR-in-action>/* bundle/

# add the schemas
mkdir -p schemas
cp -r <schemas/*> schemas/

# the app is already in app/metadata_app.html — nothing to move

git add app schemas bundle
git commit -m "Add FAIR-in-action bundle v1.3, per-assay schemas (ArrayExpress scRNA-seq), maturity path"
git push
```

## On the virus warning

The v1.3 bundle contains: markdown, JSON, TSV, one `.docx`, one small `validate_crate.py`,
and (if included) `metadata_app.html`. No executables, no macros. The flag is almost
certainly a **false positive** on a freshly-downloaded zip containing `.py`/`.html`.

- **Safest path:** don't override the browser warning — push to GitHub as above and
  `git clone` on the other machine. Git transfers don't trigger the download scanner.
- If you must use the zip: right-click → Properties → check the publisher, or scan the
  *extracted* folder (not the zip) with Defender — it will show the files are text.
- Never blindly click "keep anyway" on a download you can't account for. Here you can
  account for it (I built it, it's text), but the GitHub route avoids the question.

## Why GitHub, not the zip, for sharing

Per the maturity path: the repo IS the single source. Zips drift and get re-downloaded
under scanner suspicion; a git repo is versioned, scanned once, and cloned cleanly. The
bundle's own rule — "edit the source, regenerate, don't copy files around" — applies to
the bundle itself.
