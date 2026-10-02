#!/usr/bin/env python3
"""Actuate dry-run: score → Jev gates → receipts. No money, no publish.

Usage:
  python3 scripts/actuate.py --dry-run
  python3 scripts/actuate.py --dry-run --store oddhobb
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import jev  # noqa: E402
from score import score_store  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="required in P0 (no actuators)")
    ap.add_argument("--store", default=None)
    args = ap.parse_args()

    # P0 law: always dry-run; never push/spend/publish from this script
    if not args.dry_run:
        print("P0: pass --dry-run. Actuators are not wired (no Shopify push, no spend).")
        return 2

    brands_dir = ROOT / "registry" / "brands"
    files = sorted(brands_dir.glob("*.json"))
    if args.store:
        files = [p for p in files if p.stem == args.store]
        if not files:
            print(f"unknown store: {args.store}")
            return 1

    print("=== bgraph actuate dry-run (P0) ===")
    print("law: score → Jev stub → human on money/publish | no actuators\n")

    all_receipts = []
    for path in files:
        data = json.loads(path.read_text())
        sc = score_store(data)
        print(f"── {sc['store_id']}  score={sc['score']}  packs={sc['pack_count']}  "
              f"branches={sc['enabled_branches']}  domain={sc['domain']}")

        # Noul: brand_ready
        r1 = jev.decide(
            "brand_ready",
            sc["store_id"],
            {
                "pack_count": sc["pack_count"],
                "has_store_json": sc["has_store_json"],
                "has_domain": sc["has_domain"],
                "commerce_link_ok": sc["commerce_link_ok"],
            },
        )
        p1 = jev.record(r1)
        print(f"  brand_ready     → {r1['answer']}  band={r1['band']}  "
              f"conf={r1['confidence']:.2f}  action={r1['action']}")
        print(f"                   receipt {p1.name}")

        # Noul: shopify_push_ok (always human in P0)
        r2 = jev.decide(
            "shopify_push_ok",
            sc["store_id"],
            {"brand_ready": r1["answer"], "pack_count": sc["pack_count"], "currency_policy": "store"},
        )
        p2 = jev.record(r2)
        print(f"  shopify_push_ok → {r2['answer']}  band={r2['band']}  "
              f"action={r2['action']}")
        print(f"                   receipt {p2.name}")

        # Choice: next_photo_sku
        opts = ["top_priority_pack", "best_margin_hint", "featured_section"]
        r3 = jev.decide(
            "next_photo_sku",
            sc["store_id"],
            {
                "pack_count": sc["pack_count"],
                "picked": "top_priority_pack" if sc["pack_count"] else opts[0],
                "confidence": min(0.5 + sc["score"] / 2, 0.95),
            },
        )
        p3 = jev.record(r3)
        print(f"  next_photo_sku  → {r3['picked']}  band={r3['band']}  "
              f"action={r3['action']}")
        print(f"                   receipt {p3.name}")

        # Noul: content tree
        r4 = jev.decide(
            "content_tree_ok",
            sc["store_id"],
            {
                "has_bgraph_branches": sc["has_bgraph_branches"],
                "r2_prefix_set": sc["r2_prefix_set"],
            },
        )
        p4 = jev.record(r4)
        print(f"  content_tree_ok → {r4['answer']}  band={r4['band']}  action={r4['action']}")
        print(f"                   receipt {p4.name}")
        print()
        all_receipts.extend([r1, r2, r3, r4])

    summary = {
        "mode": "dry-run",
        "receipts": len(all_receipts),
        "human_actions": [r for r in all_receipts if r.get("band") == "human" or "HOLD" in str(r.get("action"))],
        "model": jev.MODEL,
    }
    out = ROOT / "data" / "actuate_latest.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    print("=== summary ===")
    print(f"receipts written: {len(all_receipts)}")
    print(f"human/hold items: {len(summary['human_actions'])}")
    print(f"latest summary: {out}")
    print("\nP0 complete. Next: live Jev key · engines.yaml · one human-confirmed push.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
