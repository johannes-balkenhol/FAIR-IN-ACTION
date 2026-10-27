#!/usr/bin/env bash
# =============================================================================
# place_bundle_files.sh  —  sort the loose files at the FAIR-in-action root
# into their subdirectories, and move duplicates/zips to trash/ (never rm).
# Run from inside the bundle:  cd .../FAIR-in-action
#   bash place_bundle_files.sh        -> preview
#   bash place_bundle_files.sh go     -> execute
# Idempotent: skips anything already moved or absent.
# =============================================================================
set -uo pipefail
MODE="${1:-dry}"
TS="$(date +%F_%H%M)"
TRASH="trash/$TS"

mv_to(){ local s="$1" d="$2"
  [[ -e "$s" ]] || { echo "  skip (absent): $s"; return; }
  if [[ "$MODE" == go ]]; then mkdir -p "$d"; mv -- "$s" "$d"/ && echo "  $s -> $d/" || echo "  !! failed: $s"
  else echo "  DRY: $s -> $d/"; fi; }

trash_it(){ local s="$1"
  [[ -e "$s" ]] || { echo "  skip (absent): $s"; return; }
  if [[ "$MODE" == go ]]; then mkdir -p "$TRASH"; mv -- "$s" "$TRASH"/ && echo "  trashed: $s" || echo "  !! failed: $s"
  else echo "  DRY trash: $s"; fi; }

echo "== place FAIR-in-action files (mode=$MODE) =="

echo ""; echo "### agent/ (auditors) ###"
mv_to "fair_gdpr_audit.py"        agent
mv_to "fair_portfolio_manifest.sh" agent

echo ""; echo "### bundle/for-AI/ (machine/AI docs) ###"
for f in "FAIR-TRE-bundle_target-architecture_and-transfer-path.md" \
         "FAIR-bundle_gates-and-transferable-components_spec.md" \
         "2026-10-19_bundle-vnext_intake-to-gold_blueprint.md" \
         "grant-figures_bundle-adjustments_and_EHDS-context.md" \
         "FAIR-in-action_knowledge-graph-layer_design.md"; do mv_to "$f" bundle/for-AI; done

echo ""; echo "### bundle/for-humans/ ###"
mv_to "README_TEMPLATE_multicenter-multimodal.md" bundle/for-humans

echo ""; echo "### documents/RDM-feedback/ ###"
mv_to "FAIR-in-action_practice-feedback-register.md" documents/RDM-feedback

echo ""; echo "### documents/project-specific-audits/ ###"
mv_to "2026-10-19_FAIR-self-report_v1.md" documents/project-specific-audits

echo ""; echo "### trash: duplicates + transport zips (kept in trash/, not deleted) ###"
trash_it "fair_gdpr_audit (1).py"
trash_it "FAIR-in-action_bundle-updates_2026-10-25.zip"
trash_it "FAIR-in-action_bundle-updates_2026-10-25 (1).zip"
# condensed project-copies (the fuller originals are kept above)
trash_it "FAIR-self-report_v1_2026-10-19.md"
trash_it "FAIR-bundle-vnext_blueprint_2026-10-19.md"
trash_it "FAIR-bundle_gates-spec_2026-10-19.md"
trash_it "FAIR-in-action_knowledge-graph-layer_design_2026-10-25.md"

echo ""
[[ "$MODE" == dry ]] && echo "PREVIEW. Re-run: bash place_bundle_files.sh go"
echo "After go: root holds only the bundle's own top files (README.md, core_model.yaml, audit.py, ...);"
echo "the new docs live under bundle/for-AI, bundle/for-humans, documents/, agent/."
echo "Merge notes: target-architecture extends bundle/for-AI/ARCHITECTURE.md; README_TEMPLATE_multicenter-multimodal"
echo "replaces for-humans/README_TEMPLATE_multicenter.md; grant-figures §2 can split to bundle/compliance/EHDS-and-national-context.md."
