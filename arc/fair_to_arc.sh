#!/usr/bin/env bash
# fair_to_arc.sh — die komplette Pipeline: MAGE-TAB → ISA → ARC
# Usage: ./fair_to_arc.sh <idf> <sdrf> <projekt-ordner> <ziel-ARC>
set -e
IDF="$1"; SDRF="$2"; PROJ="$3"; OUT="$4"
DIR="$(dirname "$0")"
echo "1/3  MAGE-TAB → ISA ..."
python3 "$DIR/sdrf_to_isa.py" --idf "$IDF" --sdrf "$SDRF" -o /tmp/_isa.json
echo "2/3  ISA → ARC ..."
python3 "$DIR/make_arc.py" --isa /tmp/_isa.json --project "$PROJ" --out "$OUT"
echo "3/3  RO-Crate validieren ..."
python3 "$DIR/../bundle/for-AI/validate_crate.py" "$OUT/ro-crate-metadata.json"
echo "Fertig: $OUT"
