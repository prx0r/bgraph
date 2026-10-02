#!/usr/bin/env python3
"""Thin Jev client — stub local judge + receipt writer.

P0: rule-based Choice/Noul with sleepintel-like bands.
Live Jev later: same decide()/record() signatures, swap backend.
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "jev" / "decisions.json"
RECEIPTS = ROOT / "data" / "decisions"
MODEL = "stub-local-v1"


def load_decisions() -> dict:
    return json.loads(DECISIONS.read_text())


def band_confidence(conf: float, thresholds: dict | None = None) -> str:
    t = thresholds or {"auto": 0.8, "confirm": 0.5}
    if conf >= t.get("auto", 0.8):
        return "auto"
    if conf >= t.get("confirm", 0.5):
        return "confirm"
    return "human"


def band_noul(answer: bool, confidence: float, thresholds: dict | None = None) -> str:
    """Noul band: strong yes/no can be auto; weak → confirm/human."""
    t = thresholds or {"auto": 0.8, "confirm": 0.5}
    if answer and confidence >= t.get("auto", 0.8):
        return "auto"
    if (not answer) and confidence <= 1 - t.get("auto", 0.8):
        return "auto"
    if confidence >= t.get("confirm", 0.5):
        return "confirm"
    return "human"


def decide(decision_id: str, store_id: str, inputs: dict[str, Any], model: str = MODEL) -> dict:
    """Local stub judge. Returns receipt-shaped dict (not yet persisted)."""
    doc = load_decisions()
    dec = next((d for d in doc["decisions"] if d["id"] == decision_id), None)
    if not dec:
        raise ValueError(f"unknown decision_id: {decision_id}")
    prim = dec["primitive"]
    conf = float(inputs.get("confidence", inputs.get("score", 0.7)))
    thr = dec.get("thresholds") or doc.get("bands")

    if prim == "noul":
        # explicit answer or derive from inputs
        if "answer" in inputs:
            answer = bool(inputs["answer"])
        elif decision_id == "brand_ready":
            packs = int(inputs.get("pack_count") or 0)
            has_json = bool(inputs.get("has_store_json"))
            has_domain = bool(inputs.get("has_domain"))
            cl_ok = bool(inputs.get("commerce_link_ok", True))
            answer = packs >= 1 and has_json and has_domain and cl_ok
            conf = 0.9 if answer else 0.4
        elif decision_id == "shopify_push_ok":
            ready = bool(inputs.get("brand_ready") or inputs.get("answer_ready"))
            packs = int(inputs.get("pack_count") or 0)
            answer = ready and packs >= 1
            conf = 0.85 if answer else 0.35
        elif decision_id == "content_tree_ok":
            answer = bool(inputs.get("has_bgraph_branches")) and bool(inputs.get("r2_prefix_set"))
            conf = 0.88 if answer else 0.4
        else:
            answer = bool(inputs.get("answer", False))
        band = band_noul(answer, conf, thr)
        action = dec.get("action_if_true") if answer else dec.get("action_if_false")
        # money/publish fail-closed
        if dec.get("fail_direction") == "fail_closed_human" or decision_id == "shopify_push_ok":
            if band != "auto" or decision_id == "shopify_push_ok":
                band = "human" if decision_id == "shopify_push_ok" else band
                action = "HOLD_human_confirm" if decision_id == "shopify_push_ok" else action
        result = {"answer": answer, "confidence": conf, "band": band, "action": action}

    elif prim == "choice":
        options = dec.get("options") or ["a", "b", "c"]
        picked = inputs.get("picked") or inputs.get("option") or options[0]
        if picked not in options:
            picked = options[0]
        band = band_confidence(conf, thr)
        result = {
            "picked": picked,
            "options": options,
            "confidence": conf,
            "band": band,
            "action": f"recommend:{picked}" if band == "auto" else f"review:{picked}",
        }
    else:
        raise ValueError(f"unsupported primitive: {prim}")

    return {
        "decision_id": decision_id,
        "store_id": store_id,
        "primitive": prim,
        "question": dec.get("question"),
        "model": model,
        "thresholds": thr,
        "fail_direction": dec.get("fail_direction"),
        "inputs": inputs,
        **result,
    }


def record(receipt: dict) -> Path:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%S")
    rid = f"actuate-{ts}-{receipt.get('store_id', 'x')}-{receipt.get('decision_id', 'd')}"
    path = RECEIPTS / f"{rid}.json"
    payload = {"id": rid, "ts": time.time(), **receipt}
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return path
