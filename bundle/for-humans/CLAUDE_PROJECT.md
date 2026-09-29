# Using an AI assistant with this package

*Optional. If you use Claude (or a similar assistant) to help run your project, this sets
it up so its advice follows the charter instead of generic guesses.*

## Set up a Project

1. Create a new Project in Claude.
2. **Upload as knowledge:** `FAIR_CHARTER.md`, your chosen `domains/` page (or your
   filled-in `_TEMPLATE.md`), and `worksheets/00_checklist.md`.
3. **Paste into the Project's custom instructions** (not as a file — instructions are
   always in effect; files are only consulted):

```
This project follows the FAIR charter (FAIR_CHARTER.md). Read it first.

Before advising on metadata or data structure, identify the domain and the unit
of study from the attached domain page. If it is unclear, ask — don't guess.

Sort every metadata field into machine / project / human. Only ever ask me to
provide the "human" fields — anything a script could read from the data is not my
job to type.

Use controlled-vocabulary terms where they exist. A wrong term is worse than free
text: if no term fits, say so and record it as a named characteristic rather than
forcing a wrong one.

When uncertain, say so. A confidently wrong metadata value is worse than an
admitted gap.
```

## What it is good for

- Turning your `domains/` page into a concrete metadata list for your specific study.
- Writing the small extractor script that reads your machine-readable fields.
- Reviewing a folder and telling you what is missing for bronze/silver/gold.
- Drafting the README, the data-availability section, the DMP.

## What to keep it away from

- Deciding sensitivity or legal basis — that is yours and your institution's.
- Inventing ontology terms — make it look them up, not guess them.
- Anything where a confident wrong answer is worse than no answer. Tell it to flag
  uncertainty rather than paper over it.

## Facts in files, behaviour in instructions

Upload the *reference material* (charter, domain page, checklist) as files. Put the
*rules of behaviour* in the instructions. The instructions are read every message; a
file might not be opened. Keeping the upload small — three or four files — means the
assistant actually attends to them.
