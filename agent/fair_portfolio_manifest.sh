#!/usr/bin/env bash
# =============================================================================
# fair_portfolio_manifest.sh  —  read-only portfolio manifest for the FAIR audit
# -----------------------------------------------------------------------------
# Walks the top-level project folders under a root and records, per project:
#   name · last-modified · size · has README / DMP / project.yaml / git · FAIR tier
# Nothing is written inside your folders; one TSV is emitted to the current dir.
# Run it once on the LAPTOP and once on the HPC, then send me both TSVs — I diff
# them for the real tiers and the laptop<->HPC mirror state.
#
#   bash fair_portfolio_manifest.sh /mnt/d/Research
#   bash fair_portfolio_manifest.sh /storage/users/job37yv/Projects
# =============================================================================
set -uo pipefail
ROOT="${1:?usage: fair_portfolio_manifest.sh <root>}"
HOST="$(hostname -s 2>/dev/null || echo host)"
STAMP="$(date +%F)"
OUT="fair_manifest_${HOST}_${STAMP}.tsv"

# locate the bundle auditor if present (optional; tier stays "n/a" if absent)
SCAN=""
for c in "$ROOT"/cRDM/Projects/FAIR-in-action/agent/fair_scan.py \
         "$ROOT"/FAIR-in-action/agent/fair_scan.py \
         "$ROOT"/*/FAIR-in-action/agent/fair_scan.py; do
  [[ -f "$c" ]] && { SCAN="$c"; break; }
done

printf "project\tmtime\tsize\treadme\tdmp\tproject_yaml\tgit\ttier\n" > "$OUT"

shopt -s nullglob
for d in "$ROOT"/*/; do
  name="$(basename "$d")"
  mtime="$(date -r "$d" +%F 2>/dev/null || echo '?')"
  size="$(du -sh "$d" 2>/dev/null | cut -f1)"
  readme=no; dmp=no; yaml=no; git=no
  compgen -G "$d"'[Rr][Ee][Aa][Dd][Mm][Ee]*' >/dev/null && readme=yes
  compgen -G "$d"'*[Dd][Mm][Pp]*'            >/dev/null && dmp=yes
  compgen -G "$d"'project.y*ml'              >/dev/null && yaml=yes
  [[ -d "$d/.git" ]] && git=yes
  tier="n/a"
  if [[ -n "$SCAN" ]]; then
    tier="$(python3 "$SCAN" "$d" --quiet 2>/dev/null | grep -ioE 'bronze|silver|gold' | head -1 || true)"
    [[ -z "$tier" ]] && tier="scan?"
  fi
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
    "$name" "$mtime" "$size" "$readme" "$dmp" "$yaml" "$git" "$tier" >> "$OUT"
done

echo "Wrote $OUT  ($(($(wc -l < "$OUT")-1)) projects)"
[[ -z "$SCAN" ]] && echo "note: fair_scan.py not found under $ROOT — tier column is n/a (structure columns still useful)."
echo "Send me this file. Run the same on the other machine for the mirror diff."
