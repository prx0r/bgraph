# bgraph — brand identity graph

**Objective organiser for multi-brand social/content structure.**  
Create the graph once. Every new store instantiates it.

| Layer | Lives in |
|-------|----------|
| Products, listings, assets, orders | `oddhobbies` commerce core |
| Brand identity + branches + content methods | **bgraph** |
| R2 media files | `powpowpow-warehouse/.../content/stores/<store_id>/` |
| Publish executors | later: Postiz / OpenPost / influence |
| YouTube analytics pulls | later: youtube-analytics-cli / MCP |

## What this is

- Identity graph per brand (OddHobb, Grimoirer, StoneDoorway, …)
- Social **branches** (youtube, instagram, tiktok, pinterest, x)
- **Content types** (longform, short, vertical, post, ad) with R2 layouts
- **Methods** (ingest → organise → package → publish → measure)
- **Exports** as graph JSON for agents / company-graph alignment
- **Templates** so a new brand is one instantiate call

## What this is not

- Not a video editor
- Not a scheduler (Postiz/OpenPost later)
- Not product truth (oddhobbies owns SKUs/costs)
- Not sleepintel’s 244-channel sleep network (that repo stays separate)

## Quick start

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 -m pytest tests/ -q

# new brand from template
python3 scripts/instantiate_brand.py \
  --template brand.template.json \
  --store-id mybrand \
  --name "MyBrand" \
  --domain mybrand.com
```

## Brands seeded

| store_id | Status |
|----------|--------|
| oddhobb | pilot — all main branches |
| grimoirer | scholarly subset |
| stonedoorway | empty scaffold until thesis |

## Docs

| Doc | Purpose |
|-----|---------|
| `docs/SYSTEM.md` | Map of the map |
| `docs/ORGANISER.md` | Graph model + R2 layout + methods |
| `docs/NEW-BRAND.md` | Instantiation checklist |
| `RESOURCES.md` | External repos to steal patterns from |
| `TODO.md` | 10 autonomous work items |

## Layout

```
bgraph/
  AGENTS.md
  README.md
  RESOURCES.md
  TODO.md
  docs/
  schemas/           # brand-organiser.v1, content_type.v1, method.v1
  registry/
    brands/          # per-store organiser.json instances
    channels/        # platform capability + method contracts
    content_types/   # longform/short/vertical/post/ad
    methods/         # ingest/organise/package/publish/measure
  templates/         # new-brand starter
  scripts/           # validate, export, instantiate
  tests/
  exports/           # generated graph JSON (gitignored runtime or committed snapshots)
  data/              # optional local working copies
```
