# AGENTS.md — bgraph (the spine)

> **You are the organiser.** This repo is the objective brand graph.
> Every store you add, every branch you enable, every method you define
> lives here first. Commerce truth is elsewhere. This is the spine.

---

## What this is

A **git-structured, schema-backed identity graph** for multi-brand commerce:

- `store_id` keys every system (site, commerce, R2, ads)
- **Branches** = social platforms (youtube, instagram, …)
- **Content types** = longform, short, vertical, post, ad
- **Methods** = ingest → organise → package → publish → measure
- **Exports** = graph JSON for agents and other repos
- **Templates** = new brand in one command

Controller only — **never** render content, **never** auto-publish.

---

## Read in this order

1. `README.md`
2. `docs/architecture/ARCHITECTURE.md`
3. `docs/integrations/INTEGRATIONS.md`
4. `docs/operations/BRAND-ADD.md`
5. `registry/brands/*.json`
6. `TODO.md` / `RESOURCES.md`

---

## Daily loop

```bash
cd /root/bgraph
python3 scripts/validate.py
python3 scripts/export_graph.py
python3 scripts/brand_status.py
python3 -m pytest tests/ -q
```

---

## Laws

1. **Spine, not engine** — no content creation, no channel SDKs.
2. **One schema** — `brand-organiser.v1` for every brand.
3. **store_id is sacred** — matches oddhobbies + pogpet + R2 paths.
4. **Methods are contracts** — JSON; executors plug in later.
5. **Publish gate = human_confirm** until QP receipts exist.
6. **Secrets = vault names only** — never tokens in `registry/`.
7. **Product truth = oddhobbies** — bgraph points at packs/graph.
8. **Site hosts = pogpet BRANDS map** — domains key into this graph.
9. **Validate before claim** — green tests before “done”.
10. **Owner pushes git** — commit locally when asked.

---

## Adding a brand (summary)

```bash
python3 scripts/instantiate_brand.py --store-id X --name "X" --domain x.com
# edit registry/brands/X.json
# create oddhobbies/stores/X/
# add pogpet BRANDS host
# CF zone + email + tunnel
python3 scripts/validate.py && python3 scripts/export_graph.py
```

Full checklist: `docs/operations/BRAND-ADD.md`

---

## When stuck

| Problem | Go to |
|---------|-------|
| Validate fails | `docs/operations/DAILY-LOOP.md` |
| New brand missing fields | `docs/operations/BRAND-ADD.md` |
| How site links | `docs/integrations/SITE.md` |
| How commerce links | `docs/integrations/COMMERCE.md` |
| R2 paths | `docs/architecture/R2-CONTENT.md` |
| What to steal externally | `RESOURCES.md` |
