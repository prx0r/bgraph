# INTEGRATIONS — how bgraph talks to the rest

## Map

| System | Repo / path | Role | Join key |
|--------|-------------|------|----------|
| **bgraph** | `/root/bgraph` | Identity + branches + methods | `store_id` |
| **Commerce** | `/root/oddhobbies` | Products, packs, assets, orders | `store_id` |
| **Site engine** | `/root/pogpet` | oddhobb.com multi-brand app | `BRANDS[host].store_id` |
| **Shopify** | byg8sv-p6 / feed sync | Channel catalog | handle / sku |
| **Etsy** | PogPet drafts | Discovery channel | listing_id |
| **R2** | powpowpow-warehouse | commerce + content media | path prefixes |
| **Company graph** | agentcom kernel | Brand entities + resources | store_id / domain |
| **QP law** | qprivately / cmail | Gates on publish/spend | method.gate |
| **Publishers** | Postiz/OpenPost (later) | Execute posting_methods | branch_id |

Detail: [SITE.md](SITE.md) · [COMMERCE.md](COMMERCE.md) · [CHANNELS.md](CHANNELS.md) · [ADS-ANALYTICS.md](ADS-ANALYTICS.md)

---

## store_id contract

| store_id | Domain | Commerce pack | Site host key | R2 content |
|----------|--------|---------------|---------------|------------|
| oddhobb | oddhobb.com | oddhobbies/stores/oddhobb | oddhobb.com | content/stores/oddhobb |
| grimoirer | grimoirer.com | oddhobbies/stores/grimoirer | grimoirer.com | content/stores/grimoirer |
| stonedoorway | stonedoorway.com | oddhobbies/stores/stonedoorway | stonedoorway.com | content/stores/stonedoorway |

**Never invent a second id.** If it’s not in `registry/brands/`, it isn’t a bgraph brand.

---

## Read paths (who reads bgraph)

| Consumer | How |
|----------|-----|
| Agents | `exports/<store_id>.json` or registry JSON |
| oddhobbies docs | pointer to bgraph for branches/methods |
| pogpet | `BRANDS[host].bgraph` path + store_id |
| Dashboards | brand_status + graph export |

## Write paths (who writes bgraph)

| Writer | What |
|--------|------|
| Humans / agents | `registry/brands/*.json` via instantiate + edit |
| Never | Commerce packs write into bgraph |
| Never | Site code writes into bgraph |

---

## Data flow example (OddHobb longform)

1. bgraph: `oddhobb/youtube` accepts `longform` · method publish.human_confirm  
2. oddhobbies: listing pack `XMAS-3D-ORNAMENT` + assets  
3. R2: drop master under `content/stores/oddhobb/youtube/longform/raw/`  
4. organise + package from listing pack  
5. Human confirms publish → YouTube video_id  
6. analytics pull → `analytics/youtube/`  
7. Later: join with commerce orders for optimise  

---

## Company graph alignment

Export bgraph → optional company-graph nodes:

```
brand/store  ← store_id
domain       ← identity.domain
email/phone  ← identity.*
social       ← branch.account.handle
credential_ref ← method auth_ref names only
```
