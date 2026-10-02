# CHANNELS — Shopify, Etsy, socials

## Shopify

| Path | Tool | Source |
|------|------|--------|
| Pack SKUs (15 oddhobb) | `oddhobbies/shop/push_listings.py` | stores/oddhobb/listings |
| Mesh/personalised products | `pogpet/shopify-app/scripts/sync-catalog.mjs` | `/backend/api/feeds/shopify.json` |

| Field | Value |
|-------|-------|
| Store | `byg8sv-p6.myshopify.com` (OddHobb) |
| Auth | vault `SHOPIFY_*` · token `shpat_` |
| Idempotency | handle / sku |

**Unify later:** map feed ids ↔ commerce SKUs; one upsert script.

## Etsy

| Field | Value |
|-------|-------|
| Shop | PogPet `67863887` (legacy drafts) |
| Packs | oddhobbies listing packs |
| Auth | OAuth laptop — **blocked on this VPS** |
| Write path | packs → API after re-auth |

Brand public name = OddHobb (not PogPet).

## Social branches (bgraph)

Per brand `branches[]`:

| Platform | Default content | Publish gate |
|----------|-----------------|--------------|
| youtube | longform, short | human_confirm |
| instagram | vertical, post | human_confirm |
| tiktok | vertical | human_confirm |
| pinterest | post, vertical | human_confirm |
| x | post | human_confirm |

Handles locked in oddhobbies SOCIALS + bgraph identity.

## Later executors

Postiz / OpenPost / TryPost — one instance, **workspace = store_id**.  
bgraph defines methods; executors implement them.

## Ads

| Layer | Location |
|-------|----------|
| Campaigns / creatives tables | oddhobbies commerce.db |
| Creative sources | product assets + content masters |
| Spend | human grant (QP later) |

See [ADS-ANALYTICS.md](ADS-ANALYTICS.md).
