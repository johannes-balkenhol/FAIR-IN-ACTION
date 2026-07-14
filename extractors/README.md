# Extractors

One per assay. Each fills every `source: auto` field in its profile — and nothing else.

**The rule: if a human is ever asked for a field an extractor could have filled, the
extractor is broken.** That is the only measure of success here.

| Assay | Extractor | Reads | Status |
|---|---|---|---|
| scRNA-seq (10x) | `fastq_10x.py` | FASTQ headers, h5ad | ❌ |
| bulk / dual RNA-seq | `fastq_bulk.py` | FASTQ headers, aligner logs | ❌ |
| proteomics MS/MS | `ms_raw.py` | raw file headers, DIA-NN/MaxQuant report | ❌ |
| flow cytometry | `fcs.py` | FCS keywords — `$CYT`, `$DATE`, `$OP`, `$SPILLOVER`, `$PnN`/`$PnS` | ❌ |

The FCS one is the easiest and most satisfying: nearly all of flow's technical
metadata is already *inside the file*, and is nonetheless typed by hand into a
spreadsheet in most labs, every week, everywhere.
