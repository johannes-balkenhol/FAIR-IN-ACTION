#!/usr/bin/env python3
"""
extractors/fcs.py — fill `source: auto` fields from FCS files.

    python3 extractors/fcs.py data/raw/*.fcs

This is the most satisfying extractor in the toolkit, because nearly all of flow
cytometry's technical metadata is ALREADY INSIDE THE FILE — $CYT, $DATE, $OP,
$TOT, $PAR, the full detector/fluorochrome list in $PnN/$PnS, and the spillover
matrix — and it is nonetheless typed by hand into a spreadsheet, every week, in
almost every lab on earth.

No dependencies. FCS 3.0/3.1 TEXT segment parsing is ~40 lines.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, sys


def parse_fcs(p: pathlib.Path):
    with open(p, "rb") as f:
        header = f.read(58).decode("ascii", "replace")
        if not header.startswith("FCS"):
            print(f"  ! {p.name}: not an FCS file", file=sys.stderr)
            return None
        version = header[:6].strip()
        t_start, t_end = int(header[10:18]), int(header[18:26])
        f.seek(t_start)
        text = f.read(t_end - t_start + 1).decode("latin-1")

    delim, body = text[0], text[1:]
    parts = body.split(delim)
    kw = {parts[i].strip(): parts[i + 1].strip()
          for i in range(0, len(parts) - 1, 2) if parts[i].strip()}

    npar = int(kw.get("$PAR", 0) or 0)
    panel = []
    for i in range(1, npar + 1):
        detector = kw.get(f"$P{i}N", "")          # detector, e.g. BV421-A
        marker   = kw.get(f"$P{i}S", "")          # the antigen, e.g. CD11c
        if not marker and detector.upper() in ("FSC-A", "FSC-H", "SSC-A", "SSC-H", "TIME"):
            continue                              # scatter/time: not markers
        panel.append({"detector": detector, "marker": marker or None,
                      "voltage": kw.get(f"$P{i}V", "")})

    spill = kw.get("$SPILLOVER") or kw.get("SPILL") or ""
    return {
        "file_name":    p.name,
        "file_type":    "fcs",
        "file_role":    "raw",
        "size_bytes":   p.stat().st_size,
        "fcs_version":  version,
        "fcs_run.cytometer":        kw.get("$CYT", ""),
        "fcs_run.acquisition_date": kw.get("$DATE", ""),
        "fcs_run.operator":         kw.get("$OP", ""),
        "fcs_run.n_events":         int(kw.get("$TOT", 0) or 0),
        "fcs_run.compensation":     "matrix in FCS" if spill else "none",
        "panel.n_parameters":       npar,
        "panel.markers":            panel,
        "_experiment": kw.get("$EXP", ""),
        "_cytometer_serial": kw.get("$CYTSN", ""),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--md5", action="store_true")
    a = ap.parse_args()

    files = []
    for p in a.paths:
        pp = pathlib.Path(p)
        files += sorted(pp.rglob("*.fcs")) if pp.is_dir() else [pp]

    recs = [r for f in files if f.is_file() and (r := parse_fcs(f))]
    if not recs:
        raise SystemExit("no readable FCS files")

    if a.md5:
        for f, r in zip(files, recs):
            r["checksum_md5"] = hashlib.md5(f.read_bytes()).hexdigest()

    try:
        import yaml
        print(yaml.safe_dump({"files": recs}, sort_keys=False, allow_unicode=True))
    except ImportError:
        print(json.dumps({"files": recs}, indent=2))

    r = recs[0]
    named = [m for m in r["panel.markers"] if m["marker"]]
    print(f"\n  {len(recs)} FCS file(s) read → cytometer, date, operator, event count, "
          f"compensation and a {len(named)}-marker panel, all without asking anyone.",
          file=sys.stderr)
    print(f"  panel: {', '.join(m['marker'] for m in named[:8])}"
          f"{' …' if len(named) > 8 else ''}", file=sys.stderr)
    print("\n  STILL REQUIRED FROM A HUMAN — and only from a human:", file=sys.stderr)
    print("    · antibody CLONE per marker  (different clones give different answers;", file=sys.stderr)
    print("      the FCS file does not know, and this is the field everyone omits)", file=sys.stderr)
    print("    · gating strategy            (MIFlowCyt requires it; without the gating", file=sys.stderr)
    print("      hierarchy a flow figure cannot be evaluated at all)", file=sys.stderr)


if __name__ == "__main__":
    main()
