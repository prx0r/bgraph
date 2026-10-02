# TODO — autonomous work queue

Ten items. Work top-down. **Validate before marking done.**  
Organiser only — no content creation, no auto-publish.

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 -m pytest tests/ -q
```

| # | Task | Done when | Status |
|---|------|-----------|--------|
| 1 | Scaffold repo + AGENTS/README/SYSTEM/ORGANISER | files exist; validate passes | [x] |
| 2 | Schemas brand-organiser.v1 + content_type.v1 + method.v1 | schemas present | [x] |
| 3 | Registry: platforms.yaml, content_types.yaml, methods.yaml | validate OK | [x] |
| 4 | Template `templates/brand.template.json` | instantiable | [x] |
| 5 | Seed brands oddhobb, grimoirer, stonedoorway | `registry/brands/*.json` | [x] |
| 6 | `scripts/validate.py` green | exit 0 | [x] |
| 7 | `scripts/export_graph.py` → `exports/*.json` | 3 graphs | [x] |
| 8 | `scripts/instantiate_brand.py` + tests | pytest green | [x] |
| 9 | RESOURCES.md + this TODO | committed in repo | [x] |
| 10 | Align oddhobbies docs pointers to bgraph | AGENTS/BRAND-STACK link `/root/bgraph` | [x] |

## Next after queue (not in the 10)

- Content sidecar schema + R2 `content/stores/` upload script (in oddhobbies or bgraph/scripts)
- `content_items` table in commerce.db
- Postiz/OpenPost workspace per store_id
- youtube-analytics-cli OAuth + analytics pull into R2
- Company-graph nodes for three brands
