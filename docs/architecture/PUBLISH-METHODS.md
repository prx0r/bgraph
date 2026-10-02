# Publish methods

Methods are **contracts**, not code. Executors (Postiz, OpenPost, manual UI)
plug in later. **v1 law: social publish is always `human_confirm`.**

## Stages

| Stage | Purpose | Typical gate |
|-------|---------|--------------|
| ingest | file enters R2 raw/ | none |
| organise | move to typed folder + sidecar | none |
| package | title/desc/tags from commerce pack | none |
| publish | platform upload | **human_confirm** |
| measure | analytics → R2 analytics/ | none |
| optimise | join analytics × products × orders | later |

## Shared method_ids

| method_id | stage | outputs |
|-----------|-------|---------|
| ingest.local_or_r2 | ingest | raw object |
| organise.folder | organise | typed object + metadata |
| package.from_listing | package | package_json |
| publish.human_confirm | publish | publish_task → platform_id |
| measure.analytics_pull | measure | analytics_json |
| optimise.join_later | optimise | report |

## Branch posting methods

| method_id | Platform | Kind | Gate |
|-----------|----------|------|------|
| yt.upload.unlisted_then_public | YouTube | youtube_upload | human_confirm |
| ig.publish.human | Instagram | instagram_publish | human_confirm |
| tt.publish.human | TikTok | tiktok_publish | human_confirm |
| pin.publish.human | Pinterest | pinterest_publish | human_confirm |
| x.publish.human | X | x_publish | human_confirm |

### YouTube note

Upload **unlisted** → human flips public (sleepintel CHANNEL_PIPELINE pattern).

## Package source

`package.from_listing` pulls from oddhobbies:

```
stores/<store_id>/listings/<SKU>.json
  etsy_title, tags, description, agent_sku, price
store.json style_lock + voice
```

## Analytics tools (later)

| Branch | Tool | Sink |
|--------|------|------|
| youtube | youtube-analytics-cli / MCP | `content/stores/<id>/analytics/youtube/` |
| others | TBD | `analytics/<branch>/` |

Metrics default: views, avg_view_duration, subscribers_gained.

## Future gates

| Gate | When |
|------|------|
| human_confirm | today |
| qp_grant | after cmail/qp effect gateway wired for publish |

Never auto-public without a receipt.
