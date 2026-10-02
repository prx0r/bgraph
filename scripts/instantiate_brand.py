#!/usr/bin/env python3
"""Instantiate a new brand organiser from template."""
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--template", default=str(ROOT / "templates" / "brand.template.json"))
    ap.add_argument("--store-id", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--brand-id", default=None)
    ap.add_argument("--domain", default=None)
    ap.add_argument("--email", default=None)
    ap.add_argument("--phone", default=None)
    ap.add_argument("--handle", default=None)
    ap.add_argument("--voice", default="TODO voice")
    ap.add_argument("--status", default="scaffold", choices=["scaffold", "active", "paused"])
    args = ap.parse_args()

    store_id = args.store_id
    if not re_match(store_id):
        print("store-id must be lowercase alphanumeric + underscore/hyphen")
        return 1
    out_path = ROOT / "registry" / "brands" / f"{store_id}.json"
    if out_path.exists():
        print(f"refusing to overwrite existing {out_path}")
        return 1

    tpl = json.loads(Path(args.template).read_text())
    data = deepcopy(tpl)
    data["store_id"] = store_id
    data["brand_id"] = args.brand_id or store_id
    data["status"] = args.status
    data["identity"]["display_name"] = args.name
    data["identity"]["handle_primary"] = args.handle
    data["identity"]["domain"] = args.domain
    data["identity"]["email"] = args.email or (f"hello@{args.domain}" if args.domain else None)
    data["identity"]["phone"] = args.phone
    data["identity"]["voice"] = args.voice
    data["commerce_link"]["r2_commerce_prefix"] = f"commerce/stores/{store_id}"
    data["commerce_link"]["pack_path"] = f"oddhobbies/stores/{store_id}"
    data["commerce_link"]["graph_export"] = f"oddhobbies/graph/{store_id}.json"
    data["commerce_link"]["product_library_ref"] = (
        f"r2://powpowpow-warehouse/powpowpow/content/stores/{store_id}/product-library/links.json"
    )
    for b in data["branches"]:
        b["r2_layout"]["root"] = f"content/stores/{store_id}/{b['branch_id']}"
        b["analytics"]["r2_sink"] = f"content/stores/{store_id}/analytics/{b['branch_id']}/"
        # rewrite folder paths to relative under branch
        folders = []
        for f in b["r2_layout"].get("folders") or []:
            parts = f.split("/")
            folders.append("/".join(parts[-2:]) if len(parts) >= 2 else parts[-1])
        b["r2_layout"]["folders"] = folders
        if args.handle:
            b["account"]["handle"] = args.handle
    today = date.today().isoformat()
    data["created_at"] = today
    data["updated_at"] = today
    data["notes"] = f"Instantiated from template on {today}"

    out_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out_path}")
    print(f"next: edit identity/branches, create oddhobbies/stores/{store_id}/, run validate.py + export_graph.py")
    return 0


def re_match(s: str) -> bool:
    import re
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9_-]*", s))


if __name__ == "__main__":
    sys.exit(main())
