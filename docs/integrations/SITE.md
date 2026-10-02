# SITE — pogpet multi-brand app

**Repo:** `/root/pogpet` · **Live:** oddhobb.com  
**Pattern:** one Flask + bridge + premesh app; brands are Host config.

## Brand map (authoritative)

| store_id | Primary host | Alias | commerce pack |
|----------|--------------|-------|---------------|
| oddhobb | oddhobb.com | pog.pet | oddhobbies/stores/oddhobb |
| grimoirer | grimoirer.com | ochema.co | oddhobbies/stores/grimoirer |
| stonedoorway | stonedoorway.com | — | oddhobbies/stores/stonedoorway |

Config: `pogpet/backend/config.py` → `BRANDS[host].store_id`

## Resolution

```
GET /api/brand  → brand_for(Host)
premesh zone    → brand_for(Host)["host"]
```

Unknown host → default oddhobb (never 404 branding).

## Tunnel checklist (new host)

1. Cloudflare zone + NS  
2. Email Routing hello@ / orders@  
3. CNAME host+www → figgsite tunnel  
4. `~/.cloudflared/figgsite.yml` ingress  
5. `BRANDS` entry with `store_id`  
6. bgraph `registry/brands/<id>.json` + oddhobbies store pack  

## What the site owns

- Photo → mesh → product fan-out (Meshy, ask-first)  
- Consumer chat / gift brief  
- Prodigi print path  
- Public `/img/` mirrors + Shopify feed  

## What the site does not own

- Multi-brand product truth (oddhobbies)  
- Social branch methods (bgraph)  
- Etsy listing packs  

Full map: `/root/oddhobbies/docs/commerce/SITE-LINK.md`
