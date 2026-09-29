#!/usr/bin/env python3
"""
make_arc.py — baut aus einem FAIR-in-action Projekt eine ARC (Annotated Research Context).

    python3 make_arc.py --project /pfad/zum/projekt --out /pfad/zur/ARC

Nimmt: die ISA-JSON (aus sdrf_to_isa.py) + die Projektdateien.
Erzeugt: die ARC-Ordnerstruktur mit ISA-Metadaten, Workflows, RO-Crate.

ARC-Struktur (DataPLANT-Konvention):
  ARC/
  ├── isa.investigation.xlsx    (hier: isa.investigation.json — xlsx braucht arctrl)
  ├── studies/<id>/isa.study.json
  ├── assays/<id>/isa.assay.json + dataset/  (Rohdaten oder Links)
  ├── workflows/                (Scripts/Pipelines — CWL)
  ├── runs/                     (prozessierte Ergebnisse)
  └── ro-crate-metadata.json    (die RO-Crate-Schicht)

WICHTIG (Harmonisierungs-Prinzip): assays/ enthält ROHDATEN + Metadaten.
runs/ enthält prozessierte Daten, die per workflows/ erzeugt wurden — NICHT neu annotiert.
"""
import json, argparse, pathlib, shutil, sys

def build_arc(isa_json_path, project_dir, out_dir, link_raw=True):
    isa = json.load(open(isa_json_path))
    out = pathlib.Path(out_dir)
    proj = pathlib.Path(project_dir) if project_dir else None
    # ARC-Skelett
    for d in ["studies", "assays", "workflows", "runs"]:
        (out / d).mkdir(parents=True, exist_ok=True)

    # 1. Investigation
    (out / "isa.investigation.json").write_text(
        json.dumps({k: v for k, v in isa.items() if k != "studies"} |
                   {"studies": [s["identifier"] for s in isa["studies"]]},
                   indent=2, ensure_ascii=False))

    # 2. Studies + Assays
    for st in isa["studies"]:
        sid = st["identifier"]
        sdir = out / "studies" / sid; sdir.mkdir(exist_ok=True)
        (sdir / "isa.study.json").write_text(json.dumps(st, indent=2, ensure_ascii=False))
        for a in st.get("assays", []):
            aid = a["@id"].split("/")[-1]
            adir = out / "assays" / aid; (adir / "dataset").mkdir(parents=True, exist_ok=True)
            (adir / "isa.assay.json").write_text(json.dumps(a, indent=2, ensure_ascii=False))
            # Rohdaten: verlinken (nicht kopieren — können riesig / in ENA sein)
            manifest = {"dataFiles": a.get("dataFiles", []),
                        "note": "Raw data — linked, not copied. Large files live in ENA/archive."}
            (adir / "dataset" / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))

    # 3. Workflows (Scripts) — aus dem Projekt, wenn vorhanden
    if proj and (proj / "scripts").exists():
        (out / "workflows" / "README.md").write_text(
            "# workflows/\nScripts/Pipelines, die aus Rohdaten die prozessierten Daten "
            "erzeugen. Idealerweise als CWL. Siehe das Projekt-`scripts/`.\n"
            "Diese sind die PROVENIENZ der Daten in runs/.\n")

    # 4. Runs (prozessierte Daten) — Hinweis nach Harmonisierungs-Prinzip
    (out / "runs" / "README.md").write_text(
        "# runs/\nProzessierte Daten (counts, h5ad, Ergebnisse). NICHT neu annotiert — "
        "sie hängen am erzeugenden Workflow in workflows/. Das Script IST die Annotation.\n")

    # 5. RO-Crate-Metadaten (die Schicht, die ARC benutzt)
    rocrate = build_rocrate_from_isa(isa)
    (out / "ro-crate-metadata.json").write_text(json.dumps(rocrate, indent=2, ensure_ascii=False))

    # 6. ARC-README
    (out / "README.md").write_text(f"""# ARC — {isa.get('title','')[:60]}

Annotated Research Context (DataPLANT/NFDI-Standard). Erzeugt aus FAIR-in-action.

## Struktur
- `isa.investigation.json` — das Projekt (ISA Investigation)
- `studies/` — die Studien (ISA Study)
- `assays/` — die Messungen: Rohdaten (verlinkt) + Metadaten (ISA Assay)
- `workflows/` — die Scripts, die prozessierte Daten erzeugen (die Provenienz)
- `runs/` — prozessierte Ergebnisse (nicht neu annotiert; hängen an workflows/)
- `ro-crate-metadata.json` — die maschinenlesbare RO-Crate-Schicht

## Nächster Schritt zur vollen ARC
Für `isa.investigation.xlsx` (Excel-Form) und Validierung: DataPLANT **ARCitect** oder
**arctrl**. Diese JSON-Form ist ISA-vollständig und ARC-strukturiert; xlsx ist Konvertierung.
""")
    return out

def build_rocrate_from_isa(isa):
    """Minimale, valide RO-Crate aus dem ISA-Modell."""
    graph = [
        {"@type": "CreativeWork", "@id": "ro-crate-metadata.json",
         "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
         "about": {"@id": "./"}},
        {"@id": "./", "@type": "Dataset",
         "name": isa.get("title", "research dataset"),
         "description": isa.get("description", "")[:500],
         "license": isa.get("license", ""),
         "hasPart": [{"@id": "isa.investigation.json"},
                     {"@id": "studies/"}, {"@id": "assays/"},
                     {"@id": "workflows/"}, {"@id": "runs/"}]},
        {"@id": "isa.investigation.json", "@type": "File",
         "name": "ISA Investigation metadata", "encodingFormat": "application/json"},
    ]
    # Personen als Entities
    for p in isa.get("people", []):
        pid = f"#person/{p.get('name','').replace(' ','_')}"
        graph.append({"@id": pid, "@type": "Person", "name": p.get("name","")})
    return {"@context": "https://w3id.org/ro/crate/1.1/context", "@graph": graph}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--isa", required=True, help="ISA-JSON (aus sdrf_to_isa.py)")
    ap.add_argument("--project", default="", help="Projektordner (für scripts/ etc.)")
    ap.add_argument("--out", required=True, help="Ziel-ARC-Ordner")
    a = ap.parse_args()
    out = build_arc(a.isa, a.project, a.out)
    print(f"  ARC gebaut → {out}")
    import os
    for root, dirs, files in os.walk(out):
        level = root.replace(str(out), '').count(os.sep)
        print("  " + "  "*level + pathlib.Path(root).name + "/")
        for f in files:
            print("  " + "  "*(level+1) + f)

if __name__ == "__main__":
    main()
