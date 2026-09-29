# SOP — aus einem fertigen Projekt eine RO-Crate machen

*Der letzte Schritt der Maturity-Path: das fertige, FAIR-annotierte Projekt wird in eine
RO-Crate gepackt — das maschinen- UND menschenlesbare Forschungsdatenobjekt. **Jetzt per
SOP (dieses Dokument); später als Knopf in der App.** Die App kann heute schon eine
RO-Crate exportieren; diese SOP beschreibt den vollständigen Weg für das ganze Projekt.*

---

## Wann

Am Ende, wenn das Projekt Silver/Gold ist: Metadaten vollständig, Rohdaten annotiert,
Script vorhanden, Repository-Accession/DOI da (oder pending). Die RO-Crate ist die
Verpackung, die alles zu einem zitierbaren, wiederverwendbaren Objekt bündelt.

## Was in die RO-Crate kommt (und was NICHT)

Nach dem Harmonisierungs-Prinzip (`METADATA_HARMONIZATION.md`):

| Gehört rein | Wie |
|---|---|
| **Rohdaten-Metadaten** (das feste Schema) | als strukturierte Entities in `ro-crate-metadata.json` |
| **Rohdaten** selbst | als `File`-Entities (oder Link, wenn zu groß / in ENA) |
| **das Script** (Pipeline, Analyse) | als `SoftwareSourceCode` / Workflow-Entity — die Provenienz |
| **prozessierte Daten** | als `File`, **verknüpft mit dem Script**, das sie erzeugte — NICHT neu annotiert |
| **Personen, Lizenz, Identifiers** | Root-Dataset-Properties (creator, license, identifier) |
| **ELN-Link, Repository-Accession, Code-DOI** | als `related_identifiers` / Links |

**Prozessierte Daten (h5ad, counts) werden NICHT von Hand annotiert** — sie hängen am
Script, das sie erzeugte. Das ist der Kern: die RO-Crate enthält Rohdaten-Metadaten +
Script + Zeiger auf prozessierte Daten, nicht standardisierte h5ad-Annotationen.

## Der Weg — heute (per SOP / Script)

### Schritt 1 — App-Export als Basis
In der Metadaten-App: Export → **`custom — raw JSON of everything`** ODER
**`catalogue — DataCite / JSON-LD record`**. Das liefert die strukturierten
Rohdaten-Metadaten. (Die App exportiert bereits eine RO-Crate-nahe JSON-LD.)

### Schritt 2 — die Vorlage füllen
`bundle/for-AI/ro-crate-metadata.template.json` in den Projekt-Root kopieren als
`ro-crate-metadata.json` und füllen:
- **Root-Dataset:** title, description, datePublished, creator (ORCID), license, identifier
- **`hasPart`:** die Dateien — Rohdaten, DATAFINDER, die Script-Dateien, prozessierte Daten
- **das Script:** als Entity mit `@type: ["File", "SoftwareSourceCode"]`, verlinkt vom
  Code-Repo/Zenodo-DOI
- **prozessierte Dateien:** jeweils `resultOf` → das Script (die Provenienz-Kette)
- **`mentions`/Sample-Entities:** die Sample-IDs aus dem DATAFINDER mit ihren
  Charakteristiken (organism, condition …) als `PropertyValue` mit `propertyID` (CURIE)

### Schritt 3 — validieren
```bash
python3 bundle/for-AI/validate_crate.py ro-crate-metadata.json
```
Muss "structurally valid RO-Crate" melden. Prüft: Descriptor, Root-Dataset, keine toten
Referenzen.

### Schritt 4 — packen
Der Projekt-Ordner MIT der `ro-crate-metadata.json` im Root **ist** die RO-Crate. Zum
Verschicken/Deponieren: als ZIP (dann heißt es RO-Crate-Zip) oder in ein Repository, das
RO-Crate versteht (WorkflowHub, Zenodo mit RO-Crate).

## Der Weg — später (in der App, ein Knopf)

Die App hat schon einen RO-Crate-nahen Export. Der Ausbau (App-Feature, nicht Bundle):
1. Knopf **"Export → RO-Crate"** neben den anderen Export-Optionen
2. sammelt: die gefüllten Schema-Felder + die DATAFINDER-Zeilen + die Datei-Zeiger
3. fügt die Script-/Code-Repo-Links als Provenienz-Entities ein
4. schreibt eine vollständige, validierte `ro-crate-metadata.json`
5. optional: zippt den Projekt-Ordner zur RO-Crate-Zip

Das ist der letzte Schritt der Maturity-Path für die App: Regel (diese SOP) → Automation
(ein Script `make_rocrate.py`) → Kontrolle (der App-Knopf). Gebaut wird es **am realen
Projekt** (A03), nicht abstrakt — dort zeigt sich, welche Provenienz-Verknüpfungen wirklich
nötig sind.

## Für A03 konkret

```
A03/
├── ro-crate-metadata.json         ← das hier erzeugt die SOP
├── data/raw_data/  (FASTQ)        → File-Entities + Schema-Metadaten
├── data/meta_data/ (DATAFINDER)   → Sample-Entities mit CURIEs
├── scripts/  (Pipeline)           → SoftwareSourceCode-Entity (die Provenienz)
├── data/processed/ (counts pro Organismus) → File, resultOf → das Script
└── README.md                      → menschenlesbare Beschreibung
```
mouse/E10/phage-counts werden NICHT einzeln annotiert — sie hängen am Pipeline-Script,
das sie aus den FASTQ + der kombinierten Referenz erzeugte. Genau das Harmonisierungs-
Prinzip in der Praxis.

---

## Nächster Schritt für die Automatisierung

Ein `make_rocrate.py` schreiben, das aus dem App-JSON-Export + dem DATAFINDER + den
Datei-Pfaden automatisch die `ro-crate-metadata.json` baut. **Das ist ein Script, gebaut am
A03-Projekt** — der natürliche nächste Entwicklungsschritt, wenn A03 metadaten-fertig ist.
Bis dahin: diese SOP von Hand (mit der Vorlage + dem Validator).
