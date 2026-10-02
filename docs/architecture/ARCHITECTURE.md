# ARCHITECTURE — the objective graph

## Purpose

bgraph answers: **for brand/store `X`, what identity, which channels, which content types, which R2 layout, which publish methods?**

It does **not** answer: what does product X cost? How do we mesh a photo? How do we publish a video?

Those live in oddhobbies / pogpet / (later) Postiz.

---

## Node types

| Type | Key | Example |
|------|-----|---------|
| **store** | `store_id` | `oddhobb` |
| **identity** | `identity:<store_id>` | OddHobb · @oddhobbstudio · oddhobb.com |
| **branch** | `<store_id>/<platform>` | `oddhobb/youtube` |
| **content_type** | `<store_id>/<branch>/<type>` | `oddhobb/youtube/longform` |
| **r2_layout** | path prefix | `content/stores/oddhobb/youtube/longform` |
| **method** | `method:<id>` | `publish.human_confirm` |
| **commerce_ref** | store catalog | `commerce:oddhobb` |

## Edge types

| Relation | Meaning |
|----------|---------|
| `has_identity` | store owns identity record |
| `owns_branch` | identity owns social branch |
| `accepts` | branch accepts content type |
| `stores_in` | content type files live under R2 layout |
| `published_via` | content type publishes through method |
| `references_products` | content links commerce products |
| `commerce_link` | store ↔ oddhobbies pack path |

---

## Visual

```
store:oddhobb
  │ has_identity
  ▼
identity:oddhobb ──────────────┐
  │ owns_branch                │ commerce_link
  ▼                            ▼
branch:oddhobb/youtube    commerce:oddhobb
  │ accepts                   (oddhobbies packs)
  ▼
content_type:…/longform
  │ stores_in              published_via
  ▼                            ▼
r2:content/stores/…        method:publish.human_confirm
```

---

## Instance file (registry/brands/<store_id>.json)

| Section | Contains |
|---------|----------|
| `schema_version` | `brand-organiser.v1` |
| `store_id` / `brand_id` | hard keys |
| `identity` | display_name, handle, domain, email, phone, voice, style_lock |
| `commerce_link` | pack_path, r2 commerce prefix, graph export |
| `site` | pogpet repo, primary_host, alias_hosts |
| `branches[]` | platform, account, content_types, posting_methods, r2_layout, analytics |
| `content_type_registry` | longform/short/… constraints |
| `pipeline_methods` | high-level stage map |

---

## Channel registry

`registry/channels/platforms.yaml` — per-platform:

- handle rules (X: no dots · IG: periods OK)
- default content types
- default posting methods + **gate**
- analytics tool + metrics

---

## Content type registry

`registry/content_types/content_types.yaml`

| Type | Ratio | Products? | Default methods |
|------|-------|-----------|-----------------|
| longform | 16:9 | yes | ingest→organise→package→publish→measure |
| short | 9:16 ≤60s | yes | ingest→organise→package→publish |
| vertical | 9:16 ≤90s | yes | ingest→organise→publish |
| post | 1:1/4:5/2:3 | yes | ingest→organise→package→publish |
| ad | mixed | yes | reuse masters + product assets |

---

## Method registry

`registry/methods/methods.yaml`

| Stage | method_id | Gate |
|-------|-----------|------|
| ingest | ingest.local_or_r2 | none |
| organise | organise.folder | none |
| package | package.from_listing | none |
| publish | publish.human_confirm | **human_confirm** |
| measure | measure.analytics_pull | none |
| optimise | optimise.join_later | none |

Social publish methods (`yt.*`, `ig.*`, `tt.*`, `pin.*`, `x.*`) **must** be `human_confirm` in v1.

---

## Graph export

```bash
python3 scripts/export_graph.py
# → exports/<store_id>.json
```

```json
{
  "schema_version": "bgraph-export.v1",
  "store_id": "oddhobb",
  "nodes": [...],
  "edges": [...],
  "counts": {"nodes": 26, "edges": 39}
}
```

Consumers: agents, company-graph alignment, dashboards.

---

## company-graph alignment

| bgraph | agentcom CompanyGraph |
|--------|----------------------|
| store | company / store resource |
| identity.domain/email/phone | resource nodes |
| branch.account.handle | social resource |
| method auth_ref | credential_ref (name only) |

---

## Evolution rules

- New platform = channel registry entry + optional brand branch
- New content type = content_types.yaml + template defaults
- New method = methods.yaml + human/QP gate declared
- Never fork schema per brand
- Never store API keys in registry
