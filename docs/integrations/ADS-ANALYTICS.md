# ADS-ANALYTICS — later spine, schema now

## Ads (schema lives in commerce)

oddhobbies `commerce.db`:

- `ad_campaigns` (store_id, channel, budget, status)  
- `ad_creatives` (product_id, asset_id, copy, destination)  
- `ad_spend_ledger`  

**bgraph role:** content types + R2 masters feed creatives; methods gate spend (`qp_grant` later).

Readiness view: `v_ad_readiness` (price + assets + live listing).

## Analytics

| Branch | Tool (later) | Sink |
|--------|--------------|------|
| youtube | youtube-analytics-cli / MCP | `content/stores/<id>/analytics/youtube/` |
| others | TBD | `analytics/<branch>/` |

Sidecar fields:

```json
"analytics": {
  "last_pull": null,
  "views": null,
  "retention_pct": null,
  "avg_view_duration": null
}
```

## Optimise (phase 2)

```
analytics × product_links × commerce.orders
  → what content moves money
  → next content queue
```

method_id: `optimise.join_later` — not implemented in v1.

## Sleepintel parallel

sleepintel scores 244 sleep channels. bgraph scores **3 brands’ branches** the same way later — same export shape, different corpus.
