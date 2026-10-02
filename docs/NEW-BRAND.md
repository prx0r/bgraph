# New brand checklist

1. Instantiate from template:

```bash
python3 scripts/instantiate_brand.py \
  --template templates/brand.template.json \
  --store-id newbrand \
  --name "NewBrand" \
  --domain newbrand.com \
  --email hello@newbrand.com
```

2. Edit `registry/brands/newbrand.json`:
   - voice + style_lock
   - live branches (youtube / instagram / …)
   - handles (claim status)
   - commerce_link.pack_path → oddhobbies `stores/newbrand`

3. Create matching oddhobbies pack:
   - `oddhobbies/stores/newbrand/store.json`
   - listing packs + `identity.socials`

4. R2 prefix convention:
   - `commerce/stores/newbrand/assets/`
   - `content/stores/newbrand/...`

5. Validate + export:

```bash
python3 scripts/validate.py
python3 scripts/export_graph.py --store newbrand
```

6. Human claims: social handles, email test, Telnyx if shared phone.

7. Only then: content calendars, Postiz workspace, analytics OAuth.

## Do not

- Fork a new schema per brand
- Put secrets in `registry/brands/*.json`
- Publish without human confirm
- Treat bgraph as the product catalog
