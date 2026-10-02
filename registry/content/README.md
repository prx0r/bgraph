# /content — structure stub (not a pipeline)

**P0/P1:** define where content lives. **Not built:** upload/render/publish code.

## Contracts already in bgraph

| Doc | Path |
|-----|------|
| Content types | `registry/content_types/content_types.yaml` |
| R2 layout | `docs/architecture/R2-CONTENT.md` |
| Branches | `registry/brands/*.json` → `branches[]` |
| Methods | `registry/methods/methods.yaml` |

## Engines

See `registry/engines.yaml` → `content` engine (R2 `content/stores/<store_id>/`).

## Calendar stub (P1 — fill when ready)

`data/calendars/<store_id>.json`:

```json
{
  "store_id": "oddhobb",
  "week": "2026-W41",
  "slots": [
    {"day": "Mon", "branch": "youtube", "content_type": "longform", "sku_hint": "XMAS-3D-ORNAMENT", "status": "idea"}
  ]
}
```

## How content slots into coordination

```
score → actuate (brand_ready / content_tree_ok)
  → later: content engine ingest
  → publish.human_confirm (bgraph law)
  → measure.analytics_pull
```

## Resources that slot in (when we build content)

| From RESOURCES | Use |
|----------------|-----|
| nerranetwork | R2 sidecars + ACL pattern |
| vms | Source/Cut/Review/Final folders |
| Postiz/OpenPost | publish later |
| YT analytics MCP | measure later |
