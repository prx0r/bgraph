# COMMERCE — oddhobbies link

**Repo:** `/root/oddhobbies`  
**DB:** `db/commerce.db` · packs: `stores/<store_id>/`

## What commerce owns

| Asset | Path |
|-------|------|
| Store packs | `stores/<store_id>/store.json` + `listings/*.json` |
| Product truth | `db/commerce.db` |
| Assets labels | R2 `commerce/stores/<id>/assets/…` |
| Graph export | `graph/<store_id>.json` |
| MCP | `db/commerce_mcp.py` |
| Shopify pack push | `shop/push_listings.py --store <id>` |

## How bgraph references commerce

```json
"commerce_link": {
  "r2_commerce_prefix": "commerce/stores/oddhobb",
  "pack_path": "oddhobbies/stores/oddhobb",
  "graph_export": "oddhobbies/graph/oddhobb.json",
  "product_library_ref": "r2://…/content/stores/oddhobb/product-library/links.json"
}
```

## Content ↔ products

| From | To |
|------|-----|
| bgraph content_type | `references_products` → commerce_ref |
| content sidecar | `product_links[]` = commerce SKUs |
| product-library/links.json | asset_refs → commerce asset paths |

**Never** store unit costs in bgraph.

## Adding a brand’s commerce side

1. `oddhobbies/stores/<store_id>/store.json`  
2. Listing packs  
3. `python3 oddhobbies/db/seed_store.py --store <store_id>`  
4. `python3 oddhobbies/db/export_graph.py --store <store_id>`  
5. Point bgraph `commerce_link` at those paths  

See oddhobbies `docs/commerce/` + `stores/README.md`.
