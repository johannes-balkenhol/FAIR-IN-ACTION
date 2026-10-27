#!/usr/bin/env bash
# =============================================================================
# prepare_project.sh  —  give it a project, it ADDS the FAIR/GDPR scaffold that
# is missing and writes a road-to-gold checklist. ADDITIVE ONLY: it never moves,
# renames or deletes anything that already exists, so it is safe to run on any
# project (reorganising/renaming is a separate, preview-first step by design).
#
#   bash prepare_project.sh <project_dir>        # preview (dry-run)
#   bash prepare_project.sh <project_dir> go     # apply
#
# Place in the FAIR-in-action bundle root (next to project.yaml.template).
# =============================================================================
set -uo pipefail
PROJ="${1:?usage: prepare_project.sh <project_dir> [go]}"
MODE="${2:-dry}"
PROJ="$(cd "$PROJ" 2>/dev/null && pwd)" || { echo "not a directory: $1"; exit 1; }
NAME="$(basename "$PROJ")"
BUNDLE="$(cd "$(dirname "$0")" && pwd)"
TMPL="$BUNDLE/project.yaml.template"
act(){ [[ "$MODE" == go ]]; }
say(){ echo "  $*"; }

echo "== prepare project: $NAME  (mode=$MODE) =="

have_readme=no;   [[ -e "$PROJ/README.md" || -e "$PROJ/README.txt" ]] && have_readme=yes
have_manifest=no; [[ -e "$PROJ/project.yaml" || -e "$PROJ/ro-crate-metadata.json" ]] && have_manifest=yes
have_license=no;  ls "$PROJ"/LICENSE* >/dev/null 2>&1 && have_license=yes
have_git=no;      [[ -d "$PROJ/.git" ]] && have_git=yes

echo ""; echo "### add missing scaffold (additive; existing files untouched) ###"

# project.yaml (manifest INSIDE the project — travels with the data)
if [[ "$have_manifest" == no ]]; then
  if act; then
    if [[ -f "$TMPL" ]]; then
      sed "s/<PROJECT_NAME>/$NAME/g; s/<DATE>/$(date +%F)/g" "$TMPL" > "$PROJ/project.yaml" 2>/dev/null || cp "$TMPL" "$PROJ/project.yaml"
    else
      cat > "$PROJ/project.yaml" <<EOF
project: $NAME
created: $(date +%F)
owner:            # TODO
modality:         # TODO  bulk-rnaseq | scrnaseq | imaging | flow-cytometry | proteomics | genome
organism:         # TODO
sensitive: false  # TODO  true if human / patient / clinical data
ethics_vote:      # TODO  if sensitive
consent_scope:    # TODO  if sensitive
license_data:     # TODO  e.g. CC-BY-4.0
license_code:     # TODO  e.g. MIT
retention:        # TODO  e.g. 10y post-publication
repository:       # TODO  target repo (ENA/ArrayExpress/EGA/PRIDE/BioImage Archive/Zenodo)
EOF
    fi
    say "created project.yaml"
  else say "DRY: would create project.yaml (from project.yaml.template if present, name/date filled)"; fi
else say "project.yaml present — kept"; fi

# README
if [[ "$have_readme" == no ]]; then
  if act; then
    cat > "$PROJ/README.md" <<EOF
# $NAME

<one-sentence description a stranger understands>

- data/  · analysis/  · metadata/  · results/   · manifest: project.yaml
- FAIR / GDPR status & remaining work: FAIR_GDPR_TODO.md
EOF
    say "created README.md"
  else say "DRY: would create README.md"; fi
else say "README present — kept"; fi

# metadata/ + documents/ (safe, FAIR-needed)
for d in metadata documents; do
  if [[ ! -d "$PROJ/$d" ]]; then
    if act; then mkdir -p "$PROJ/$d"; say "created $d/"; else say "DRY: would create $d/"; fi
  fi
done

# .gitignore + git init (code versioned; big/sensitive data excluded)
if [[ "$have_git" == no ]]; then
  if act; then
    [[ -f "$PROJ/.gitignore" ]] || printf 'data/\n*.bam\n*.fastq*\n*.zip\n*.h5ad\n*.RData\n*.tif\n*.czi\n__pycache__/\n' > "$PROJ/.gitignore"
    ( cd "$PROJ" && git init -q ) && say "git initialised (+ .gitignore excluding data/bam/fastq/images)" || say "!! git init failed"
  else say "DRY: would git init (+ .gitignore excluding data/, bam, fastq, images)"; fi
else say ".git present — kept"; fi

# re-detect so the checklist reflects what this run just created
[[ -e "$PROJ/README.md" || -e "$PROJ/README.txt" ]] && have_readme=yes
[[ -e "$PROJ/project.yaml" || -e "$PROJ/ro-crate-metadata.json" ]] && have_manifest=yes
ls "$PROJ"/LICENSE* >/dev/null 2>&1 && have_license=yes
[[ -d "$PROJ/.git" ]] && have_git=yes

# road-to-gold checklist (the 'list of remaining parts')
TODO="$PROJ/FAIR_GDPR_TODO.md"
tick(){ [[ "$1" == yes ]] && echo x || echo ' '; }
if act; then
  cat > "$TODO" <<EOF
# FAIR + GDPR — road to gold : $NAME
_generated $(date +%F) by prepare_project.sh · additive run — nothing was moved or renamed._

## Bronze (structure)
- [$(tick "$have_readme")] README.md
- [$(tick "$have_manifest")] project.yaml inside the project (manifest travels with the data)
- [ ] fill project.yaml: owner, modality, organism
- [ ] standard folders: data/{raw_data,primary_data}, analysis, results

## Silver (described + licensed)
- [$(tick "$have_license")] LICENSE (data + code) — e.g. CC-BY-4.0 / MIT
- [ ] metadata schema + controlled vocabulary (bundle core_model + the matching profile)
- [ ] one stable ID per sample (samples.tsv) — the join key for everything downstream

## Gold (deposited + packaged + reproducible)
- [$(tick "$have_git")] code in git
- [ ] deposition accession / DOI (ENA / ArrayExpress / EGA / PRIDE / BioImage Archive / Zenodo)
- [ ] RO-Crate / ARC packaging (data + documentation + provenance as one object)

## GDPR (only if human / patient / clinical data)
- [ ] sensitive? set it in project.yaml
- [ ] ethics vote + consent scope recorded
- [ ] donor_id -> identity mapping kept OUT of shared folders and git
- [ ] access restricted to a named group (not world, not 'users'); retention/deletion date set
- [ ] no patient identifiers in file/folder names
EOF
  say "wrote FAIR_GDPR_TODO.md"
else say "DRY: would write FAIR_GDPR_TODO.md (bronze/silver/gold + GDPR checklist, pre-ticked from current state)"; fi

echo ""
[[ "$MODE" == dry ]] && echo "PREVIEW. Apply: bash prepare_project.sh \"$PROJ\" go"
echo "Additive only — data, code and folder names untouched. Renaming/reorganising is a separate preview-first step."
