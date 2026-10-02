# Agent surface — consumer MCP (ChatGPT / Muse / Grok)

**Theory:** official OpenAI ChatGPT plugins = remote MCP + optional UI.  
**Rule:** one MCP · `store_id` param · 6 tools · annotations on every tool · no costs/secrets in output.

## Connect (ChatGPT developer mode)

```
https://mcp.oddhobb.com/mcp
# or local/dev:
# oddhobbies/db/consumer_mcp.py  (stdio)
```

Param on every tool: `store_id` ∈ {`oddhobb`, `grimoirer`, `stonedoorway`}  
(or omit → default oddhobb via brand host later).

## Tool surface (full chain)

| Tool | Step | Annotations |
|------|------|-------------|
| `search_products` | catalog | readOnly · openWorld=false · destructive=false |
| `get_product` | specifics | readOnly |
| `upload_photo` | person/dog image | write · openWorld=false · destructive=false |
| `get_photo_status` | machine view + mesh job | readOnly |
| `get_quote` | pricing + fulfilment | readOnly |
| `start_checkout` | reserve → Shopify checkout URL | write · openWorld=true · destructive=false |
| `get_order_status` | order lookup | readOnly |

## Chain (Muse / ChatGPT)

```
upload_photo(store_id, file_b64 or url)
  → photo_id
get_photo_status(photo_id)
  → machine view (subject, qc) + mesh_status + preview_url
search_products(store_id) / get_product(store_id, sku)
  → products that accept this mesh/person
get_quote(store_id, sku, options)
  → price tier + fulfilment blurb (no unit costs)
start_checkout(store_id, sku, photo_id, customer_email)
  → { checkout_url, order_ref }  # Shopify / site
get_order_status(store_id, order_ref)
  → status
```

## What agents never see

Unit costs · vault keys · ops MCP · supplier APIs · internal IDs beyond order_ref/photo_id.

## Later

- Domain verification for public plugin
- Muse token auth (api_key)
- Plugin submission packet (5+3 tests)
- Optional widget UI

## References

- OpenAI plugins: developers.openai.com/plugins
- agentcom-plugin-canonical annotations
- pogpet Muse MCP: `/root/pogpet/docs/muse-mcp-design.md`
- Commerce consumer sketch: oddhobbies `db/CONSUMER-MCP.md`
