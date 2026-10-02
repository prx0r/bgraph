# bgraph — brand identity spine

**One objective graph. Every brand instantiates it.**  
Site hosts, commerce stores, social branches, content methods, R2 layouts — same shape, different `store_id`.

| This repo owns | This repo does **not** own |
|----------------|----------------------------|
| Identity + branches + content methods | Product costs / SKUs (oddhobbies) |
| store_id contract across systems | Mesh / print pipeline (pogpet) |
| Graph exports for agents | Publish execution (Postiz later) |
| Brand drop-in templates | Etsy/Shopify API calls |

---

## The spine (how systems connect)

```
                    ┌─────────────────┐
                    │     bgraph      │  identity + branches + methods
                    │  (this repo)    │
                    └────────┬────────┘
                             │ store_id
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
  oddhobbies            pogpet site           R2 media
  commerce.db           oddhobb.com           content/stores/<id>/
  packs + orders        grimoirer.com         commerce/stores/<id>/
  graph export           stonedoorway.com
        │                    │
        └──────────┬─────────┘
                   ▼
         Shopify · Etsy · ads · analytics
```

**Hard key:** `store_id` ∈ { `oddhobb`, `grimoirer`, `stonedoorway`, … }

---

## Docs map

| Doc | Read when |
|-----|-----------|
| [AGENTS.md](AGENTS.md) | Every session — laws + daily loop |
| [README.md](README.md) | What bgraph is |
| [docs/THE-STACK.md](docs/THE-STACK.md) | **How all repos fit** |
| [docs/DISTINCTION.md](docs/DISTINCTION.md) | **bgraph vs oddhobbies vs pogpet vs influence** |
| [docs/architecture/ARCHITECTURE.md](docs/architecture/ARCHITECTURE.md) | Graph model, nodes, edges |
| [docs/architecture/R2-CONTENT.md](docs/architecture/R2-CONTENT.md) | R2 folder + sidecar contract |
| [docs/architecture/PUBLISH-METHODS.md](docs/architecture/PUBLISH-METHODS.md) | Method contracts |
| [docs/architecture/AGENT-SURFACE.md](docs/architecture/AGENT-SURFACE.md) | Consumer MCP for ChatGPT/Muse |
| [docs/integrations/INTEGRATIONS.md](docs/integrations/INTEGRATIONS.md) | oddhobbies · pogpet · Shopify · Etsy · company graph |
| [docs/operations/BRAND-ADD.md](docs/operations/BRAND-ADD.md) | Add a brand end-to-end |
| [docs/operations/DAILY-LOOP.md](docs/operations/DAILY-LOOP.md) | Validate, export, status |
| [RESOURCES.md](RESOURCES.md) | External patterns + influence playbooks |
| [TODO.md](TODO.md) | Work queue |

---

## Quick start

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 scripts/brand_status.py
python3 -m pytest tests/ -q

# add a brand
python3 scripts/instantiate_brand.py \
  --store-id mybrand \
  --name "MyBrand" \
  --domain mybrand.com \
  --email hello@mybrand.com
```

---

## Current brands

| store_id | Domain | Site | Commerce | Status |
|----------|--------|------|----------|--------|
| **oddhobb** | oddhobb.com | pogpet multi-brand | oddhobbies/stores/oddhobb | active |
| **grimoirer** | grimoirer.com | pogpet multi-brand | oddhobbies/stores/grimoirer | active |
| **stonedoorway** | stonedoorway.com | pogpet multi-brand | oddhobbies/stores/stonedoorway | scaffold |

---

## Layout

```
bgraph/
  AGENTS.md  README.md  RESOURCES.md  TODO.md
  docs/
    architecture/   ARCHITECTURE · R2-CONTENT · PUBLISH-METHODS
    integrations/   INTEGRATIONS · SITE · COMMERCE · ADS-ANALYTICS
    operations/     BRAND-ADD · DAILY-LOOP
  schemas/          brand-organiser.v1 · content_type.v1 · method.v1
  registry/
    brands/         <store_id>.json   ← one file per brand
    channels/       platforms.yaml
    content_types/  content_types.yaml
    methods/        methods.yaml
  templates/        brand.template.json
  scripts/          validate · export_graph · instantiate · brand_status
  tests/
  exports/          <store_id>.json graph snapshots
```
