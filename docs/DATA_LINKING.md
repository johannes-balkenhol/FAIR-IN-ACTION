# Data-Linking — Dateien mit Metadaten verknüpfen (das Manifest-Prinzip)

*Antwort auf: "Wo sind die Data-Links? Wie löst man 500 FASTQ, meist gleiche Metadaten,
wenige Felder unterschiedlich, intelligent?" — Die Lösung ist ein gelöstes Problem; jedes
Repository macht es so.*

## Das Prinzip: Vererbung + Manifest (wie SDRF)

Nicht 500× alles tippen. Zwei Ebenen:

1. **Projekt-Ebene — was für ALLE gleich ist**, einmal (Organismus, Protokoll, Instrument,
   Lizenz…). Das sind die `source: project`-Felder der App.
2. **Manifest-Tabelle — nur was sich unterscheidet**, eine Zeile pro Datei:
   `datei | sample | read | lane | pfad | md5`. Alles andere wird vom Projekt geerbt.

So macht es ArrayExpress (SDRF), nf-core (samplesheet), jedes Sequencing-Sample-Sheet.

## Warum eine Tabelle, nicht 500 × .meta.json

| Ansatz | Wann |
|---|---|
| **Manifest (eine Tabelle)** | viele Dateien, meist gleiche Metadaten → **der Normalfall** |
| Pro-Datei `.meta.json` | wenige, große, sehr unterschiedliche Dateien |

Bei "500 FASTQ ↔ 8 Samples" ist die Tabelle richtig: 500 Zeilen, aber nur die
Sample-Spalte + read/lane unterscheiden sich; der Rest kommt vom Projekt.

## Intelligent: Automuster + Korrektur

Die App liest den Dateinamen und **schlägt** sample/read/lane vor:

```
S1_L001_R1_001.fastq.gz   → sample=S1   read=R1  lane=L001   ✓
S1_L002_R1_001.fastq.gz   → sample=S1   read=R1  lane=L002   ✓
V_12_R1.fastq.gz          → sample=V    read=R1              ⚠ sollte V_12 sein → korrigieren
mouse_gut_S3_R2.fq.gz     → sample=mouse ...                 ⚠ Konvention uneindeutig → korrigieren
```

**Automuster kann nicht jede Namenskonvention raten** — deshalb ist die Tabelle
editierbar: Vorschlag + manuelle Korrektur. Bei einheitlicher Benennung (S1_L001_R1) ist
fast nichts zu korrigieren; bei uneinheitlicher korrigiert man die Sample-Spalte einmal
pro Sample (Copy-Paste über gleiche Samples).

**Tipp für die Zukunft:** Wenn die Benennung von Anfang an dem Schema
`YYYYMMDD_sampleID_type_v01` folgt (siehe Handout), erkennt das Automuster fast alles —
gute Benennung zahlt sich hier direkt aus.

## Pfade — offen für alle Systeme

Der `pfad` im Manifest ist **relativ zum Projektordner** (`data/raw/S1_R1.fastq`), nicht
absolut. Das ist portabel über Linux/Windows/Mac/IP — der absolute Ort darf sich ändern,
das Manifest bleibt gültig. Optional zusätzlich **md5**: identifiziert die Datei über
ihren Inhalt, überlebt Umbenennen und Verschieben.

## Die Kategorien der App (nach Web-Standards)

Etablierte Gliederung (aus ISA, DataCite, MIABIS, FHIR):

| Kategorie | Inhalt | Standard | In der App |
|---|---|---|---|
| Administrativ | Titel, Autor, ORCID, Abstract, Förderung | **DataCite** | teils (→ LMU-Generator) |
| **Data links / Manifest** | Datei ↔ Sample ↔ Pfad | SDRF / RO-Crate | ✅ **jetzt neu** |
| Biologisch | Organismus, Gewebe, Krankheit | ISA / Ontologien | ✅ |
| Technisch | Instrument, Library, Protokoll | ISA / MIABIS | ✅ |
| Experimentelles Design | Bedingung, Zeitpunkt, Faktoren | ISA Factors | ✅ |
| Klinisch | Diagnose, Phänotyp | FHIR | ✅ (Profil) |
| Provenienz | welches Script, wann, wer | RO-Crate / PROV | ✅ |
| Lizenz & Zugang | Lizenz, Sensitivität, DSB | DataCite / DUO | ✅ |

Was noch fehlt: **Administrativ voll (DataCite)** — dafür gibt es den fertigen
[LMU-DataCite-Generator](https://www.datacite-metadatengenerator.gwi.uni-muenchen.de/);
die App verweist darauf statt zu duplizieren.

## Wie das Manifest ins Forschungsobjekt kommt

Das Manifest ist die Vorstufe der RO-Crate-Verknüpfung:
- Manifest-Zeile → RO-Crate `File`-Entity
- `sample`-Spalte → `about` (welches Sample die Datei beschreibt)
- so entsteht das formale Nesting Datei ↔ Sample im maschinenlesbaren Objekt

`arc/make_arc.py` kann das lesen — die Brücke ist gebaut.

## Am realen Projekt (A03) anpassen

Die App gehört zum Bundle und wird **pro Projekt angepasst**. Für A03 (Triple RNA-seq)
zeigt sich die konkrete Struktur: mehrere Organismen pro Sample, counts pro Organismus.
Dort wird die Manifest-Funktion an der echten Namenskonvention und der echten
Sample-Datei-Beziehung feinjustiert — das universelle Gerüst steht, die Feinheit kommt am
Fall.
