#!/usr/bin/env python3
"""Export brand organiser graphs to exports/<store_id>.json."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "registry" / "brands"
EXPORTS = ROOT / "exports"


def export_brand(data: dict) -> dict:
    sid = data["store_id"]
    nodes = []
    edges = []

    nodes.append({
        "id": sid,
        "type": "store",
        "label": data["identity"]["display_name"],
        "data": {
            "brand_id": data["brand_id"],
            "status": data.get("status"),
            "domain": data["identity"].get("domain"),
            "email": data["identity"].get("email"),
            "phone": data["identity"].get("phone"),
        },
    })
    nodes.append({
        "id": f"identity:{sid}",
        "type": "identity",
        "label": data["identity"]["display_name"],
        "data": data["identity"],
    })
    edges.append({"from": sid, "to": f"identity:{sid}", "rel": "has_identity"})
    edges.append({"from": sid, "to": f"commerce:{sid}", "rel": "commerce_link"})

    nodes.append({
        "id": f"commerce:{sid}",
        "type": "commerce_ref",
        "label": f"commerce:{sid}",
        "data": data.get("commerce_link") or {},
    })

    for b in data.get("branches") or []:
        bid = f"{sid}/{b['branch_id']}"
        nodes.append({
            "id": bid,
            "type": "branch",
            "label": b["branch_id"],
            "data": {
                "platform": b["platform"],
                "enabled": b.get("enabled", True),
                "account": b.get("account"),
            },
        })
        edges.append({"from": f"identity:{sid}", "to": bid, "rel": "owns_branch"})
        for ct in b.get("content_types") or []:
            ctid = f"{bid}/{ct}"
            nodes.append({
                "id": ctid,
                "type": "content_type",
                "label": ct,
                "data": {"content_type": ct, "branch_id": b["branch_id"]},
            })
            edges.append({"from": bid, "to": ctid, "rel": "accepts"})
            edges.append({"from": ctid, "to": f"commerce:{sid}", "rel": "references_products"})
        for m in b.get("posting_methods") or []:
            mid = f"method:{m['method_id']}"
            if not any(n["id"] == mid for n in nodes):
                nodes.append({
                    "id": mid,
                    "type": "method",
                    "label": m["method_id"],
                    "data": m,
                })
            for ct in b.get("content_types") or []:
                edges.append({"from": f"{bid}/{ct}", "to": mid, "rel": "published_via"})
        root = (b.get("r2_layout") or {}).get("root")
        if root:
            rid = f"r2:{root}"
            nodes.append({"id": rid, "type": "r2_layout", "label": root, "data": b["r2_layout"]})
            for ct in b.get("content_types") or []:
                edges.append({"from": f"{bid}/{ct}", "to": rid, "rel": "stores_in"})

    # de-dupe edges
    seen = set()
    deduped = []
    for e in edges:
        key = (e["from"], e["to"], e["rel"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(e)

    return {
        "schema_version": "bgraph-export.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "store_id": sid,
        "nodes": nodes,
        "edges": deduped,
        "counts": {"nodes": len(nodes), "edges": len(deduped), "branches": len(data.get("branches") or [])},
    }


def main() -> int:
    EXPORTS.mkdir(parents=True, exist_ok=True)
    store_filter = None
    if "--store" in sys.argv:
        store_filter = sys.argv[sys.argv.index("--store") + 1]
    files = sorted(BRANDS.glob("*.json"))
    if store_filter:
        files = [p for p in files if p.stem == store_filter]
    if not files:
        print("no brands to export")
        return 1
    for path in files:
        data = json.loads(path.read_text())
        graph = export_brand(data)
        out = EXPORTS / f"{data['store_id']}.json"
        out.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {out} nodes={graph['counts']['nodes']} edges={graph['counts']['edges']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
