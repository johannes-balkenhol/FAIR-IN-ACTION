#!/usr/bin/env python3
"""
isa_model.py — das ISA-Modell (Investigation / Study / Assay) als verbindende Schicht.

ISA ist das gemeinsame Metadaten-Modell, auf das ALLES im Bundle ausgerichtet ist:
  - das Schema (profiles/) liefert die Felder
  - die App füllt sie
  - RO-Crate verpackt sie
  - ARC ist die Ziel-Ordnerstruktur
ISA ist die Brücke dazwischen. Projekt→Sample→Messung IST Investigation→Study→Assay.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json


@dataclass
class OntologyTerm:
    """Ein kontrollierter Begriff: label + CURIE (z.B. 'Mus musculus' / NCBITaxon:10090)."""
    label: str
    accession: str = ""      # CURIE, z.B. NCBITaxon:10090
    source: str = ""         # NCBITaxon, EFO, ...

    def to_dict(self):
        return {"annotationValue": self.label,
                "termAccession": self.accession, "termSource": self.source}


@dataclass
class Characteristic:
    """Eine Eigenschaft eines Samples: category=value, ontologie-gebunden."""
    category: str            # z.B. 'organism'
    value: str               # z.B. 'Mus musculus'
    ontology: Optional[OntologyTerm] = None
    unit: str = ""

    def to_dict(self):
        d = {"category": self.category, "value": self.value}
        if self.ontology: d["ontology"] = self.ontology.to_dict()
        if self.unit: d["unit"] = self.unit
        return d


@dataclass
class Sample:
    """Eine biologische Probe = eine ISA Source/Sample-Zeile."""
    sample_id: str
    characteristics: List[Characteristic] = field(default_factory=list)
    factors: Dict[str, str] = field(default_factory=dict)   # das experimentelle Design

    def to_dict(self):
        return {"@id": f"#sample/{self.sample_id}", "name": self.sample_id,
                "characteristics": [c.to_dict() for c in self.characteristics],
                "factorValues": self.factors}


@dataclass
class Assay:
    """Eine Messung = ISA Assay. Verweist auf Samples, Rohdaten, das Protokoll."""
    assay_id: str
    measurement_type: str            # z.B. 'RNA sequencing'
    technology: str                  # z.B. 'nucleotide sequencing'
    platform: str = ""               # z.B. 'Illumina NovaSeq 6000'
    samples: List[str] = field(default_factory=list)     # sample_ids
    raw_files: List[str] = field(default_factory=list)   # FASTQ etc.
    protocol_ref: str = ""

    def to_dict(self):
        return {"@id": f"#assay/{self.assay_id}", "measurementType": self.measurement_type,
                "technologyType": self.technology, "platform": self.platform,
                "samples": self.samples, "dataFiles": self.raw_files,
                "protocol": self.protocol_ref}


@dataclass
class Study:
    """Eine Studie = ISA Study. Bündelt Samples + Assays + Protokolle + Faktoren."""
    study_id: str
    title: str = ""
    description: str = ""
    samples: List[Sample] = field(default_factory=list)
    assays: List[Assay] = field(default_factory=list)
    protocols: List[Dict] = field(default_factory=list)
    factors: List[str] = field(default_factory=list)    # Namen der Design-Faktoren

    def to_dict(self):
        return {"identifier": self.study_id, "title": self.title,
                "description": self.description,
                "factors": self.factors,
                "protocols": self.protocols,
                "materials": {"samples": [s.to_dict() for s in self.samples]},
                "assays": [a.to_dict() for a in self.assays]}


@dataclass
class Investigation:
    """Das ganze Projekt = ISA Investigation. Die oberste Ebene."""
    identifier: str
    title: str = ""
    description: str = ""
    people: List[Dict] = field(default_factory=list)     # name, orcid, role
    studies: List[Study] = field(default_factory=list)
    license: str = ""
    identifiers: Dict[str, str] = field(default_factory=dict)  # accession, doi, ...

    def to_dict(self):
        return {"identifier": self.identifier, "title": self.title,
                "description": self.description, "people": self.people,
                "license": self.license, "identifiers": self.identifiers,
                "studies": [s.to_dict() for s in self.studies]}

    def to_isa_json(self, path=None):
        """ISA-JSON — die maschinenlesbare ISA-Form."""
        j = json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
        if path: open(path, "w").write(j)
        return j
