# BRAND-ADD — add a store to the spine

## Checklist

### 1. bgraph

```bash
python3 scripts/instantiate_brand.py \
  --store-id mybrand \
  --name "MyBrand" \
  --domain mybrand.com \
  --email hello@mybrand.com \
  --handle @mybrand
```

Edit `registry/brands/mybrand.json`:

- [ ] `identity.voice` + `style_lock`
- [ ] Live branches (enable youtube/instagram/…)
- [ ] Handles + claim status
- [ ] `commerce_link` → oddhobbies paths
- [ ] `site` block → pogpet host

```bash
python3 scripts/validate.py
python3 scripts/export_graph.py --store mybrand
python3 scripts/brand_status.py
```

### 2. Commerce (oddhobbies)

- [ ] `stores/mybrand/store.json`
- [ ] `listings/*.json` (first SKUs)
- [ ] `python3 db/seed_store.py --store mybrand`
- [ ] `python3 db/export_graph.py --store mybrand`

### 3. Site (pogpet)

- [ ] `BRANDS["mybrand.com"] = { store_id, support, … }` in `backend/config.py`
- [ ] Tunnel CNAME + ingress
- [ ] `GET /api/brand` returns store

### 4. Identity (Cloudflare + email)

- [ ] Zone + NS
- [ ] hello@ / orders@ Email Routing
- [ ] Shared phone if family-wide
- [ ] Social handles claimed (human)

### 5. Assets

- [ ] R2 `commerce/stores/mybrand/assets/`
- [ ] R2 `content/stores/mybrand/` tree (when content starts)
- [ ] product-library/links.json when images exist

### 6. Channels

- [ ] Shopify store + packs push (when ready)
- [ ] Etsy packs (when OAuth works)
- [ ] bgraph branches enabled

---

## Definition of done (brand scaffold)

| Check | Command / path |
|-------|----------------|
| bgraph file | `registry/brands/mybrand.json` |
| validate | `python3 scripts/validate.py` |
| export | `exports/mybrand.json` |
| commerce pack | `oddhobbies/stores/mybrand/store.json` |
| site host | pogpet BRANDS entry |
| docs pointer | oddhobbies AGENTS related repos |

## Template

Start from `templates/brand.template.json` via `instantiate_brand.py` — don’t hand-copy JSON.
