# THE-STACK — how all the repos fit

> **bgraph is the spine.** Other repos are engines, sites, ops, and law.
> One key everywhere: `store_id` ∈ { `oddhobb`, `grimoirer`, `stonedoorway`, … }

---

## Map

```
                    ┌──────────────────────────┐
                    │   LAW  qprivately        │
                    │   + influence law/acom   │
                    │   + cmail qp/            │
                    │   grants · gates ·       │
                    │   receipts               │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │  SPINE  bgraph (THIS)    │
                    │  brands · branches ·     │
                    │  methods · agent MCP     │
                    │  contracts · exports     │
                    └────────────┬─────────────┘
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
   oddhobbies               pogpet site               R2
   PRODUCT TRUTH            SITE / FULFILMENT         MEDIA
   packs · costs            oddhobb.com               commerce/stores/<id>/
   listings · orders        grimoirer.com             content/stores/<id>/
   consumer_mcp data        mesh → print
          │                      │
          └──────────┬───────────┘
                     ▼
            DOORS (what users/agents touch)
            Shopify · Etsy · consumer MCP
            ChatGPT / Muse / Grok · site UI
                     │
                     ▼
            OPS  influence
            cmail inbox · steve desk
            domain/social ops · passports
```

---

## Distinction (one table)

| Repo | Owns | Does **not** own |
|------|------|------------------|
| **bgraph** | Brand identity graph, branches, content methods, agent-surface contracts, store_id spine | Products, costs, mesh, inbox |
| **oddhobbies** | Product truth: packs, costs, listings, assets labels, ads/sales schema, consumer catalog data | Brand graph, social branches |
| **pogpet** | Live site + photo→mesh→print + multi-brand Host map | Catalog truth, brand graph |
| **influence** | Ops plane: inbox, human tasks, passports, domain/social ops | Product truth, mesh |
| **qprivately** | Law: grants/gates/receipts | Product runtime |

---

## store_id contract

| store_id | Domain | Commerce pack | Site host key |
|----------|--------|---------------|---------------|
| oddhobb | oddhobb.com | oddhobbies/stores/oddhobb | oddhobb.com |
| grimoirer | grimoirer.com | oddhobbies/stores/grimoirer | grimoirer.com |
| stonedoorway | stonedoorway.com | oddhobbies/stores/stonedoorway | stonedoorway.com |

R2:

```
commerce/stores/<store_id>/assets/   # product images (oddhobbies)
content/stores/<store_id>/…          # social content (bgraph contract)
```

---

## Agent door (already built)

| Piece | Path |
|-------|------|
| Consumer MCP | `oddhobbies/db/consumer_mcp.py` |
| Tool contract | `bgraph/registry/agent_surfaces/consumer_mcp.json` |
| Theory | `bgraph/docs/architecture/AGENT-SURFACE.md` |

**Chain:** search → upload_photo → photo/mesh status → quote → Shopify checkout URL → order status.

ChatGPT / Muse / Grok all attach to this MCP — doors, not second kernels.

---

## Playbooks (steal, don’t rebuild)

| Source | Use when |
|--------|----------|
| `bgraph/RESOURCES.md` | Brand structure, publishing, YT, R2 media |
| `influence/products/OS.md` | How factories/plane/doors compose |
| `influence/resources.md` | Agent law, connectors, Jev, monid |
| `influence/docs/GUIDE.md` | Daily ops (desk, domain buy) |
| `qprivately` | Grant/gate/receipt law |

---

## Daily loop (spine only)

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 scripts/brand_status.py
python3 -m pytest tests/ -q
```

Commerce ops live in oddhobbies. Site ops live in pogpet. Inbox/ops live in influence.

---

## Read next

- Distinction detail: [DISTINCTION.md](DISTINCTION.md)
- Brand add: [operations/BRAND-ADD.md](operations/BRAND-ADD.md)
- Agent surface: [architecture/AGENT-SURFACE.md](architecture/AGENT-SURFACE.md)
- Commerce map: `/root/oddhobbies/docs/commerce/SITE-LINK.md`
