# FAIR in action

**Forschungsdaten so aufbereiten, dass sie wiederverwendbar sind — von der ersten Messung
bis zur zitierbaren, europafähigen Veröffentlichung.** Für jede Disziplin: Lebenswissen-
schaften, Medizin, Sozialwissenschaften, Physik, und mehr. Für Menschen wie für KI.

Die meisten FAIR-Anleitungen sagen Forschenden, *was* zu tun ist, und lassen sie damit
allein. Dieses System macht das Gegenteil: Es füllt aus, was es aus den Daten und dem
Projekt selbst füllen kann, und fragt eine Person nur nach dem, was **nur sie** wissen
kann. Und es ist so gebaut, dass jedes so aufgesetzte Projekt am Ende ein sauberes,
zitierbares, konsortiumsweit verknüpfbares Objekt ist.

---

## Das Ziel — allgemein, nicht auf ein Fach beschränkt

Jede Studie, jedes Experiment, jede Erhebung erzeugt Daten. Ob Genomsequenzen, Mikroskopie-
bilder, Umfragen, Sensordaten oder klinische Befunde — sie sind nur dann wiederverwendbar,
wenn sie **findbar, zugänglich, interoperabel und nachnutzbar** sind (FAIR), und bei
personenbezogenen Daten zusätzlich **datenschutzkonform** (GDPR).

Der Kern in einem Satz: **Jedes Metadatum wird beantwortet von der Maschine** (steht in den
Daten), **vom Projekt** (einmal festgelegt) **oder von einem Menschen** (nur er weiß es).
Nur das Letzte wird gefragt. Diese Liste kurz zu halten — kontrolliertes Vokabular nutzen,
Rohdaten schützen, alles verknüpfen — macht ein einmal richtig aufgesetztes Projekt danach
in allem billiger: Analyse, Berichte, Abschlussarbeiten, Anträge, ein Wissensgraph des
Konsortiums.

---

## Die Kette — am Anfang entschieden, nicht am Ende

Die zentrale Idee des Flagship-Ansatzes: **Die Reihenfolge steht am Projektstart fest, nicht
am Ende.**

```
Datenmanagementplan → Metadatenschema → Erfassungs-App → verpacktes Forschungsobjekt → Repository
```

Das **Repository** legt fest, welche Metadaten nötig sind, welcher Datentyp, welche Lizenz,
welche Aufbewahrungsfrist. Wählt man es früh, beantwortet das die meisten späteren Fragen.

---

## Die elf Schritte — von der Messung zum übertragbaren Verfahren

Das System folgt den elf Schritten, die ein Datensatz von der Werkbank bis zur
kontrollierten, europafähigen Veröffentlichung durchläuft. Schritt 1–8 machen **einen**
Datensatz fertig, Schritt 9 macht die Handhabung **wiederholbar**, Schritt 10–11 bringen
ihn aus der Einrichtung heraus.

| # | Schritt | Was das System dazu beiträgt |
|---|---|---|
| 1 | **Rechtsgrundlage / Ethik** klären (bei sensiblen Daten) | `bundle/clinical/` — Sensitivität zuerst, DSB-Freigabe |
| 2 | **Projekt aufsetzen** — Struktur, Benennung, DMP | `bundle/STACK.md`, das Handout, `init_project` |
| 3 | **Metadatenschema** wählen (pro Assay/Datentyp) | `profiles/`, die wachsende Schema-Datenbank |
| 4 | **Metadaten erfassen** — was die Maschine kann, automatisch | die **Erfassungs-App** (`app/metadata_app.html`) |
| 5 | **Kontrolliertes Vokabular** — Ontologie-Begriffe statt Freitext | OLS4-Anbindung in der App |
| 6 | **Rohdaten schützen** — unveränderlich, geprüft | Prinzip im Handout, `extractors/` |
| 7 | **Provenienz** — welches Script erzeugte welches Ergebnis | `docs/METADATA_HARMONIZATION.md` |
| 8 | **Verpacken** — RO-Crate / ARC (der NFDI-Standard) | `arc/`, `docs/SOP_make_rocrate.md` |
| 9 | **Wiederholbar machen** — SOP, dann Workflow, dann Automatisierung | die SOPs, der `agent/` |
| 10 | **National auffindbar** — Repository, DOI, kontrollierter Zugang | `docs/SCHEMA_DATABASE_DESIGN.md` (Export-Ziele) |
| 11 | **Europafähig** — beschreibbar für den europäischen Katalog | RO-Crate/ISA als Beiprodukt der Aufbereitung |

