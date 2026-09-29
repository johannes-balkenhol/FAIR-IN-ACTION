# The maturity path — the organizing logic of FAIR-in-action

Every part of this bundle sits on one of three steps, and the whole design is about
climbing them in order.

```
┌──────────────────────────────────────────────────────────────────┐
│ 1. RULE        SOP · guideline · checklist                        │
│                humans and AI follow it by hand                     │
│                (the handout, STACK.md, the evaluation checklist)   │
├──────────────────────────────────────────────────────────────────┤
│        ↓  once the rule is stated precisely enough to automate     │
├──────────────────────────────────────────────────────────────────┤
│ 2. AUTOMATION  a script does it, no hand-work                      │
│                folder creation · checksums · metadata extraction   │
│                rsync (cloud⇄HPC) · standardised git commits        │
├──────────────────────────────────────────────────────────────────┤
│        ↓  once the automation is trustworthy                       │
├──────────────────────────────────────────────────────────────────┤
│ 3. CONTROL     the app fills, checks, and ENFORCES                 │
│                metadata_app.html: schema-driven forms, folder      │
│                creation, controlled-vocab enforcement, autofill    │
│                from source (machine/ELN), export in many formats   │
└──────────────────────────────────────────────────────────────────┘
```

## Why this order matters

**You cannot automate a rule you haven't stated precisely, and you cannot enforce in an
app something you haven't automated.** So the work is always rule → automation → app, never
the reverse. A vague guideline ("keep good metadata") can't be automated; a precise one
("every sample row needs organism as an NCBITaxon term, from this API") can — and then the
app can enforce it with a dropdown.

This is also why the bundle *starts* as documents (SOPs, checklists) and *grows* into
tooling. The documents aren't a placeholder for the app — they're step 1, and they stay
valuable because they define what steps 2 and 3 must do.

## MetaFold — the worked proof

MetaFold (Münster; ThZobel/MetaFold) is a similar HTML/desktop app that already walked this
path for imaging RDM: it took the guideline "make a structured project folder with
metadata" and turned it into one-click, template-driven folder creation with capture-time
forms. **Evaluate it as the reference implementation of step 2→3**, and bring its
automation features into our HTML app:

| MetaFold feature | Bring into our app as |
|---|---|
| Template-based folder creation | automated scaffold from the project skeleton |
| Category system (templates by project type) | per-assay schema selection |
| Capture-time metadata forms | the schema-driven form (already the app's core) |
| Prefilled reusable fields | project-level autofill |
| Filename suggestion | enforce the naming rule at creation |
| `metadata.json` + `readme.html` output | machine + human readable output (→ RO-Crate) |
| eLabFTW + OMERO integration | pull/push metadata to the ELN via API |
| Project discovery (recursive scan) | the "evaluate existing project" function, automated |

That last row is worth noting: MetaFold's *recursive scan of existing data* is the
automated version of our by-hand `04_evaluate_existing_project.md` checklist \u2014 the same
step 1 → step 2 climb.

## The controlling angle

Step 3 isn't just convenience \u2014 it's **control**. Once the app enforces the schema
(dropdowns instead of free text, required fields, ID patterns, source-tagged autofill), the
rules can't be silently broken. That is how "please follow the SOP" becomes "the SOP is
enforced by construction" \u2014 the same move as the FAIR/GDPR gates becoming automated checks
before share/publish.

**The endpoint:** rules the app enforces, gates the app checks, metadata the app fills from
source \u2014 so a FAIR + GDPR-compliant project is the path of least resistance, not extra work.
