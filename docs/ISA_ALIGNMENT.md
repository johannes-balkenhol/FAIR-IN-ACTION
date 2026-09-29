# ISA als das verbindende Modell — alles im Bundle aufeinander abgestimmt

*ISA (Investigation / Study / Assay) ist das gemeinsame Metadaten-Modell, auf das das
ganze System ausgerichtet ist. Es ist die Brücke zwischen deinem Schema, der App, dem
menschenlesbaren und dem maschinenlesbaren Output, RO-Crate und ARC.*

## Was ISA ist

Ein Modell, das jedes Experiment in drei Ebenen strukturiert:

```
INVESTIGATION   das Projekt (A03, ein Paper, ein Grant)
   └─ STUDY      eine Studie (z.B. GF vs SPF Darm-Mikrobiom)
        └─ ASSAY  eine Messung (Triple RNA-seq)
```

Das ist **genau dein Modell** — Projekt → Sample → Messung. ISA gibt ihm genormte Namen
und zwei Formate: ISA-JSON (maschinenlesbar) und ISA-Tab/xlsx (die ARC-Form).

## Wie alles darauf ausgerichtet ist

```
   profiles/ (Schema)          die Felder — was erfasst wird
        │  App füllt
        ▼
   ISA-Modell (isa_model.py)   das gemeinsame Modell — Investigation/Study/Assay
        │
   ┌────┴─────────────┬──────────────────┐
   ▼                  ▼                   ▼
menschenlesbar    maschinenlesbar      ARC (make_arc.py)
(Handout,         (ISA-JSON,           DataPLANT/NFDI-
 README)           RO-Crate)            Ordnerstruktur
```

- **Schema (`profiles/`)** liefert die Felder → werden zu ISA Characteristics/Factors.
- **App** füllt sie → exportiert Richtung ISA.
- **RO-Crate** (`bundle/for-AI/`) ist die maschinenlesbare Verpackungsschicht.
- **ARC** (`arc/`) ist die Ziel-Ordnerstruktur; RO-Crate ist die Schicht darin.
- **ISA** ist der gemeinsame Nenner — alles konvertiert über ISA.

## Deine Ordnerstruktur bleibt

Wichtig: **Du behältst deine intuitive Struktur** (`data/raw_data/`, `primary_data/`, …).
`arc/make_arc.py` ist ein **Converter**, der bei Bedarf daraus die ARC-Konvention
(`assays/`, `workflows/`, `runs/`) erzeugt — zum Deponieren/Teilen. Kein Zwang, in der
ARC-Struktur zu arbeiten; sie wird nur beim Export erzeugt.

## Das relationale Schema (deine Metadaten)

ISA IST das relationale Modell:
- Investigation 1—n Study 1—n Assay n—n Sample
- Sample 1—n Characteristic (ontologie-gebunden)
Das `isa_model.py` bildet diese Relationen als Klassen ab. Eine echte relationale DB
(SQL) wäre die nächste Stufe — die Klassen hier sind das Modell dafür, DB-Schema entsteht
am realen Projekt, wenn Datenmenge es verlangt.

## Wo es heute steht (ehrlich)

- ✅ ISA-Modell (`arc/isa_model.py`) — läuft
- ✅ MAGE-TAB → ISA (`arc/sdrf_to_isa.py`) — an echter E-MTAB-17360 getestet
- ✅ ISA → ARC (`arc/make_arc.py`) — erzeugt valide ARC-Struktur + RO-Crate
- ✅ Pipeline (`arc/fair_to_arc.sh`) — alles in einem
- 🔨 andere Assays (Imaging/REMBI, FHIR) → eigene Reader, am Projekt
- 🔨 xlsx-ARC-Form → via DataPLANT ARCitect/arctrl
- 🏗️ App-Integration (RO-Crate/ARC-Export-Knopf) → App-Feature
- 🏗️ echte SQL-DB → wenn Datenmenge es verlangt

Das Fundament steht und ist an echten Daten bewiesen. Der Rest wächst am realen Projekt.