**Der Punkt:** Diese elf Schritte sind keine Checkliste für einen Datensatz. Sie sind das
Rohmaterial für **Verfahren, die andere Gruppen, Konsortien und Standorte übernehmen
können.** Ein gelöster Fall wird zur SOP, die SOP zum portablen Workflow, der Workflow zur
Automatisierung.

---

## Für wen ist was

### 🧑‍🔬 Ein Mensch (Studierende bis PI)
→ `bundle/START_HERE.md` → das Handout (1–2 Seiten) → die Worksheets.
Die Erfassungs-App fragt dich nur nach dem, was nur du weißt.

### 🤖 Eine KI (Claude, ChatGPT, lokal)
→ `bundle/STACK.md` lesen und befolgen. Bei sensiblen Daten: lokales Modell
(`bundle/clinical/LOCAL_AI_for_sensitive_data.md`) — nichts verlässt den Rechner.

### 🏛️ Ein Konsortium / eine Förderlinie
→ Diese README + `docs/` zeigen, dass die erzeugten Objekte auf die Standards **RO-Crate,
ISA und ARC** (NFDI/DataPLANT) hinauslaufen — also europafähig, ohne Neubau.

---

## Was im Repository ist

```
bundle/     Der Standard: Handout, STACK.md, SOPs, Worksheets, klinischer Pfad
profiles/   Metadaten-Schemas pro Assay (wächst aus echten Submissions)
app/        Die Erfassungs-App (HTML, läuft überall, keine Installation)
arc/        ISA-Modell + ARC-Converter — das verpackte Forschungsobjekt (NFDI-Standard)
agent/      FAIR-Auditor — prüft Projektordner, bewertet bronze/silber/gold
docs/       Design: Schema-Datenbank, DMP-Entscheidungsbaum, Harmonisierung, RO-Crate, ARC
```

---

## Die Erfassungs-App — für den täglichen Gebrauch

`app/metadata_app.html` — im Browser öffnen, keine Installation, läuft auf Linux, Windows,
Mac.

- **Öffnen, ausfüllen, schließen, wieder öffnen → ausgefüllte Felder bleiben** (Autosave im
  Browser).
- **Vorlage speichern** — den nächsten Experiment-Run startest du mit den Werten des
  letzten und änderst nur, was anders ist.
- **Datenordner öffnen** (Chrome/Edge) — die App sieht deine Rohdateien und schreibt die
  Metadaten als `<projekt>.meta.json` **neben die Rohdaten**. Auch ein altes Experiment
  lässt sich so nachträglich annotieren: Ordner öffnen → die App lädt, was schon da ist →
  du ergänzt.
- **Nur die bernsteinfarbenen Felder** musst du füllen; der Rest ist schon da — und
  trotzdem editierbar, falls die Maschine sich irrt.
- **Export** nach ArrayExpress, GEO, ENA, RO-Crate, oder als Lückenblatt für Mitarbeitende.

Was die Browser-App bewusst **nicht** kann und wo andere Werkzeuge helfen: Autor/Titel/
Abstract im DataCite-Format erzeugt der
[DataCite-Generator der LMU](https://www.datacite-metadatengenerator.gwi.uni-muenchen.de/);
für sehr tief in den Rechner integrierte Ordner-Workflows gibt es Desktop-Werkzeuge wie
MetaFold. Diese App bleibt bewusst plattformunabhängiges HTML.

---

## Standards, auf die alles hinausläuft

| Schicht | Standard |
|---|---|
| Metadaten-Modell | **ISA** (Investigation / Study / Assay) |
| Verpackung, maschinenlesbar | **RO-Crate** |
| Container-Struktur (NFDI/DataPLANT) | **ARC** |
| Vokabulare | NCBITaxon, UBERON, EFO, MONDO … (Lebenswiss.); je Fach eigene |
| Repositorien | ArrayExpress/ENA, PRIDE, BioImage Archive, EGA (kontrolliert), Zenodo … |

Bereitschaft ist nicht Konformität: Der Europäische Gesundheitsdatenraum (Verordnung (EU)
2025/327) gilt ab 2029, die technischen Spezifikationen entstehen noch. Ziel ist ein
Datensatz, der sich in **jede** endgültig geforderte Form bringen lässt — kein
Konformitätsanspruch.

---

## Lizenz & Kontakt

MIT (Code) · CC-BY-4.0 (Standard/Doku). Core Unit Research Data Management (cRDM),
Universität Würzburg — coreunitrdm@uni-wuerzburg.de
