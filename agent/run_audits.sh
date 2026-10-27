#!/usr/bin/env bash
# =============================================================================
# run_audits.sh  —  run the FAIR-in-action audit suite across sibling projects
# Lives in the bundle root; scans a projects root (default: the bundle's parent,
# i.e. every project folder next to FAIR-in-action) and writes dated reports.
# READ-ONLY on the scanned projects; writes only into FAIR-in-action/reports/.
#
#   bash run_audits.sh                         # scan ../  (siblings of the bundle)
#   bash run_audits.sh /storage/users/job37yv/Projects
# =============================================================================
set -uo pipefail
BUNDLE="$(cd "$(dirname "$0")" && pwd)"
ROOT="${1:-$(dirname "$BUNDLE")}"
DATE="$(date +%F)"
REP="$BUNDLE/reports/$DATE"
mkdir -p "$REP"
echo "== FAIR-in-action audit suite =="
echo "  bundle : $BUNDLE"
echo "  root   : $ROOT"
echo "  reports: $REP"
echo ""

run(){ echo "---- $1 ----"; shift; "$@"; echo; }

# 1) FAIR + GDPR + structure + root-level  (the one auditor that exists today)
if [[ -f "$BUNDLE/agent/fair_gdpr_audit.py" ]]; then
  echo "[1] FAIR + GDPR + structure + root  (agent/fair_gdpr_audit.py)"
  python3 "$BUNDLE/agent/fair_gdpr_audit.py" "$ROOT" --json "$REP/fair_gdpr.json" \
      | tee "$REP/fair_gdpr.txt"
  echo ""
else
  echo "[1] SKIP: agent/fair_gdpr_audit.py not found (run place_bundle_files.sh first)."
fi

# 2) FAIR tier per project  (the bundle's own auditor; wire its CLI here)
#    e.g.:  for p in "$ROOT"/*/ ; do python3 "$BUNDLE/audit.py" "$p" ; done > "$REP/fair_tier.txt"
echo "[2] FAIR tier (audit.py) — hook: wire your per-project call here."

# 3) Metadata validation  (validate.py against core_model + profiles)
#    e.g.:  python3 "$BUNDLE/validate.py" "$p/metadata/project.yaml"
echo "[3] metadata validation (validate.py) — hook."

# ---- audit types framework (have vs to-build) -------------------------------
cat > "$REP/AUDIT_TYPES.md" <<'EOF'
# Audit types — status (this run)

| Audit | What it checks | Engine | Status |
|---|---|---|---|
| Structure / FAIR | folders, README, manifest-inside, naming, tier | agent/fair_gdpr_audit.py | RUN |
| GDPR | sensitive-but-readable, ethics ref, retention, identifiers-in-names | agent/fair_gdpr_audit.py | RUN |
| Root hygiene | detached manifests, version sprawl, loose files | agent/fair_gdpr_audit.py | RUN |
| FAIR tier (bronze/silver/gold) | per-project maturity | audit.py | HOOK (wire CLI) |
| Metadata validation | fields vs core_model + profile, controlled vocab | validate.py + ols_check.py | HOOK |
| Data QC | per-modality quality runs (e.g. ID-namespace, dims, contamination) | per profile | TO BUILD |
| Release-gate (G2) | recorded go/no-go, metadata travels with result | gates spec | TO BUILD |

Direction is good when, run over run, more projects move up a tier and fewer carry
GDPR flags, and G0/G1/G2 coverage rises. Compare reports/<date>/fair_gdpr.json over time.
EOF

echo ""
echo "Done. Human report: $REP/fair_gdpr.txt | machine: $REP/fair_gdpr.json | types: $REP/AUDIT_TYPES.md"
echo "Re-run on a schedule and diff the JSON to track the trend (tiers up, GDPR flags down, gates covered)."
