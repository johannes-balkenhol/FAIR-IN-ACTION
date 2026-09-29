# Handout — Projektstruktur für Analyse & Reproduzierbarkeit (analyse-orientiert)

*Die zweite Handout-Variante des FAIR-in-action-Bundles. Während das Standard-Handout
(`RDM_handout_v3.docx`) datenmanagement-orientiert ist, zeigt dieses die volle
Analyse-Pipeline-Struktur: von Rohdaten über Notebooks + Scripts bis zu Workflows (CWL/
Nextflow), RO-Crate und ARC. Für Projekte, in denen die Analyse selbst reproduzierbar und
lehrbar sein soll — ein Biologe im Labor soll die Analyse verstehen und nachbauen können.*

---

## Die Ordnerstruktur

```
PROJECT_NAME/
├── README.md            die Karte durch alles · Installation · volle Reproduzierbarkeit
├── DMP.md               Datenmanagementplan
├── LICENSE
│
├── data/
│   ├── raw_data/        erste Messung · unveränderlich · read-only · oder Link
│   ├── primary_data/    Rohdaten nutzbar gemacht (durch Code) · offene Formate
│   ├── secondary_data/  aus externen Quellen zusammengestellt
│   └── meta_data/       das Metadaten-Schema · kontrolliertes Vokabular · Data-Links
│
├── documents/
│   ├── project_plan/    Projektplan · workflow.svg (Flussdiagramm mit Input/Output je Schritt)
│   ├── reports/         tägliche/Zwischen-Reports · Zwischenergebnisse · Diskussion
│   ├── methods/         ELN-Link oder ELN-Datei (.eln/.pdf) · die Methoden
│   ├── experimental_procedure/  das experimentelle Protokoll
│   └── manuscript/      das finale Manuskript
│
├── notebooks/           JupyterNotebooks je Pipeline-Schritt, mit lehrreichen Kommentaren
│   ├── 01_data_exploration_and_qc.ipynb
│   ├── 02_reference_genome_download.ipynb
│   ├── 03_mapping_and_quantification.ipynb
│   └── 04_differential_expression_analysis.ipynb
│
├── scripts/             der Code aus den Notebooks, sauber, mit Input/Output-Header
│   ├── python/          01_… .py  02_… .py  …
│   └── bash/            01_… .sh  02_… .sh  … (z.B. Mapping)
│
├── analysis/            Zwischendaten (NICHT raw/primary/secondary), gespiegelt zur Pipeline
│   ├── intermediate_data/   nummeriert wie scripts/
│   ├── figures/             Zwischen-Abbildungen
│   └── tables/              Zwischen-Tabellen
│
├── results/             kuratierte Endergebnisse
│   ├── figures/         finale Abbildungen (auch fürs Paper)
│   ├── tables/          finale Tabellen
│   └── summaries/       Ergebnis-Zusammenfassungen für Diskussion/Kollaboration
│
└── code/                Workflow-Definitionen (getrennt von scripts/)
    ├── cwl/             CWL-Workflows
    └── nextflow/        Nextflow-Pipelines
```

## Die drei Ebenen des Codes — und warum getrennt

| Ordner | Was | Für wen |
|---|---|---|
| `notebooks/` | die **lehrbare** Analyse — Erklärungen, Kommentare, ein Biologe versteht es | Menschen, zum Verstehen & Nachbauen |
| `scripts/python/` + `scripts/bash/` | der **saubere** Code aus den Notebooks, mit Input/Output-Header | Ausführung, Wiederverwendung |
| `code/cwl/` + `code/nextflow/` | die **portable** Workflow-Definition | Automatisierung, andere Rechner |

**Notebook → Script → Workflow** ist der Reifegrad-Pfad: erst lehrbar, dann sauber, dann
automatisiert. Genau die Maturity-Path-Logik des Bundles, auf die Analyse angewandt.

---

## ⚠️ Drei Dinge für saubere RO-Crate/ARC-Automatisierung

Diese Struktur ist intuitiv — **du behältst sie**. Aber für die *automatische* Konvertierung
zu RO-Crate und ARC sind drei Dinge wichtig:

### 1. Maschinenlesbare Input/Output-Header (das Wichtigste)

Jedes Script sagt im Header, welche Dateien rein- und rausgehen — **nicht nur als
Kommentar, sondern maschinenlesbar**, damit `make_arc.py` die Provenienz-Kette automatisch
bauen kann:

```python
# ── 03_mapping_and_quantification.py ──
# Zweck: Reads gegen die kombinierte Referenz mappen, Counts pro Organismus
INPUTS  = ["data/primary_data/V_19_R1.fastq.gz",
           "data/primary_data/V_19_R2.fastq.gz",
           "data/secondary_data/combined_reference.fa"]
OUTPUTS = ["analysis/intermediate_data/V_19_mouse_counts.tsv",
           "analysis/intermediate_data/V_19_E10_counts.tsv",
           "analysis/intermediate_data/V_19_phage_counts.tsv"]
# ────────────────────────────────────────
```

