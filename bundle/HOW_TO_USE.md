# How to use this bundle — the complete walkthrough

*The one page that shows what using FAIR-in-action actually looks like, end to end, with a
real worked example. If `START_HERE.md` tells you which door, this tells you how to walk
through it.*

---

## The whole workflow in one picture

```
1. THIS bundle chat        →  produces the rules: STACK.md, the SOPs, the schemas
        │
2. open a PROJECT chat     →  one chat per project (e.g. "DECIDE_A03")
        │
3. upload to that chat:    →  STACK.md + FAIR_ACTION_PLAN_SOP.md + SOP_build_schema_and_app.md
                              + the project's own files (.sdrf, .idf, sample sheet, config)
        │
4. paste the kickoff       →  from PROJECT_CHAT_KICKOFF.md, filled for your project
        │
5. the chat runs the SOP   →  assesses → lists gaps (auto/human/check) → does the auto ones
        │                      → builds the assay schema → generates the collaborator HTML
        │
6. you + collaborators     →  fill only the highlighted open fields
        │
7. deposit + package       →  ArrayExpress(+ENA) / repository → RO-Crate → DOI
```

**Build once here. Apply per project there.** That separation is the whole design — it's
why one bundle scales across all your projects without redoing the thinking.

---

## What you upload to a project chat

Every project chat needs these, because **chats are isolated — one chat cannot see another
chat's files or its connected folders.** So you carry them in each time:

**From the bundle:**
- `STACK.md` — the rules the AI enforces
- `FAIR_ACTION_PLAN_SOP.md` — the per-project action list generator
- `for-AI/SOP_build_schema_and_app.md` — how to build the schema + the capture app
- `for-AI/schemas/_gold-template_E-MTAB-17360/` — the correct-by-construction template

**From the project (on your HPC/cloud):**
- the metadata: `.sdrf.tsv` / `.idf.yaml` (or whatever exists)
- the sample sheet (even if it's a PDF — the chat extracts it)
- `config.yaml`, the folder tree (`tree -L 4` output)
- the capture app `metadata_app.html` (from the FAIR-IN-ACTION GitHub repo)

Then paste the kickoff prompt from `PROJECT_CHAT_KICKOFF.md`, filled in.

---

## Worked example — DECIDE_A03 (triple RNA-seq)

*This is what a real hand-off into a project chat looks like. Copy the shape for any
project.*

**The assessment (what the chat is told / works out):**

> The project is genuinely close to publishable. A03 already has: correct skeleton, DMP,
> LICENSE, README, environment.yml, real `.idf.yaml` + `.sdrf.tsv` metadata, checksums
> (`md5_*.log`), and the VRC SOPs already in `documents/`. Someone did this well.
>
> It's **triple RNA-seq** — mouse (GRCm39) + bacteria E10 + phage SepSi_11_M, confirmed by
> `data/refs/` (three genomes) and `combined/chrom_to_organism.tsv`. Design: GF/SPF ×
> bacteria/phage.

**The gap list the chat produces (auto / human / check):**

1. Declare all **three organisms with roles** in the SDRF (host / bacterium / phage)
2. Finish the metadata — `METADATA_TODO.md` is unfinished; fill the human `Characteristics[]`
3. Convert `.idf.yaml` → **MAGE-TAB `.idf.txt`** (ArrayExpress wants tab-delimited, not YAML)
4. Sample sheet is a **PDF** → extract to the structured DATAFINDER
5. Build the **DATAFINDER** at root (V_1..V_19 → cohort, organisms, batch, file pointers)
6. Tidy the duplicated `processed/` vs `processed_data/` dirs
7. Run **G1/G2 gates** — the Before-Sharing checklist is already in `documents/`
8. Record the **read-partitioning method** + combined reference build for the multi-organism DE

**The tooling already on the HPC** (don't rebuild): `make_ae_metadata.py`,
`make_metadata.py`, `make_primary_h5ad.py`, `MetadataTemplates/`.

**The template to copy from:** the completed **E-MTAB-17360** (scRNA-seq) — same shape,
curator-accepted, correct by construction. For triple RNA-seq: strip its single-cell
barcode fields, add the two extra organism rows (see `SOP_build_schema_and_app.md`).

**The outcome:** a scaffolded, metadata-complete, gate-checked project with a
`metadata_app_A03.html` whose open fields Mercedes Gomez's team fill in a browser — then
deposit to ArrayExpress (which brokers the raw reads to ENA automatically).

---

## Two limits to know (so nothing surprises you)

1. **Chats are isolated.** No chat — including an AI in this bundle chat — can open a
   `claude.ai/chat/...` or `claude.ai/project/...` link, or see another chat's connected
   folder. You carry files between chats by uploading them. This is why the kickoff
   uploads everything the project chat needs.

2. **The AI proposes; you and your DPO dispose.** For anything touching sensitive data or
   data-protection law, the AI flags and stops — it does not authorise. That is by design
   (see `STACK.md` §4 and `clinical/`).

---

## If you are a human who just wants the short version

1. Open `START_HERE.md` → pick your door (new / existing / sensitive).
2. Open the **1–2 page handout** (`handout/`) → that's the whole standard at a glance.
3. For real work, open a **project chat**, upload the four bundle files + your project's
   files, and paste the kickoff. The chat does the rest and hands you a short list of what
   only you can answer.

That's it. The bundle makes the project FAIR; you answer the few things only a human knows.
