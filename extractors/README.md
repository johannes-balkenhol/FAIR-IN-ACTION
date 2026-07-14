# Extractors

One per assay. Each fills every `source: auto` field in its profile — and nothing else.

**The rule: if a human is ever asked for a field an extractor could have filled, the
extractor is broken.** That is the only measure of success here.

| Assay | Extractor | Reads | Status |
|---|---|---|---|
| bulk / 10x RNA-seq | `fastq.py` | FASTQ headers | ✅ |
| flow cytometry | `fcs.py` | FCS `$CYT` `$DATE` `$OP` `$TOT` `$PnN`/`$PnS` `$SPILLOVER` | ✅ |
| scRNA-seq processed | `h5ad.py` | h5ad `.obs`, `.X`, cell/gene counts | ❌ |
| proteomics MS/MS | `ms_raw.py` | raw headers, DIA-NN / MaxQuant report | ❌ |

## Usage

```bash
python3 extractors/fastq.py data/raw/ --md5 -o auto_fields.yaml
python3 extractors/fcs.py   data/raw/*.fcs
```

## What they find that you would not

`fastq.py` reports the **flowcell ID of every file**, and warns when a directory
contains more than one:

```
⚠ 2 different flowcells: HFWFVDMXX, HFWXYZABC.
  That is a BATCH. Set assay.batch, or your integration will silently absorb it.
```

Nobody spots that by looking at filenames. It is free, it is in the header of every
read, and it is the single most common invisible confounder in sequencing.

`fcs.py` reads the cytometer, acquisition date, operator, event count, compensation
and the full marker panel — all of which are already **inside the file**, and all of
which are nonetheless typed into a spreadsheet by hand, every week, in almost every
lab on earth.

## What they deliberately do NOT do

They do not guess. `fastq.py` infers 10x chemistry from R1 length (28 bp → v3) and
says so out loud — `CONFIRM this with the facility` — rather than writing it in
silently. An extractor that quietly guesses is worse than one that asks.
