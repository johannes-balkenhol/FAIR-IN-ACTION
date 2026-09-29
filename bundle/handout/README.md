# Handout — zwei Varianten

Das Bundle hat zwei Handout-Varianten. Beide sind gültig; nimm die, die zum Projekt passt.

| Variante | Fokus | Wann |
|---|---|---|
| `RDM_handout_v3.docx` | **Datenmanagement** — Ordnerstruktur, Benennung, Lifecycle, Gates | jedes Projekt, der Standard (AG Heinze v0.3) |
| `RDM_handout_analysis_oriented.md` | **Analyse & Reproduzierbarkeit** — Notebooks, Scripts, Workflows (CWL/Nextflow), RO-Crate/ARC-ready | Analyse-Projekte mit Pipeline (z.B. RNA-seq) |

Die analyse-orientierte Variante zeigt zusätzlich:
- Notebooks (lehrbar) → Scripts (sauber) → Workflows (portabel)
- maschinenlesbare Input/Output-Header für automatische RO-Crate-Provenienz
- wie die Ordnerstruktur auf ARC gemappt wird
- warum der Excel-DataFinder bei sauberer .sdrf.tsv + Data-Links + RO-Crate entfällt

`rdm_handout_source.js` erzeugt die .docx-Variante (Node + docx).
