# Harvest prompt — paste this into a project chat to improve the FAIR bundle

*Copy the block below into any project chat (FlowSep, PANC, DECIDE, a conference chat,
the VRC/SOP chat…). It asks that chat to report — in a fixed, mergeable format — what it
knows that could improve the shared FAIR-in-action bundle. Because the format is fixed,
the answers from different chats drop straight into `BUNDLE_description.md` without
reconciling by hand.*

---

```
We are assembling a shared FAIR-in-action bundle — one set of materials we hand to
every scientist (human-readable) and every AI assistant (machine-readable) so every
project is guided the same way. It has these layers: FAIR principle (RDM handout),
FAIR-data-object definition + RO-Crate profile, the metadata SCHEMA (LinkML), the
metadata GENERATOR APP, RO-Crate packaging, secure-handling guideline, and deposition.

From THIS project's work, report anything that could improve that bundle. Please answer
ONLY in the fixed format below — short, concrete, one bullet per item, no prose. If a
section has nothing, write "none".

## 1. Concrete artifacts (with locations)
- GitHub repos / URLs (schema, app, scripts) — exact links
- The metadata schema: where it lives, what format (LinkML/JSON/…), how many fields
- The metadata generator app: name, URL, what it does, what stage it's at
- Any deposition scripts, extractors, validators — path or URL

## 2. Metadata fields & vocabulary this project needs
- Fields specific to this domain the core schema is missing
- Controlled vocabularies / ontologies used (name + how bound: OLS API, cached, …)
- ID patterns / naming rules that must be enforced (regex if any)

## 3. What worked / what broke (evidence for the bundle)
- A concrete success ("did X in N days because the schema was reused")
- A concrete failure to design against ("free-text field gave SEP125 vs SEP 125")
- Any machine-vs-human field split learned here (what the instrument gave for free)

## 4. Deposition & repository facts
- Which repository this data goes to, and why
- The exact metadata format it demands (SDRF/IDF, REMBI, MIxS, …)
- Anything only-a-human-knew at submission time (the fields that cost days)

## 5. Standards / tools seen that we should adopt or align with
- Name + one line + link (e.g. a conference tool, a repository checklist)

## 6. One thing you'd change about the current bundle
- The single most useful improvement, from this project's perspective

Keep it factual and copy-pasteable. Exact URLs and field names matter more than
explanation — I will merge these answers into the bundle description directly.
```

---

## What to UPLOAD to the target chat (so it can answer well)

Before pasting the prompt into a project chat, give that chat the current bundle so it
knows what it is improving. Upload:

- `BUNDLE_description.md` (this bundle's contents + the real repo list)
- `02_FAIR_data_object_definition.md` (what a finished object is)
- the RDM handout (`2026-09-07_RDM_handout_AGHeinze_v3.docx`)

That is enough context (~4 files) for the chat to see the target and report only what is
missing or better in ITS domain. Do not upload the whole bundle — the three above are the
orientation; more just dilutes it.

## How to use the answers

1. Run it in each relevant chat: **FlowSep, PANC, DECIDE / infection projects, the
   conference chat, the VRC/SOP chat**, and any clinical chat.
2. Paste each answer into a scratch file, or straight back into the bundle chat.
3. The fixed sections map 1:1 onto `BUNDLE_description.md`:
   - §1 → fills the two `<FILL IN>` URLs and the "what each piece is" rows
   - §2 → the schema's field/vocabulary coverage
   - §3 → the "what worked / what broke" evidence table
   - §4 → the deposition section
   - §5 → the "standards to adopt" list
   - §6 → the backlog of improvements

## Why a fixed format

Free-form "tell me what you know" gives six differently-shaped answers you then have to
reconcile. A fixed template means every chat returns the same six sections, so merging is
mechanical — the same reason the metadata schema itself uses fixed fields rather than free
text.

## The two things most worth getting

Everything helps, but two answers unblock the most:

1. **The exact GitHub URLs** (§1) — the schema repo and the app. These are the `<FILL IN>`
   gaps; once filled, the bundle can point at real code.
2. **Each project's missing fields** (§2) — this is how the core schema grows to actually
   cover the group's work, instead of being omics-shaped forever.
