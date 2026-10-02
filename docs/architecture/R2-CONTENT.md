# R2 content layout

Canonical media tree for **social/content** files (not product commerce assets).

## Bucket + prefix

```
s3://powpowpow-warehouse/powpowpow/
  commerce/stores/<store_id>/     # product images, listing assets (oddhobbies)
  content/stores/<store_id>/      # social content (bgraph contract)
```

## Content tree (every brand, same shape)

```
content/stores/<store_id>/
  _manifest/
    index.json              # all content items (optional export)
    calendar.json           # publish plan
  product-library/
    links.json              # refs → commerce assets (no file copies)
  <branch>/                 # youtube | instagram | tiktok | pinterest | x
    <content_type>/         # longform | short | vertical | post | ad
      raw/                  # camera masters / drops
      edit|cuts/            # WIP
      masters/              # finished
      thumbnails|covers/
      scripts|chapters/
      metadata/
        <content_id>.json   # sidecar
  analytics/
    <branch>/
      <YYYY-MM>.json
```

## content_id

```
<store_id>-<branch>-<type>-<slug>-<yyyymmdd>
oddhobb-youtube-longform-brick-couple-unboxing-20261002
```

## Sidecar metadata (minimal contract)

```json
{
  "content_id": "oddhobb-youtube-longform-brick-couple-20261002",
  "store_id": "oddhobb",
  "branch": "youtube",
  "content_type": "longform",
  "status": "idea|raw|edit|ready|published|archived",
  "r2": {
    "master": "r2://powpowpow-warehouse/powpowpow/content/stores/oddhobb/youtube/longform/masters/….mp4",
    "thumbnail": "r2://…/thumbnails/….jpg"
  },
  "product_links": ["XMAS-3D-ORNAMENT"],
  "asset_refs": [
    "r2://powpowpow-warehouse/powpowpow/commerce/stores/oddhobb/assets/etsy/ACTIVE-COUPLE-FIGURE/….jpg"
  ],
  "channel": {
    "youtube": {"handle": "@oddhobbstudio", "video_id": null, "url": null}
  },
  "seo": {"hook": "", "keywords": [], "description": ""},
  "analytics": {"last_pull": null},
  "created_at": "2026-10-02T00:00:00Z",
  "published_at": null
}
```

## Pattern sources

- Sidecars + ACL: nerranetwork gallery storage
- Categories Source/Cut/Review/Final: BuildWithHussain/vms
- Commerce assets stay in `commerce/stores/<id>/assets/<SKU>/`

## Rules

1. Content **references** commerce paths — never owns product truth.
2. One content_id per master.
3. analytics/ only after publish + pull.
4. No secrets in sidecars.
5. Brand style_lock from bgraph identity + oddhobbies store.json governs visuals.
