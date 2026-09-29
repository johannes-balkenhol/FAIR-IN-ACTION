# arc/ — ISA-Modell, ARC-Converter, RO-Crate-Verbindung

Die Schicht, die alles verbindet: das **ISA-Modell** (Investigation/Study/Assay) als
gemeinsames Datenmodell, ein **Converter** von den Metadaten zur **ARC** (DataPLANT/NFDI),
mit **RO-Crate** als maschinenlesbarer Schicht darin.

## Was ist was

| Datei | Rolle |
|---|---|
| `isa_model.py` | Das ISA-Modell als Python-Klassen (Investigation→Study→Assay→Sample). Die verbindende Datenschicht. |
| `sdrf_to_isa.py` | Liest echte MAGE-TAB (SDRF+IDF) → ISA. Beweis: ISA aus echten, akzeptierten Metadaten. |
| `make_arc.py` | ISA → ARC-Ordnerstruktur mit RO-Crate. Der ARC-Converter. |
| `fair_to_arc.sh` | Die ganze Pipeline in einem: MAGE-TAB → ISA → ARC → validiert. |

## Benutzen

```bash
# alles in einem:
./fair_to_arc.sh projekt.idf.txt projekt.sdrf.txt /pfad/zum/projekt /pfad/zur/ARC
```

Ergebnis: eine ARC-Struktur (studies/ assays/ workflows/ runs/ + ro-crate-metadata.json),
ISA-vollständig, RO-Crate-validiert, ARC-kompatibel.

## Das Prinzip (alles aufeinander abgestimmt)

```
profiles/ (Schema)  →  App füllt  →  ISA-Modell  →  RO-Crate  →  ARC
   Felder              Werte          gemeinsames     maschinen-    NFDI-
                                      Modell          lesbar        Standard
```

- **Deine Ordnerstruktur bleibt** wie sie ist (intuitiver) — `make_arc.py` ist der
  **Converter**, der bei Bedarf daraus die ARC-Konvention erzeugt. Du arbeitest weiter in
  `data/raw_data/` etc.; die ARC entsteht nur zum Deponieren/Teilen.
- **Rohdaten** → in `assays/` (verlinkt, nicht kopiert).
- **prozessierte Daten** → in `runs/`, NICHT neu annotiert — sie hängen an den
  `workflows/` (dem Script). Das Harmonisierungs-Prinzip.

## Grenzen (ehrlich)

- `sdrf_to_isa.py` ist an ArrayExpress-MAGE-TAB getestet (RNA-seq). Andere Assays
  (Imaging/REMBI, klinisch/FHIR) brauchen eigene Reader → wachsen am realen Projekt.
- `isa.investigation.xlsx` (Excel-ARC-Form) erzeugt DataPLANT **ARCitect/arctrl** aus
  dieser JSON. Hier: die ISA-JSON-Form (vollständig, aber nicht die xlsx).
- Voll produktiv wird das am **echten Projekt (A03)** — dort zeigt sich, welche
  ISA-Felder und Workflow-Verknüpfungen wirklich nötig sind.
