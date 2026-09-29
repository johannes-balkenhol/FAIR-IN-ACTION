# Verlinkte Projekte — PacBio-Genom → RNA-seq

*Wenn ein RNA-seq-Projekt auf ein frisch assembliertes Genom mappt, sind das ZWEI
FAIR-Objekte, verbunden über die Assembly-Accession. So bleibt beides reproduzierbar.*

## Die Kette

```
PROJEKT 1: PacBio Genom-Sequenzierung
  Rohdaten (HiFi reads) ──▶ Assembly (hifiasm/flye) ──▶ Annotation (Prokka/Bakta)
                                    │
                              genome_accession (GCA_…)  ← die Brücke
                                    │
                                    ▼
PROJEKT 2: RNA-seq
  Rohdaten (FASTQ) ──▶ Mapping auf DIESES Genom ──▶ Counts pro Gen
                              │
                       combined_reference = die exakte Assembly-Version + Accession
```

## Warum zwei getrennte Objekte (nicht eins)

- **Verschiedene Repositories:** Genom → ENA + NCBI Assembly (GCA_…). Expression →
  ArrayExpress (brokert Reads zu ENA). Ein Projekt kann nicht beide Standards erfüllen.
- **Verschiedene Assays:** Genom = DNA/WGS/long-read. RNA-seq = RNA/transcriptomic. Andere
  Schemas (profiles/pacbio-genome.yaml vs profiles/bulk-rnaseq.yaml).
- **Unabhängige Nachnutzung:** Das Genom ist eine Ressource für sich — andere können darauf
  mappen, ohne dein RNA-seq zu brauchen.

## Die Brücke — was das RNA-seq-Schema vom Genom braucht

Im RNA-seq-Projekt MUSS die Referenz exakt festgehalten werden (sonst nicht reproduzierbar):

| RNA-seq-Feld | Wert aus dem PacBio-Projekt |
|---|---|
| `combined_reference` / `reference_genome` | die exakte Assembly (GCA_… + Version) |
| Referenz-`.fasta` | das `genome_fasta` aus Projekt 1 |
| Referenz-`.gff` | das `annotation_gff` aus Projekt 1 |
| Link zum Genom-Projekt | dessen genome_accession / DOI |

**Die Regel:** Das RNA-seq referenziert die Assembly über ihre **Accession + Version**,
nicht über einen lokalen Pfad. Ein Pfad wie `/home/…/genome.fa` ist nicht reproduzierbar;
`GCA_XXXXXXXXX.1` ist es.

## Reihenfolge der Deposition

**Zuerst das Genom deponieren, dann RNA-seq.** Weil RNA-seq die Genom-Accession
referenzieren muss:

1. **PacBio-Projekt fertigstellen** → ENA (Reads) + NCBI/ENA Assembly (GCA_…) →
   genome_accession bekommen
2. **RNA-seq-Projekt** → die genome_accession als combined_reference eintragen → zu
   ArrayExpress
3. **Beide verlinken** in ihren README/RO-Crate: RNA-seq → "reference: GCA_…";
   Genom → "used by: E-MTAB-… (RNA-seq)"

## Status (dein Fall)

- PacBio-Assembly: **noch nicht deponiert, liegt lokal auf dem HPC** → Schritt 1 steht aus
- RNA-seq: neues Projekt → wartet auf die genome_accession aus Schritt 1

**Empfehlung:** Setz das PacBio-Projekt ZUERST auf (profiles/pacbio-genome.yaml),
deponiere die Assembly, dann referenziert das RNA-seq sie sauber. Bis die Accession da ist,
trägst du im RNA-seq `combined_reference: "<lokale Assembly v1, GCA pending>"` ein und
ersetzt es nach der Genom-Deposition.

## Beide als RO-Crate / ARC

Jedes Projekt wird sein eigenes FAIR-Objekt (RO-Crate/ARC). Die Verlinkung im RO-Crate:
das RNA-seq-Objekt nennt das Genom-Objekt in `mentions`/`isBasedOn` mit dessen DOI/Accession.
So ist die Provenienz-Kette maschinenlesbar — ein Werkzeug kann von den RNA-seq-Counts
zurück zur exakten Genom-Version navigieren.
