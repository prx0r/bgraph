# AGENTS.md — bgraph (read first)

**bgraph is the brand identity organiser.**  
It does **not** create content. It defines, for each brand/store: identity, social branches, content types, R2 layouts, and posting methods. New brands instantiate the same graph.

Controller only — same law as sleepintel: **renders nothing**. Commerce truth lives in `oddhobbies`. Publish executors live in Postiz/influence later.

## Start here

1. `README.md`
2. `docs/SYSTEM.md`
3. `docs/ORGANISER.md`
4. `schemas/*.json`
5. `registry/brands/*.json` + `registry/channels.yaml`
6. `TODO.md` — autonomous work queue
7. `RESOURCES.md` — external patterns

## Daily loop (autonomous)

```bash
python3 scripts/validate.py
python3 scripts/export_graph.py          # graph exports for all brands
python3 scripts/instantiate_brand.py --template oddhobb --store-id <new_id>
python3 -m pytest tests/ -q
```

## Laws

1. **Organiser, not creator** — no scripts that render/upload content.
2. **One schema** — every brand is the same graph shape.
3. **store_id is the key** — matches oddhobbies commerce + R2.
4. **Methods are contracts** — JSON methods, not provider SDKs.
5. **Human gate on publish** — never auto-public.
6. **Secrets stay in vault** — `auth_ref` names only.
7. **Product truth lives in commerce** — bgraph points at it.
8. **Validate before claim** — green tests before “done”.
