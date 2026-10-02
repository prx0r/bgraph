# SYSTEM — how bgraph works

## The loop

1. **Identity** — brand/store locked (domain, email, phone, handles, voice).
2. **Branches** — each social platform is a graph branch with account + methods.
3. **Content types** — longform / short / vertical / post / ad define R2 layout + constraints.
4. **Methods** — ingest → organise → package → publish → measure (contracts).
5. **Export** — graph JSON for agents, oddhobbies commerce links, company-graph edges.
6. **Instantiate** — copy template → fill store_id → new brand ready for packs in oddhobbies.

## Organs (who does what)

| Organ | Repo | Role |
|-------|------|------|
| **bgraph** | this repo | Identity graph + methods (controller) |
| **commerce** | oddhobbies | Products, listings, assets, orders |
| **R2** | powpowpow-warehouse | Files under `content/stores/<id>/` |
| **publish** | Postiz/OpenPost/influence later | Execute posting_methods |
| **sleepintel** | /root/sleepintel | Separate sleep-YouTube network (pattern only) |
| **company graph** | agentcom kernel | Brand entities + credential_refs |
| **QP law** | qprivately / cmail | Gates on consequential effects |

## Laws

- Organiser only — no content creation code paths.
- store_id matches oddhobbies + R2 prefix.
- Methods are JSON contracts; executors plug in later.
- Publish always human-gated until QP receipts exist.
- Secrets never in registry files — `auth_ref` only.

## Export shape

`exports/<store_id>.json`:

```
store → identity → branch → content_type → r2_layout
                      │              └→ method
                      └→ account
content_type → commerce.product_library (oddhobbies graph ref)
```

## Validation

```bash
python3 scripts/validate.py   # schemas + brands + channels + methods
python3 scripts/export_graph.py
python3 -m pytest tests/ -q
```
