#!/usr/bin/env python3
"""Human-readable brand status board."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "registry" / "brands"


def main() -> int:
    files = sorted(BRANDS.glob("*.json"))
    if not files:
        print("no brands")
        return 1
    print(f"{'store_id':<16} {'status':<10} {'domain':<22} {'handle':<20} branches")
    print("-" * 90)
    for path in files:
        d = json.loads(path.read_text())
        ident = d.get("identity") or {}
        branches = d.get("branches") or []
        enabled = [b["branch_id"] for b in branches if b.get("enabled", True)]
        disabled = [b["branch_id"] for b in branches if not b.get("enabled", True)]
        branch_s = ",".join(enabled) or "(none)"
        if disabled:
            branch_s += f"  [off: {','.join(disabled)}]"
        site = (d.get("site") or {}).get("primary_host") or ident.get("domain") or "-"
        print(
            f"{d.get('store_id','?'):<16} {d.get('status','?'):<10} "
            f"{site:<22} {(ident.get('handle_primary') or '-'):<20} {branch_s}"
        )
    print()
    print(f"{len(files)} brands · schema brand-organiser.v1")
    print("exports:", ", ".join(sorted(p.name for p in (ROOT / 'exports').glob('*.json'))) or "(none)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
