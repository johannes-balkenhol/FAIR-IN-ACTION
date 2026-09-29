#!/usr/bin/env python3
"""
sdrf_to_isa.py — liest eine echte ArrayExpress MAGE-TAB (SDRF+IDF) und baut das ISA-Modell.

    python3 sdrf_to_isa.py --idf E-MTAB-XXXXX.idf.txt --sdrf E-MTAB-XXXXX.sdrf.txt

Das ist der Beweis, dass das ISA-Modell aus echten, akzeptierten Metadaten entsteht —
nicht aus Fantasie. MAGE-TAB → ISA → (weiter zu RO-Crate und ARC).
"""
import csv, re, argparse, sys
from isa_model import Investigation, Study, Assay, Sample, Characteristic, OntologyTerm

def parse_idf(path):
    """IDF = Investigation-Ebene: Titel, Beschreibung, Personen, Protokolle."""
    d = {}
    for row in csv.reader(open(path), delimiter='\t'):
        if row and row[0].strip():
            d[row[0].strip()] = [c for c in row[1:] if c.strip()]
    inv = Investigation(
        identifier=(d.get("Investigation Title", ["study"])[0][:40].replace(" ", "_")),
        title=(d.get("Investigation Title", [""])[0]),
        description=(d.get("Experiment Description", [""])[0]),
    )
    # Personen
    firsts = d.get("Person First Name", []); lasts = d.get("Person Last Name", [])
    roles = d.get("Person Roles", [])
    for i, last in enumerate(lasts):
        inv.people.append({"name": f"{firsts[i] if i<len(firsts) else ''} {last}".strip(),
                           "role": roles[i] if i < len(roles) else ""})
    # Protokolle
    pnames = d.get("Protocol Name", []); ptypes = d.get("Protocol Type", [])
    pdescs = d.get("Protocol Description", [])
    protocols = []
    for i, pn in enumerate(pnames):
        protocols.append({"name": pn,
                          "type": ptypes[i] if i < len(ptypes) else "",
                          "description": pdescs[i] if i < len(pdescs) else ""})
    inv._protocols = protocols
    inv.license = (d.get("Comment[Licence]", d.get("Comment[License]", [""])) or [""])[0]
    for k in d:
        if k.startswith("Comment[") and "Accession" in k or k=="Investigation Accession":
            inv.identifiers[k] = d[k][0] if d[k] else ""
    return inv, protocols

def parse_sdrf(path):
    """SDRF = Sample/Assay-Ebene: eine Zeile pro Library, Characteristics + Files."""
    rows = list(csv.reader(open(path), delimiter='\t'))
    header = rows[0]; data = rows[1:]
    # Spalten-Indizes finden
    def idxs(pattern):
        return [i for i,c in enumerate(header) if re.match(pattern, c)]
    src_i = header.index("Source Name") if "Source Name" in header else 0
    char_cols = [(i, re.match(r'Characteristics\[(.+)\]', header[i]).group(1))
                 for i in range(len(header)) if header[i].startswith("Characteristics[")]
    file_cols = [i for i,c in enumerate(header) if "Data File" in c or c=="Array Data File"]
    factor_cols = [(i, re.match(r'Factor Value\[(.+)\]', header[i]).group(1))
                   for i in range(len(header)) if header[i].startswith("Factor Value[")]
    # Term Source / Accession folgen oft direkt auf ein Characteristic
    def term_after(i):
        # sucht 'Term Source REF' und 'Term Accession Number' kurz nach Spalte i
        src = acc = ""
        for j in range(i+1, min(i+3, len(header))):
            if header[j] == "Term Source REF": src = None  # value kommt aus Zeile
            if header[j] == "Term Accession Number": acc = None
        return src, acc

    samples = {}
    files_all = []
    for r in data:
        sid = r[src_i] if src_i < len(r) else "sample"
        if sid not in samples:
            s = Sample(sample_id=sid)
            for ci, cname in char_cols:
                val = r[ci] if ci < len(r) else ""
                if not val: continue
                # Ontologie: schau ob direkt danach Source/Accession stehen
                onto = None
                if ci+2 < len(header) and header[ci+1]=="Term Source REF":
                    srcv = r[ci+1] if ci+1<len(r) else ""
                    accv = r[ci+2] if ci+2<len(r) else ""
                    if srcv or accv:
                        onto = OntologyTerm(label=val, accession=accv, source=srcv)
                s.characteristics.append(Characteristic(category=cname, value=val, ontology=onto))
            for fi, fname in factor_cols:
                if fi < len(r) and r[fi]:
                    s.factors[fname] = r[fi]
            samples[sid] = s
        for fi in file_cols:
            if fi < len(r) and r[fi]:
                files_all.append(r[fi])
    factor_names = [fn for _, fn in factor_cols]
    return list(samples.values()), files_all, factor_names

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idf", required=True); ap.add_argument("--sdrf", required=True)
    ap.add_argument("-o", "--out", default="isa.json")
    a = ap.parse_args()
    inv, protocols = parse_idf(a.idf)
    samples, files, factors = parse_sdrf(a.sdrf)
    study = Study(study_id=inv.identifier or "study", title=inv.title,
                  description=inv.description, samples=samples,
                  protocols=protocols, factors=factors)
    assay = Assay(assay_id="assay1", measurement_type="RNA sequencing",
                  technology="nucleotide sequencing",
                  samples=[s.sample_id for s in samples], raw_files=files)
    study.assays = [assay]
    inv.studies = [study]
    inv.to_isa_json(a.out)
    print(f"  MAGE-TAB → ISA:  {len(samples)} samples, {len(files)} files, "
          f"{len(protocols)} protocols, factors={factors}")
    print(f"  → {a.out}")
    return inv

if __name__ == "__main__":
    main()
