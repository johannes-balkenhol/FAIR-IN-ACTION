#!/usr/bin/env python3
"""
extractors/fastq.py — fill every `source: auto` field from FASTQ files.

    python3 extractors/fastq.py data/raw/*.fastq.gz -o auto_fields.yaml
    python3 extractors/fastq.py data/raw/ --md5          # md5 is slow on big files

Covers bulk RNA-seq and 10x. The rule this enforces:

    IF A HUMAN IS EVER ASKED FOR A FIELD THIS SCRIPT COULD HAVE FILLED,
    THIS SCRIPT IS BROKEN.

Everything below is read from the first record of each file. It costs milliseconds
and it replaces a spreadsheet that someone fills in by hand, wrongly, every week,
in every sequencing facility on earth.
"""
from __future__ import annotations
import argparse, gzip, hashlib, json, pathlib, re, sys
from collections import defaultdict

# Illumina instrument-ID prefix -> model. EFO where a term exists.
INSTRUMENTS = [
    (re.compile(r"^A0"),      "Illumina NovaSeq 6000",  "EFO:0008563"),
    (re.compile(r"^LH"),      "Illumina NovaSeq X",     ""),
    (re.compile(r"^VH"),      "Illumina NextSeq 2000",  ""),
    (re.compile(r"^N[BS]"),   "Illumina NextSeq 500",   "EFO:0008565"),
    (re.compile(r"^M0"),      "Illumina MiSeq",         "EFO:0004205"),
    (re.compile(r"^[JK]0"),   "Illumina HiSeq 4000",    "EFO:0008564"),
    (re.compile(r"^D0"),      "Illumina HiSeq 2500",    "EFO:0008565"),
    (re.compile(r"^FS"),      "Illumina iSeq 100",      ""),
]

# 10x chemistry from R1 length: 16bp barcode + UMI
CHEM = {26: ("10x 3' v2", 16, 10), 28: ("10x 3' v3", 16, 12)}

HEADER = re.compile(
    r"^@(?P<instr>[^:]+):(?P<run>[^:]+):(?P<flowcell>[^:]+):(?P<lane>[^:]+):"
    r"(?P<tile>[^:]+):(?P<x>[^:]+):(?P<y>[^:\s]+)"
    r"(?:\s(?P<read>\d+):(?P<filt>[YN]):(?P<ctrl>\d+):(?P<index>\S+))?"
)

READ_TYPE = [(re.compile(r"_R1[_.]"), "read1"), (re.compile(r"_R2[_.]"), "read2"),
             (re.compile(r"_I1[_.]"), "index1"), (re.compile(r"_I2[_.]"), "index2")]


def _open(p: pathlib.Path):
    return gzip.open(p, "rt") if p.suffix == ".gz" else open(p)


def md5(p: pathlib.Path, chunk=1 << 22):
    h = hashlib.md5()
    with open(p, "rb") as f:
        while (b := f.read(chunk)):
            h.update(b)
    return h.hexdigest()


def read_one(p: pathlib.Path, want_md5=False):
    """Everything a human should never be asked about this file."""
    with _open(p) as f:
        head = f.readline().rstrip("\n")
        seq  = f.readline().rstrip("\n")
    m = HEADER.match(head)
    if not m:
        print(f"  ! {p.name}: header not Illumina-shaped, skipping "
              f"({head[:40]!r})", file=sys.stderr)
        return None
    g = m.groupdict()

    model = curie = ""
    for rx, name, efo in INSTRUMENTS:
        if rx.match(g["instr"] or ""):
            model, curie = name, efo
            break

    idx = (g.get("index") or "")
    index_lengths = [len(x) for x in idx.split("+") if x] if idx else []

    rt = "not applicable"
    for rx, label in READ_TYPE:
        if rx.search(p.name):
            rt = label
            break

    rec = {
        "file_name":    p.name,
        "file_type":    "fastq",
        "file_role":    "raw",
        "read_type":    rt,
        "size_bytes":   p.stat().st_size,
        "instrument":   f"{curie} {model}".strip(),
        "instrument_id": g["instr"],
        "run_id":       g["run"],
        "flowcell_id":  g["flowcell"],     # <- this IS your batch variable, and it is free
        "lane":         g["lane"],
        "read_length":  len(seq),
        "index_sequence": idx,
        "index_length": index_lengths,
    }
    if want_md5:
        rec["checksum_md5"] = md5(p)
    return rec


def summarise(recs):
    """Roll per-file records up to library / assay level."""
    if not recs:
        return {}
    by_type = defaultdict(list)
    for r in recs:
        by_type[r["read_type"]].append(r)

    layout = "PAIRED" if by_type["read2"] else "SINGLE"
    out = {
        "library.library_layout": layout,
        "assay.instrument":   recs[0]["instrument"],
        "assay.flowcell_id":  recs[0]["flowcell_id"],
        "assay.lane":         ",".join(sorted({r["lane"] for r in recs})),
        "assay.read_length":  sorted({r["read_length"] for r in recs}),
        "assay.index_length": recs[0]["index_length"],
        "library.index_sequence": recs[0]["index_sequence"],
        "derived.n_files":    len(recs),
    }

    # 10x: R1 length gives away the chemistry, the barcode read and the UMI length
    r1 = by_type["read1"]
    if r1:
        L = r1[0]["read_length"]
        if L in CHEM:
            chem, bc, umi = CHEM[L]
            out["library.chemistry"]    = chem
            out["library.barcode_read"] = "R1"
            out["library.umi_length"]   = umi
            out["_inferred_from"] = (f"R1 is {L} bp -> {chem} "
                                     f"({bc} bp barcode + {umi} bp UMI). "
                                     f"CONFIRM this with the facility.")

    # flowcell disagreement = more than one sequencing run in one folder
    fcs = {r["flowcell_id"] for r in recs}
    if len(fcs) > 1:
        out["_warning"] = (f"{len(fcs)} different flowcells in this set: "
                           f"{', '.join(sorted(fcs))}. That is a BATCH. "
                           f"Set assay.batch, or your integration will silently absorb it.")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="FASTQ files, or a directory")
    ap.add_argument("-o", "--out", help="write YAML here (default: stdout)")
    ap.add_argument("--md5", action="store_true", help="checksum every file (slow, but repositories require it)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    files = []
    for p in a.paths:
        pp = pathlib.Path(p)
        files += sorted(pp.rglob("*.fastq*")) if pp.is_dir() else [pp]
    files = [f for f in files if f.is_file()]
    if not files:
        raise SystemExit("no FASTQ files found")

    recs = [r for f in files if (r := read_one(f, a.md5))]
    summary = summarise(recs)

    warn = summary.pop("_warning", None)
    inf  = summary.pop("_inferred_from", None)

    doc = {"auto_fields": summary, "files": recs}
    text = json.dumps(doc, indent=2) if a.json else _yaml(doc)

    if a.out:
        open(a.out, "w").write(text)
    else:
        print(text)

    n = len(summary)
    print(f"\n  {len(recs)} file(s) read → {n} auto field(s) filled, "
          f"0 questions asked.", file=sys.stderr)
    if inf:
        print(f"  inferred: {inf}", file=sys.stderr)
    if warn:
        print(f"  ⚠ {warn}", file=sys.stderr)
    if not a.md5:
        print("  note: run with --md5 for checksums (required by every repository).",
              file=sys.stderr)


def _yaml(d):
    try:
        import yaml
        return yaml.safe_dump(d, sort_keys=False, default_flow_style=False)
    except ImportError:
        return json.dumps(d, indent=2)


if __name__ == "__main__":
    main()
