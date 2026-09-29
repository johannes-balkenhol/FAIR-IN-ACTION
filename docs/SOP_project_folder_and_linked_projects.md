# SOP — einen FAIR/GDPR-konformen Projektordner anlegen

*Die wiederverwendbare Anleitung, wie ein Projektordner aussehen muss, damit er FAIR- und
GDPR-konform ist — und wie zwei abhängige Projekte (z.B. Genom-Assembly → RNA-seq, das
darauf mappt) als getrennte, verlinkte Objekte organisiert werden. Die konkreten Befehle
führst du im jeweiligen Projekt-Chat aus; diese SOP sagt, WAS zu tun ist und WARUM.*

---

## Teil A — die FAIR-Ordnerstruktur (jedes Projekt)

```
PROJECT_NAME/
├── README.md            die Karte · Links (ELN, Genom, Git, Zenodo, DOI) · Reproduzierbarkeit
├── DMP.md               Datenmanagementplan · am START geschrieben
├── LICENSE              wie andere die Daten nutzen dürfen
│
├── data/
│   ├── raw_data/        erste Messung · READ-ONLY · checksummed · oder Link
│   ├── primary_data/    Rohdaten nutzbar gemacht (durch Code) · offene Formate
│   ├── secondary_data/  aus externen/anderen Projekten (z.B. die Referenz-Assembly)
│   └── meta_data/       das Metadaten-Schema · kontrolliertes Vokabular · Data-Links
│
├── documents/
│   ├── project_plan/    Plan · workflow.svg
│   ├── reports/         Zwischenergebnisse
│   ├── methods/         ELN-Link/-Datei
│   └── manuscript/      finales Manuskript
│
├── notebooks/  scripts/{python,bash}/  analysis/  results/  code/{cwl,nextflow}/
└── ro-crate-metadata.json   ← das FAIR-Objekt (am Ende)
```

**Die Regeln, die es FAIR machen:**
1. **Rohdaten sind unantastbar** — `raw_data/` read-only, checksummed.
2. **Eine Sample-ID überall** — im Dateinamen, ELN, Metadaten, jedem Link.
3. **Kontrolliertes Vokabular** — Ontologie-Begriffe statt Freitext.
4. **README = die Karte** — jeder Link (Daten, Code, ELN, Referenz) steht dort.
5. **DMP am Start** — legt Repository fest → das legt die Metadaten fest.

## Teil B — einen bestehenden, unordentlichen Ordner FAIR machen (wie A03)

Wenn ein Ordner schon existiert (Analyse gelaufen, aber chaotisch):

1. **NICHTS löschen/verschieben ohne Prüfung.** Erst kartieren, was da ist.
2. **Rohdaten identifizieren** → nach `raw_data/`, read-only setzen, Checksums prüfen.
3. **Prozessierte Daten** → `primary_data/` (durch Code erzeugt) / `secondary_data/`
   (extern).
4. **Zwischenergebnisse** → `analysis/`, finale → `results/`.
5. **Scripts/Notebooks** sortieren: `notebooks/`, `scripts/python/`, `scripts/bash/`.
6. **Metadaten** → `meta_data/`, mit der App füllen.
7. **README + DMP + LICENSE** ergänzen, falls fehlen.
8. **Gates prüfen** (G1 teilen / G2 publizieren).

⚠️ **Bei sensiblen Daten (Patienten):** ZUERST Sensitivität klären, nichts in die Cloud,
DSB-Freigabe — siehe `clinical/`. (Dein aktueller Fall: offene Daten, kein Problem.)

## Teil C — zwei verlinkte Projekte (Genom-Assembly → RNA-seq)

*Dein Fall: PacBio-Genom (Projekt 1, fertig, muss FAIR-strukturiert werden) → RNA-seq
mappt darauf (Projekt 2, neu). Zwei getrennte FAIR-Objekte, verbunden.*

### Warum getrennt

- **Verschiedene Repositories:** Genom → ENA + NCBI Assembly (GCA_…). RNA-seq →
  ArrayExpress. Ein Ordner kann nicht beide Standards erfüllen.
- **Verschiedene Assays:** Genom = DNA/WGS/long-read (`pacbio-genome.yaml`). RNA-seq =
  RNA/transcriptomic (`bulk-rnaseq.yaml`).
