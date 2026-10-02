# COORDINATION — pi harness + Jev + human

> **Simple model:** deterministic score first, typed judge second, human on money/publish.  
> Pattern: sleepintel (controller) · Jev Choice/Noul/Score · pi as worker harness.

---

## The loop (P0 prototype)

```
score.py     readiness in code (no LLM)
     │
     ▼
actuate.py   top candidates → Jev gate
     │
     ├── auto     (conf high)     → note only in P0
     ├── confirm  (mid)           → flag for review
     └── human    (money/publish) → receipt + HOLD
     │
     ▼
data/decisions/<ts>-<id>.json   receipt
```

**P0:** dry-run only. Nothing pushes Shopify, spends, or publishes.

---

## Roles

| Role | What | What it is not |
|------|------|----------------|
| **Pi harness** | Runs scripts, reads receipts, calls MCP | Not the judge |
| **Jev** | Typed verdicts: Choice / Noul / Score + bands | Not a chatbot |
| **Human** | Money, publish, high-stakes confirm | Not optional on spend |
| **bgraph** | decisions.json + score inputs + receipts | Not the product DB |

**Key split (later):** pi thinks via one model · Jev only on its own key (funnylabs pattern).

---

## Jev primitives (stub in P0)

| Type | Use | Example |
|------|-----|---------|
| **Choice** | pick one option | which SKU next for photos |
| **Noul** | yes/no proposition | is this brand ready to push? |
| **Score** | ordered levels | listing quality 1–5 |

**Bands:** `auto` (conf ≥ 0.8) · `confirm` (≥ 0.5) · `human` (else / money / publish)

**Fail direction:** listing/spend/publish = **fail-closed** (hold) · ranking = fail-open to prior score order.

---

## Decision points (bgraph/jev/decisions.json)

| id | brand scope | question | primitive | fail |
|----|-------------|----------|-----------|------|
| brand_ready | all | pack + domain + commerce link ready? | Noul | human |
| next_photo_sku | store | which SKU gets images next? | Choice | score order |
| shopify_push_ok | store | push listing draft? | Noul | **fail-closed + human** |
| content_calendar | store | is content tree defined? | Noul | human |

---

## Stub vs live Jev

| | P0 stub | Later live |
|--|---------|------------|
| Judge | local rules in `scripts/jev.py` | Jev API (decisions.json model pin) |
| Receipts | same JSON shape | same + model id |
| Keys | none | OpenRouter/TYPESAFE for Jev only |

Receipts stay identical so calibration can switch later without rewrite.

---

## Receipt shape

```json
{
  "id": "actuate-…",
  "decision_id": "brand_ready",
  "store_id": "oddhobb",
  "primitive": "noul",
  "question": "…",
  "answer": true,
  "confidence": 0.9,
  "band": "auto",
  "action": "note",
  "fail_direction": "human",
  "model": "stub-local-v1",
  "thresholds": {"auto": 0.8, "confirm": 0.5},
  "inputs": { "score": 0.85, "packs": 15, "domain": "oddhobb.com" },
  "ts": "…"
}
```

---

## Resources that slot in naturally

| Source | Slot |
|--------|------|
| `RESOURCES.md` → influence OS.md | Factories = engines · plane = score/Jev · doors = push/MCP |
| `RESOURCES.md` → Postiz/OpenPost | Later publish engine behind methods |
| `RESOURCES.md` → YT analytics | Later `measure` engine |
| `RESOURCES.md` → nerranetwork R2 | Later content engine layout |
| `influence/resources.md` monid | Later connector shape for paid providers |
| sleepintel `jev.py` | Shape of band + receipt client |
| funnylabs pi-extension | Later pi + separate Jev key |

---

## What we do **not** build in P0

- Daemon scheduler  
- Auto Shopify push  
- Live Jev billing  
- Postiz  
- Full QP money receipts  
- Per-brand controllers  

---

## After P0 (extensions)

1. `/content` calendar stub per store  
2. `engines.yaml` names referenced by methods  
3. Live Jev when key exists  
4. pi extension wiring  
5. One real receipted action (human-confirmed push)  
