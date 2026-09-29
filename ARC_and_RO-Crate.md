# ARC und RO-Crate — wie sie zusammenhängen und wie dieses Bundle darauf mappt

*Kurznotiz zur Einordnung. Frage: Was ist ARC, und was hat es mit RO-Crate zu tun?*

## Die beiden Standards

**RO-Crate** = eine *Verpackungs-Beschreibung*. Eine JSON-LD-Datei
(`ro-crate-metadata.json`), die einen Ordner voller Dateien maschinen- UND menschenlesbar
beschreibt: wer, was, womit, unter welcher Lizenz. Generisch, für jede Disziplin.

**ARC = Annotated Research Context** = ein *Container-Standard* aus der NFDI-Initiative
**DataPLANT** (Pflanzen-/Lebenswissenschaften). Eine **festgelegte Ordnerstruktur** plus
ISA-Metadaten plus Workflows — ein komplettes, standardisiertes FAIR-Datenpaket.

```
meine-ARC/
├── isa.investigation.xlsx     Metadaten im ISA-Modell (Investigation/Study/Assay)
├── studies/                   die Studien
├── assays/                    Messungen: Rohdaten + Metadaten
├── workflows/                 Scripts/Pipelines (CWL)
├── runs/                      Ergebnisse
└── ro-crate-metadata.json     ← RO-Crate ist die Metadaten-SCHICHT in der ARC
```

## Der Zusammenhang (der Kernpunkt)

| | ARC | RO-Crate |
|---|---|---|
| Art | Ordnerstruktur-Standard + ISA + Workflows | Metadaten-Beschreibungsformat (JSON-LD) |
| Rolle | das ganze Paket (Konvention) | die maschinenlesbare Schicht darin |
| Beziehung | **ARC benutzt RO-Crate als seine Metadaten-Schicht** | steckt in der ARC |

**Kurz: ARC ist die Hülle, RO-Crate ist das Beschreibungsformat darin.** Eine ARC *ist*
(u.a.) eine RO-Crate mit fester Ordnerstruktur und ISA-Metadaten. Kein Widerspruch — ARC
ist die strengere, vollständigere Verpackung; RO-Crate die generische Schicht.

## Wie dieses Bundle darauf mappt

Das Bundle baut praktisch schon eine ARC, nur anders benannt:

| Dieses Bundle | ARC-Entsprechung |
|---|---|
| `data/raw_data/`, `primary_data/`, … | `assays/` |
| `scripts/`, CWL-Workflows | `workflows/` |
| `results/` | `runs/` |
| DATAFINDER / Schema-Metadaten | `isa.investigation.xlsx` (ISA-Modell) |
| `ro-crate-metadata.json` (SOP_make_rocrate.md) | dieselbe Datei in der ARC |

**Konsequenz:** Wer das Harmonisierungs-Prinzip + die RO-Crate-SOP konsequent umsetzt,
erzeugt ein **ARC-kompatibles** Objekt. Zur vollen ARC fehlt nur: die Ordnernamen auf die
ARC-Konvention mappen und die Metadaten ins ISA-Format überführen (Tools dafür:
DataPLANT ARCitect, arctrl).

## Warum das strategisch zählt

**ARC ist, was NFDI/DataPLANT für FAIR-Datenpakete empfehlen** — also genau die
Standardisierung, die ein Konsortium später will. Dass dieses Bundle ohne Umweg auf eine
ARC hinausläuft, heißt: Die Arbeit ist zukunftssicher — die erzeugten Objekte lassen sich
zu ARCs machen, wenn/ falls das Konsortium ARC verlangt, ohne alles neu zu bauen.

## Roadmap (falls ARC gewünscht)

1. RO-Crate erzeugen (heute: `SOP_make_rocrate.md`) — die Basis, schon da.
2. Ordner auf ARC-Konvention mappen (`assays/`, `workflows/`, `runs/`).
3. ISA-Metadaten aus dem Schema/DATAFINDER erzeugen (`isa.investigation.xlsx`).
4. Mit ARCitect/arctrl validieren.

Nicht heute nötig — aber gut zu wissen, dass der Weg offen ist. RO-Crate ist der
gemeinsame Nenner; ARC ist die optionale, strengere Ziel-Hülle.
