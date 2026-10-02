# TODO — autonomous work queue

Work top-down. **Validate + tests before done.** Organiser only.

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 scripts/brand_status.py
python3 -m pytest tests/ -q
```

| # | Task | Status |
|---|------|--------|
| 1 | Scaffold repo + AGENTS/README/ARCHITECTURE spine | [x] |
| 2 | Schemas brand-organiser.v1 + content_type.v1 + method.v1 | [x] |
| 3 | Registry channels + content_types + methods | [x] |
| 4 | Template + instantiate_brand.py | [x] |
| 5 | Seed brands oddhobb / grimoirer / stonedoorway | [x] |
| 6 | validate.py + export_graph.py + brand_status.py + r2_layout.py | [x] |
| 7 | Full docs: integrations + operations + R2 + publish methods | [x] |
| 8 | Tests (validate, export, status, instantiate, gates, docs) | [x] |
| 9 | RESOURCES.md + spine pointers in oddhobbies + pogpet | [x] |
| 10 | Commit bgraph as beautiful objective structure | [x] |

## After the 10

- Content sidecar schema + R2 upload script  
- `content_items` in oddhobbies commerce.db  
- Postiz/OpenPost workspace per store_id  
- YouTube analytics OAuth + pull into R2  
- Company-graph nodes for three brands  
- Shopify feed ↔ commerce SKU unify  
