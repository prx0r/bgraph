#!/usr/bin/env python3
"""Print R2 content layout for a store (documentation aid)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    store = None
    if "--store" in sys.argv:
        store = sys.argv[sys.argv.index("--store") + 1]
    path = ROOT / "registry" / "brands" / f"{store}.json"
    if not path.exists():
        print(f"unknown store: {store}")
        print("available:", ", ".join(p.stem for p in sorted((ROOT / "registry" / "brands").glob("*.json"))))
        return 1
    d = json.loads(path.read_text())
    sid = d["store_id"]
    print(f"R2 layout for store_id={sid}")
    print(f"  commerce assets: commerce/stores/{sid}/assets/<SKU>/...")
    print(f"  content root:    content/stores/{sid}/")
    print()
    for b in d.get("branches") or []:
        root = (b.get("r2_layout") or {}).get("root") or f"content/stores/{sid}/{b['branch_id']}"
        print(f"  [{b['branch_id']}] enabled={b.get('enabled', True)} root={root}")
        for ct in b.get("content_types") or []:
            print(f"      {ct}/  raw|masters|metadata")
        for m in b.get("posting_methods") or []:
            print(f"      method {m.get('method_id')} gate={m.get('gate')}")
    print()
    print("  analytics sink: content/stores/<id>/analytics/<branch>/")
    print("  manifests:      content/stores/<id>/_manifest/")
    print("  product links:  content/stores/<id>/product-library/links.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