Daraus baut der Converter automatisch: **Output-Datei ← erzeugt von diesem Script ←
aus diesen Inputs**. Das ist die Brücke von deiner Ordnerstruktur zur RO-Crate. Ohne diese
maschinenlesbaren Listen muss ein Mensch jede Verknüpfung von Hand eintragen.

### 2. Ordnernamen → ARC-Konvention (der Converter mappt)

ARC (DataPLANT/NFDI) hat eine feste Struktur. Deine ist intuitiver; `arc/make_arc.py`
mappt sie beim Export:

| Deine Struktur | → ARC |
|---|---|
| `data/raw_data/`, `data/primary_data/` | `assays/<assay>/dataset/` |
| `scripts/`, `code/cwl/`, `code/nextflow/` | `workflows/` |
| `analysis/`, `results/` | `runs/` |
| `data/meta_data/` (Schema, Data-Links) | `isa.investigation` + Study/Assay |
| `documents/` | Study-Beschreibung, Protokolle |

Du arbeitest in deiner Struktur; die ARC entsteht nur beim Deponieren. Wichtig: Der
Converter muss deine **genauen Ordnernamen** kennen — halte sie konsistent (siehe Punkt 3).

### 3. `meta_data/` statt `metadata/` — Konsistenz

Eine Schreibweise durchziehen (`meta_data/`, wie im Standard-Handout und der App). Zwei
Varianten (`metadata/` vs `meta_data/`) verwirren den Converter und die Menschen.

---

## Kein Excel-DataFinder mehr nötig

**Wichtige Vereinfachung:** Der frühere Excel-„DataFinder" (die suchbare Proben-Tabelle)
wird **überflüssig**, wenn die `.sdrf.tsv` in `meta_data/` mit klaren **Data-Links**
(Datei ↔ Sample ↔ Organismus) gefüllt ist und am Ende eine **RO-Crate** entsteht. Warum:

- Die `.sdrf.tsv` ist eine Tabelle → **menschen- UND maschinenlesbar** (was der DataFinder
  auch sein sollte)
- Die Data-Links machen die Datei↔Sample-Zuordnung explizit → das war der Kernzweck des
  DataFinders
- Die RO-Crate macht alles maschinen-navigierbar → besser als eine Excel-Suche

Also: **`.sdrf.tsv` + Data-Links + RO-Crate ersetzen den DataFinder.** Eine Datei weniger
zu pflegen, kein Excel-Drift. (Wer trotzdem eine schnelle Übersicht will: die `.sdrf.tsv`
öffnet sich in jedem Tabellenprogramm.)

---

## Alles ist verknüpft — die FAIR-Kette

```
raw_data ──(scripts, Header: IN→OUT)──▶ primary/secondary/intermediate
    │                                          │
  meta_data (Schema + Data-Links) ─────────────┤
    │                                          │
  documents (Plan, Methoden, ELN, Manuskript)──┤
    │                                          ▼
    └──────────────▶ RO-Crate (ro-crate-metadata.json) ──▶ ARC ──▶ FAIR-Objekt
                     alles verknüpft: Daten + Doku + Analyse + Provenienz
```

- **Daten ↔ Metadaten:** über die Sample-ID und die Data-Links
- **Daten ↔ Analyse:** über die Input/Output-Header der Scripts
- **Analyse ↔ Doku:** `workflow.svg` in `project_plan/` zeigt die Kette; Reports in
  `reports/`; Methoden/ELN in `methods/`
- **Alles ↔ RO-Crate:** der Converter liest die Header und die Struktur → automatisch

## README, DMP, LICENSE — sauber vorbereiten

Wie im Standard-Handout: README als Karte (mit den Links zu ELN, Analyse-Server, Git,
Zenodo, DOI), DMP am Start geschrieben, LICENSE gewählt. Diese drei sind die Basis für
jedes FAIR-Objekt.

---

## Der Weg zur Automatisierung

Mit dieser Struktur + den maschinenlesbaren Headern ist der Weg frei für:

1. **CWL/Nextflow** in `code/` — aus den Scripts, die Input/Output schon deklarieren
2. **RO-Crate** — `arc/make_arc.py` liest Header + Struktur → `ro-crate-metadata.json`
3. **ARC** — die RO-Crate + ISA-Metadaten → die NFDI-Ordnerstruktur
4. **FAIR-Objekt** — deponierbar, zitierbar, konsortiumsweit verknüpfbar

Das ist der Sinn der ganzen Struktur: nicht nur ordentlich, sondern **auf automatische
Konvertierung vorbereitet**.

---

*Diese Variante ergänzt das Standard-Handout. Beide sind gültig: das eine
datenmanagement-orientiert, dieses analyse-orientiert. Für ein Analyse-Projekt mit
Pipeline (wie A03 Triple RNA-seq) ist diese Struktur die passende.*
