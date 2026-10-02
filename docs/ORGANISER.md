# ORGANISER — graph model

## Nodes

| Type | Key | Example |
|------|-----|---------|
| store | `store_id` | `oddhobb` |
| identity | `identity:<store_id>` | OddHobb · @oddhobbstudio · oddhobb.com |
| branch | `<store_id>/<platform>` | `oddhobb/youtube` |
| content_type | `<store_id>/<branch>/<type>` | `oddhobb/youtube/longform` |
| r2_layout | path prefix | `content/stores/oddhobb/youtube/longform` |
| method | `method:<id>` | `yt.upload.unlisted_then_public` |
| commerce_ref | store catalog | `commerce:oddhobb` |

## Edges

| Relation | From → To |
|----------|-----------|
| has_identity | store → identity |
| owns_branch | identity → branch |
| accepts | branch → content_type |
| stores_in | content_type → r2_layout |
| published_via | content_type → method |
| references_products | content_type → commerce_ref |
| measures | branch → analytics_slot |

## R2 layout (per branch)

```
content/stores/<store_id>/<branch>/
  <content_type>/
    raw/ edit|cuts/ masters/ thumbnails|covers/ scripts|chapters/
    metadata/<content_id>.json
```

Plus:

```
content/stores/<store_id>/_manifest/index.json
content/stores/<store_id>/product-library/links.json
content/stores/<store_id>/analytics/<branch>/
```

## content_id convention

```
<store_id>-<branch>-<type>-<slug>-<yyyymmdd>
oddhobb-youtube-longform-brick-couple-unboxing-20261002
```

## Sidecar metadata (minimal)

```json
{
  "content_id": "...",
  "store_id": "oddhobb",
  "branch": "youtube",
  "content_type": "longform",
  "status": "idea|raw|edit|ready|published|archived",
  "r2": {"master": "r2://...", "thumbnail": "r2://..."},
  "product_links": ["XMAS-3D-ORNAMENT"],
  "asset_refs": ["r2://.../commerce/stores/oddhobb/assets/..."],
  "channel": {"youtube": {"video_id": null}},
  "analytics": {"last_pull": null}
}
```

## Methods (shared contracts)

| method_id | When | Gate |
|-----------|------|------|
| ingest.local_or_r2 | drop master into branch | none |
| organise.folder | move raw → typed folder | none |
| package.from_listing | title/desc/tags from oddhobbies pack | none |
| publish.human_confirm | any platform publish | **human** |
| measure.analytics_pull | write analytics JSON | read-only |
| optimise.join_later | retention × products × orders | later |

## Company-graph alignment

| bgraph | company graph |
|--------|----------------|
| store | company / store resource |
| identity.domain/email/phone | resource nodes |
| branch.account.handle | social resource |
| method.auth_ref | credential_ref (name only) |