- **Unabhängige Nachnutzung:** Das Genom ist eine Ressource für sich.

### Die Struktur

```
Projects_shared/
├── PacBio_<organism>_genome/         ← Projekt 1
│   ├── data/raw_data/        die HiFi-Reads
│   ├── data/primary_data/    genome.fasta + annotation.gff  ← das Produkt
│   ├── data/meta_data/       pacbio-genome-Schema
│   └── README.md · DMP.md · LICENSE · ro-crate-metadata.json
│
└── <organism>_RNAseq/                ← Projekt 2 (mappt auf Projekt 1)
    ├── data/raw_data/        die RNA-FASTQs
    ├── data/secondary_data/
    │   └── reference/        ← die Assembly-Kopie: genome.fasta + annotation.gff
    │                           (physisch kopiert aus Projekt 1)
    ├── data/meta_data/       bulk-rnaseq-Schema
    │       combined_reference: "PacBio_<organism>_genome v1 (GCA_… nach Deposition)"
    └── README.md             ← "reference genome: siehe PacBio_<organism>_genome / GCA_…"
```

### Die Verlinkung — der Kernpunkt

Das RNA-seq **kopiert die Referenz** nach `secondary_data/reference/` (genome.fasta +
annotation.gff) UND **hält die Herkunft in den Metadaten fest**:

| Wo | Was |
|---|---|
| `secondary_data/reference/` | die physische Kopie: `genome.fasta` + `annotation.gff` |
| `meta_data/` `combined_reference` | die exakte Version + (nach Deposition) die GCA-Accession |
| `README.md` | "Referenzgenom: PacBio_<organism>_genome, Assembly v1, GCA_… — dieses Projekt mappt darauf" |

**Warum die Kopie + die Accession:** Die Kopie macht das RNA-seq-Projekt selbst-enthalten
(man kann es reproduzieren, ohne das PacBio-Projekt zu haben). Die Accession macht es
maschinen-verlinkbar (ein Werkzeug findet das exakte Genom). Beides zusammen = reproduzierbar
UND verlinkt.

### Die Reihenfolge

1. **PacBio-Ordner FAIR-strukturieren** (Teil B — aufräumen) → Assembly nach `primary_data/`
2. **PacBio-Assembly deponieren** → ENA + NCBI Assembly → `GCA_…` bekommen
3. **RNA-seq-Ordner neu anlegen** (Teil A) → die Referenz aus Projekt 1 nach
   `secondary_data/reference/` kopieren
4. **combined_reference** = `GCA_…` in den RNA-seq-Metadaten eintragen
5. **Beide verlinken** in README + RO-Crate

Bis die GCA-Accession da ist: `combined_reference: "lokale Assembly v1, GCA pending"`,
später ersetzen.

## Teil D — Sync HPC ↔ Nextcloud

- **Daten leben auf dem HPC** (die Analyse läuft dort), Nextcloud spiegelt die
  human-lesbaren Teile.
- **rsync mit Vorsicht:** immer erst `rsync -avn` (dry-run), lesen, dann echt.
- **`.git` NICHT syncen** (Nextcloud-Client: `.git` ausschließen), sonst Korruption.
- **Große Rohdaten** bleiben oft nur auf dem HPC; Nextcloud bekommt README, Metadaten,
  kleine Ergebnisse — nicht die BAMs/FASTQs.

## Teil E — zum FAIR-Objekt

Wenn der Ordner strukturiert + Metadaten gefüllt sind:
1. Metadaten-App: Profil laden, Felder füllen, Data-Links, Export (SDRF/IDF für RNA-seq;
   ENA-Format fürs Genom)
2. Scripts mit maschinenlesbaren `INPUTS`/`OUTPUTS`-Headern → automatische Provenienz
3. `arc/fair_to_arc.sh` → RO-Crate / ARC
4. Deponieren, Accession/DOI in README + RO-Crate eintragen, beide Projekte verlinken

---

*Diese SOP ist die Vorlage für jeden neuen oder aufzuräumenden Projektordner. Für verlinkte
Projekte (wie Genom→RNA-seq) sorgt Teil C dafür, dass beide getrennte, saubere,
verbundene FAIR-Objekte werden — reproduzierbar und maschinen-navigierbar.*
