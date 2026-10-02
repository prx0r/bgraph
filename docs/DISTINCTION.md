# DISTINCTION — what lives where

> **bgraph = spine.** oddhobbies = product truth. pogpet = site. influence = ops. qprivately = law.

---

## The five lines (memorize)

```
bgraph      identity + methods + agent contracts
oddhobbies  products + packs + orders + consumer catalog data
pogpet      website + mesh pipeline + fulfilment UI
influence   inbox + human tasks + domain/social ops
qprivately  law (grants / gates / receipts)
```

---

## bgraph vs oddhobbies

| | **bgraph** | **oddhobbies** |
|--|------------|----------------|
| **Question it answers** | What brands exist? Which channels? Which tools can agents call? | What do we sell? What does it cost? What’s the listing pack? |
| **Key files** | `registry/brands/*.json`, `agent_surfaces/`, schemas | `stores/*/listings/*.json`, `db/commerce.db`, `consumer_mcp.py` |
| **store_id role** | Defines identity graph per store | Holds product truth per store |
| **Holds prices?** | No — points at packs | Yes (retail + unit cost) |
| **Holds orders?** | No | Yes (schema + sales) |
| **Holds mesh/jobs?** | No | No — pogpet does |
| **MCP** | Documents consumer tool *contract* | Implements `consumer_mcp.py` |

**Rule:** bgraph points at oddhobbies. Never the reverse as “truth”.

---

## bgraph vs pogpet

| | **bgraph** | **pogpet** |
|--|------------|------------|
| Job | Brand graph + agent surface specs | Live oddhobb.com + mesh/print |
| Brands | store_id registry | `BRANDS[host]` in `backend/config.py` |
| New brand | instantiate + edit JSON | Add host + tunnel + BRANDS entry |

Both use the **same store_id**. bgraph describes; pogpet serves.

---

## bgraph vs influence

| | **bgraph** | **influence** |
|--|------------|---------------|
| Job | What stores/channels/tools exist | Inbox, desk, human tasks, passports |
| Playbooks | `RESOURCES.md` (structure) | `products/OS.md` + `resources.md` (ops/agent stack) |

Influence OS map: factories → plane → doors.  
bgraph is part of the **spine/plane**. Consumer MCP is a **door**.

---

## bgraph vs qprivately

| | **bgraph** | **qprivately** |
|--|------------|----------------|
| Job | Policy surface (what may be published) | Law (how effects settle) |
| Today | methods `gate: human_confirm` | Pattern only; no live receipts on stores yet |

---

## Quick “where do I…?”

| I want to… | Go to |
|------------|--------|
| Add a brand | bgraph `instantiate_brand` + oddhobbies `stores/<id>/` + pogpet BRANDS |
| Edit a product pack | oddhobbies `stores/<id>/listings/` |
| Talk to ChatGPT/Muse | `oddhobbies/db/consumer_mcp.py` + bgraph agent_surfaces |
| Fix the website | pogpet |
| Check inbox / buy domains | influence |
| Understand QP law | qprivately + influence `qp/` |
| Steal a publish/ads pattern | bgraph `RESOURCES.md` + influence `resources.md` |
