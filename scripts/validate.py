#!/usr/bin/env python3
"""Validate bgraph registries against schemas (stdlib only, no jsonschema dep)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "registry" / "brands"
REQUIRED_BRAND_KEYS = {"schema_version", "store_id", "brand_id", "identity", "branches"}
REQUIRED_BRANCH_KEYS = {"branch_id", "platform", "content_types", "posting_methods", "r2_layout"}
REQUIRED_METHOD_KEYS = {"method_id", "stage", "gate"}
GATES = {"none", "human_confirm", "qp_grant"}
STAGES = {"ingest", "organise", "package", "publish", "measure", "optimise"}


def err(msg: str) -> None:
    print(f"ERROR: {msg}")
    raise SystemExit(1)


def main() -> int:
    # templates
    tpl = json.loads((ROOT / "templates" / "brand.template.json").read_text())
    missing = REQUIRED_BRAND_KEYS - set(tpl)
    if missing:
        err(f"template missing keys {missing}")
    for b in tpl["branches"]:
        miss = REQUIRED_BRANCH_KEYS - set(b)
        if miss:
            err(f"template branch {b.get('branch_id')} missing {miss}")

    # content types yaml-ish json-less: load as text keys
    ct_path = ROOT / "registry" / "content_types" / "content_types.yaml"
    ct_text = ct_path.read_text()
    for ct in ("longform", "short", "vertical", "post", "ad"):
        if not re.search(rf"^{ct}:", ct_text, re.M):
            err(f"content_types.yaml missing {ct}")

    # methods
    methods = {}
    for line in (ROOT / "registry" / "methods" / "methods.yaml").read_text().splitlines():
        if line and not line.startswith(" ") and line.endswith(":"):
            methods[line[:-1]] = True
    for mid in (
        "ingest.local_or_r2",
        "organise.folder",
        "package.from_listing",
        "publish.human_confirm",
        "measure.analytics_pull",
        "optimise.join_later",
    ):
        if mid not in methods:
            err(f"methods.yaml missing {mid}")

    # brands
    brands = sorted(BRANDS.glob("*.json"))
    if not brands:
        err("no brand files in registry/brands")
    for path in brands:
        data = json.loads(path.read_text())
        miss = REQUIRED_BRAND_KEYS - set(data)
        if miss:
            err(f"{path.name} missing {miss}")
        if data.get("schema_version") != "brand-organiser.v1":
            err(f"{path.name} schema_version must be brand-organiser.v1")
        sid = data["store_id"]
        if path.stem != sid:
            err(f"{path.name} store_id {sid} != filename")
        if not data["identity"].get("display_name"):
            err(f"{path.name} identity.display_name required")
        enabled = [b for b in data["branches"] if b.get("enabled", True)]
        if data.get("status") == "active" and not enabled:
            err(f"{path.name} active but no enabled branches")
        for b in data["branches"]:
            miss = REQUIRED_BRANCH_KEYS - set(b)
            if miss:
                err(f"{path.name} branch {b.get('branch_id')} missing {miss}")
            for m in b.get("posting_methods", []):
                if m.get("gate") not in GATES:
                    err(f"{path.name} method {m.get('method_id')} bad gate {m.get('gate')}")
                if m.get("gate") != "human_confirm" and b.get("platform") in {"youtube", "instagram", "tiktok", "x", "pinterest"}:
                    # publish methods for social must be human_confirm in v1
                    if m.get("method_id", "").startswith(("yt.", "ig.", "tt.", "pin.", "x.")):
                        err(f"{path.name} social publish must be human_confirm: {m.get('method_id')}")
            # R2 root convention
            root = b["r2_layout"].get("root", "")
            if root and f"content/stores/{sid}/" not in root:
                err(f"{path.name} branch {b['branch_id']} r2 root not under content/stores/{sid}/")

    print(f"OK: {len(brands)} brands validated")
    print("OK: content_types + methods registry present")
    print("OK: publish gates are human_confirm for social methods")
    return 0


if __name__ == "__main__":
    sys.exit(main())
