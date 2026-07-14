#!/usr/bin/env python3
"""
cv_review.py — inspect what build_cv_cache.py actually cached, before you trust it.

    python3 cv_review.py            # show every non-exact match
    python3 cv_review.py --prune    # DELETE the fuzzy ones, keep only exact matches

WHY
---
`build_cv_cache.py` reported: PR — 14 seeds, 0 exact matches, 48 terms cached.
That means every Protein Ontology term in the cache came from a FUZZY match, and
fuzzy matches are how a wrong CURIE gets in.

A wrong CURIE is worse than free text. Free text is honestly unusable; a wrong
CURIE is *confidently* unusable, and downstream it will be believed — by a curator,
by an atlas, by whoever reuses the data in five years.

So: look at these before shipping them.
"""
import argparse, json, pathlib, sys
from build_cv_cache import SEEDS

ROOT = pathlib.Path(__file__).resolve().parent
CACHE = ROOT / "cv_cache.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prune", action="store_true",
                    help="keep only exact label matches; delete everything else")
    a = ap.parse_args()

    if not CACHE.exists():
        raise SystemExit("no cv_cache.json — run build_cv_cache.py first")
    cache = json.loads(CACHE.read_text())

    # rows are [curie, label] (v1) or [curie, label, exact] (v2). Tolerate both.
    def lab(r):   return r[1]
    def cur(r):   return r[0]

    print(f"{'ontology':11s} {'you asked for':34s} {'top cached hit':46s}")
    print("─" * 100)

    kept, dropped, total_exact, total_fuzzy = {}, [], 0, 0

    for onto, seeds in SEEDS.items():
        rows = cache.get(onto, [])
        labels = {lab(r).lower(): cur(r) for r in rows}
        keep = []
        for s in seeds:
            cid = labels.get(s.lower())
            if cid:                                  # exact label match — trustworthy
                keep.append(next(r for r in rows if cur(r) == cid))
                total_exact += 1
                continue
            # no exact match: what DID we cache for this seed?
            near = [r for r in rows if s.lower().split()[0] in lab(r).lower()]
            top = near[0] if near else None
            total_fuzzy += 1
            mark = "\033[31m✗\033[0m"
            shown = f"{cur(top)}  {lab(top)}" if top else "(nothing)"
            print(f"{mark} {onto:9s} {s:34s} {shown:46s}")
            dropped.append((onto, s, top))
            if not a.prune and top:
                keep.append(top)
        # always keep anything that was an exact hit on SOME seed
        seen = set()
        kept[onto] = [r for r in (keep or rows) if not (cur(r) in seen or seen.add(cur(r)))]

    print("─" * 100)
    print(f"  {total_exact} exact · {total_fuzzy} NOT exact\n")

    by_onto = {}
    for onto, s, top in dropped:
        by_onto.setdefault(onto, []).append(s)
    for onto, ss in sorted(by_onto.items(), key=lambda x: -len(x[1])):
        frac = len(ss) / len(SEEDS[onto])
        flag = "  ← DO NOT SHIP" if frac > 0.6 else ""
        print(f"  {onto:10s} {len(ss)}/{len(SEEDS[onto])} seeds unmatched{flag}")

    print("\n  An ontology where MOST seeds fail is not a lookup problem — it means")
    print("  you are using the wrong labels for that ontology, or the wrong ontology.")
    print("  PR, for instance, does not call the antigen 'CD4'; it uses protein")
    print("  nomenclature. Either find the right labels, or drop PR and curate the")
    print("  antibody panel vocabulary by hand — which for ~30 markers is an hour's")
    print("  work and gives you something you can actually defend.")

    if a.prune:
        CACHE.write_text(json.dumps(kept, indent=1, ensure_ascii=False))
        n = sum(len(v) for v in kept.values())
        print(f"\n  PRUNED → {n} terms kept (exact matches only). Re-run build_app.py.")
    else:
        print("\n  Nothing changed. Run with --prune to keep only exact matches.")


if __name__ == "__main__":
    main()
