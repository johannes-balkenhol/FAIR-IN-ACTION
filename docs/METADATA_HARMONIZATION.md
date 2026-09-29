# Metadaten-Harmonisierung — was von Hand annotiert wird und was das Script mitliefert

*Die Kern-Einsicht des ganzen Systems, in einem Dokument. Sie beantwortet die schwerste
Frage der Metadaten-Erfassung: Wie harmonisiert man geschachtelte, projektspezifische,
extrem diverse Metadaten? Antwort: **Man harmonisiert prozessierte Daten NICHT von Hand —
man liefert das Script mit, das sie erzeugt hat.***

---

## Das Problem

Metadaten sind der schwierige Teil, und der schwierigste Teil davon ist: **prozessierte
Daten haben beliebig diverse Annotationen, die sich nicht standardisieren lassen.**

Beispiele:
- Eine `.h5ad` (Single-Cell) hat beliebig viele `.obs`-Spalten: Cluster-Namen ("kidney
  cluster 3"), Zelltypen, Conditions, QC-Metriken — projektspezifisch, tausendfach
  verschieden. Ein festes Schema kann das nicht fassen.
- Eine Count-Matrix, ein DE-Ergebnis, eine segmentierte Bilddatei — alle tragen
  Annotationen, die das *Ergebnis der Analyse* sind, nicht standardisierbare Metadaten.

Man kann diese diversen, geschachtelten Annotationen **nicht** in ein relationales Schema
zwingen. Der Versuch führt entweder zu Datenverlust (man lässt weg, was nicht passt) oder
zu erfundenen Feldern (man presst rein, was nicht reingehört).

## Die Lösung — zwei Ebenen, unterschiedlich behandelt

```
┌─ ROHDATEN ────────────────────────────────────────────────────────┐
│  FASTQ · raw images · .fcs · raw MS                                │
│      ↓                                                              │
│  STRUKTURIERTE METADATEN (das feste Schema, Ontologie-gebunden)    │
│  organism · condition · instrument · library · protocol · …        │
│  ← DAS wird in der App erfasst, harmonisiert, standardisiert       │
│  ← reproduzierbar, weil endlich und kontrolliert                   │
└────────────────────────────────────────────────────────────────────┘
                          │
                    das SCRIPT (im Bundle, versioniert in git)
                          │  erzeugt & dokumentiert
                          ▼
┌─ PRIMÄR- / SEKUNDÄRDATEN (prozessiert) ───────────────────────────┐
│  .h5ad · count-Matrix · DE-Ergebnis · segmentierte Bilder         │
│      ↓                                                              │
│  NICHT von Hand annotiert.                                         │
│  Die Provenienz = das Script, das sie aus den Rohdaten erzeugte.  │
│  Die diversen .obs-Annotationen bleiben, wie sie sind — sie sind  │
│  das Analyse-Ergebnis, nicht standardisierbare Metadaten.         │
└────────────────────────────────────────────────────────────────────┘
```

**Die Regel:**

1. **Rohdaten annotiert man** — mit dem festen Schema, Ontologie-gebunden, in der App.
   Das ist endlich, kontrolliert, harmonisierbar.
2. **Prozessierte Daten annotiert man NICHT neu.** Man **bündelt sie mit dem Script**,
   das sie erzeugt hat. Das Script *ist* die Provenienz und die "Annotation".
3. **Das Bundle-Script harmonisiert** primär/sekundär, weil es weiß, wie sie aus den
   Rohdaten entstanden — nicht, weil jemand die h5ad-Spalten von Hand standardisiert hat.

## Warum das die einzige ehrliche Lösung ist

Eine prozessierte Datei ist reproduzierbar **genau dann, wenn** man Rohdaten + Script +
Umgebung hat. Dann sind ihre Annotationen egal — man kann sie jederzeit neu erzeugen. Die
Standardisierung der prozessierten Annotationen ist damit nicht nur schwer, sondern
**unnötig**: Das Script leistet, was die Standardisierung leisten sollte — Nachvollzieh-
barkeit.

Das ist die **RO-Crate-Logik in Reinform:**
> Rohdaten + strukturierte Metadaten + das Script, das den Rest erzeugt = das vollständige,
> reproduzierbare Objekt.

## Was am Sample verbunden wird

Alle Metadaten-Ebenen hängen an der **Sample-ID** und werden vom Script mit den
prozessierten Daten gebündelt:

| Ebene | Quelle | Wie erfasst |
|---|---|---|
| Rohdaten-Metadaten | die Datei selbst | Maschine → auto (Extractor) |
| experimentelles Protokoll | ELN-Eintrag / .docx | extrahiert, nicht neu getippt |
| Maschinen-Metadaten | Instrument-Header/Log | auto |
| personal | Projekt-Config | einmal |
| technical | Pipeline-Config/Log | auto/project |
| clinical (falls) | FHIR, kontrolliert | human, kontrollierter Zugang |

→ Diese verbundenen Rohdaten-Metadaten + **das Script** + die prozessierten Daten = das
gebündelte, harmonisierte Objekt (die RO-Crate).

## Mehrere Modalitäten in einem Projekt (z.B. Imaging + klinisch)

Getrennt behandeln, über die Sample-ID verbunden — **nicht** ein Monster-Schema:

- Imaging-Daten → REMBI-Schema
- klinische Daten → FHIR-Schema
- **eine** DATAFINDER-Tabelle verknüpft beide über die gemeinsame Sample-ID

Verschiedene Standards, ein Projekt — genau wie ArrayExpress (Experiment) + ENA (Reads)
aus einer Submission. Die Sample-ID ist der Faden durch alle Modalitäten.

## Für die Praxis (das Script im Bundle)

Das Harmonisierungs-Script (pro Assay, wächst per Projekt) leistet:

1. liest die Rohdaten-Metadaten (das feste Schema) am Sample
2. dokumentiert die Pipeline-Schritte (welches Script, welche Umgebung, welche Version)
3. bündelt prozessierte Daten **mit** dieser Provenienz — nicht mit neuen Annotationen
4. schreibt die RO-Crate: Rohdaten-Metadaten + Script-Provenienz + Datei-Zeiger

**Das Script wird nicht im Voraus gebaut, sondern am realen Projekt** (z.B. A03: mouse +
E10 + phage, counts pro Organismus). Dort zwingt die Realität die konkrete Lösung — statt
sie abstrakt zu raten.

---

*Diese Einsicht ist der Grund, warum das Bundle ein Script-Layer hat und nicht versucht,
alles in ein Schema zu pressen. Rohdaten sind endlich und harmonisierbar; prozessierte
Daten sind divers und reproduzierbar. Das eine annotiert man, das andere liefert man mit
seinem Script. Beides zusammen ist FAIR.*
