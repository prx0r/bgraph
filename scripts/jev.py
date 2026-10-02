#!/usr/bin/env python3
"""Jev client — live OpenRouter alpha decisions OR local stub.

Key: OPENROUTER_API_KEY in env or bgraph/.env (never git, never print).
Model pinned: typesafe/jev-1.13 (thresholds couple to versions).
Jev key is for THIS client only — not pi, not commerce.

Policy: auto / confirm / human from decisions.json.
Noul: yes/no cutoffs. Choice: needs 'other'. Fail direction per decision_id.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DECISIONS = ROOT / "jev" / "decisions.json"
RECEIPTS = ROOT / "data" / "decisions"
MODEL = "typesafe/jev-1.13"
ENDPOINT = "https://openrouter.ai/api/alpha/decisions"
STUB_MODEL = "stub-local-v1"


def _load_env() -> None:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def _key() -> str:
    _load_env()
    env = os.environ.get("OPENROUTER_API_KEY", "").strip("'\"")
    if env:
        return env
    raise RuntimeError("OPENROUTER_API_KEY not found (env or bgraph/.env)")


def live_enabled() -> bool:
    _load_env()
    return os.environ.get("JEV_LIVE", "0").strip() == "1" and bool(
        os.environ.get("OPENROUTER_API_KEY")
    )


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
    t = thresholds or {"auto": 0.8, "confirm": 0.5}
    if answer and confidence >= t.get("auto", 0.8):
        return "auto"
    if (not answer) and confidence <= 1 - t.get("auto", 0.8):
        return "auto"
    if confidence >= t.get("confirm", 0.5):
        return "confirm"
    return "human"


def _stub_noul(decision_id: str, inputs: dict) -> tuple[bool, float]:
    if "answer" in inputs:
        return bool(inputs["answer"]), float(inputs.get("confidence", 0.7))
    if decision_id == "brand_ready":
        packs = int(inputs.get("pack_count") or 0)
        ok = packs >= 1 and bool(inputs.get("has_store_json")) and bool(
            inputs.get("has_domain")
        ) and bool(inputs.get("commerce_link_ok", True))
        return ok, (0.9 if ok else 0.4)
    if decision_id == "shopify_push_ok":
        ready = bool(inputs.get("brand_ready") or inputs.get("answer_ready"))
        ok = ready and int(inputs.get("pack_count") or 0) >= 1
        return ok, (0.85 if ok else 0.35)
    if decision_id == "content_tree_ok":
        ok = bool(inputs.get("has_bgraph_branches")) and bool(inputs.get("r2_prefix_set"))
        return ok, (0.88 if ok else 0.4)
    return bool(inputs.get("answer", False)), float(inputs.get("confidence", 0.7))


def _live_noul(decision: dict, store_id: str, inputs: dict) -> dict:
    """Call OpenRouter alpha/decisions — sleepintel question shape."""
    state = {
        "store_id": store_id,
        "decision_id": decision["id"],
        "inputs": inputs,
        "fail_direction": decision.get("fail_direction"),
    }
    # questions as record: id -> {type, instructions, criteria}
    questions = {
        decision["id"]: {
            "type": "noul",
            "instructions": decision.get("question") or decision["id"],
            "criteria": {
                "true": decision.get("action_if_true") or "yes / ready",
                "false": decision.get("action_if_false") or "no / not ready",
            },
        }
    }
    body = json.dumps({"model": MODEL, "state": state, "questions": questions}).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Authorization": f"Bearer {_key()}",
            "Content-Type": "application/json",
        },
    )
    delay = 1.0
    out = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                out = json.load(r)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 529) and attempt < 2:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    else:
        raise RuntimeError("jev unreachable after retries")

    # Parse sleepintel shape: out["answers"][qid]["noul"] + confidence
    answers = out.get("answers") or {}
    ans = answers.get(decision["id"]) or {}
    if "noul" in ans:
        answer = ans["noul"]
    elif "answer" in ans:
        answer = ans["answer"]
    else:
        answer = False
    conf = float(ans.get("confidence") or ans.get("p") or 0.7)
    if isinstance(answer, str):
        answer = answer.strip().lower() in ("true", "yes", "1", "y")
    return {
        "answer": bool(answer),
        "confidence": conf,
        "raw_model": out.get("_pinned_model") or out.get("model", MODEL),
        "usage": out.get("usage"),
    }


def decide(decision_id: str, store_id: str, inputs: dict[str, Any], model: str | None = None) -> dict:
    doc = load_decisions()
    dec = next((d for d in doc["decisions"] if d["id"] == decision_id), None)
    if not dec:
        raise ValueError(f"unknown decision_id: {decision_id}")
    prim = dec["primitive"]
    thr = dec.get("thresholds") or doc.get("bands")
    use_live = live_enabled() and prim == "noul"
    mdl = MODEL if use_live else (model or STUB_MODEL)

    if prim == "noul":
        if use_live:
            try:
                live = _live_noul(dec, store_id, inputs)
                answer = live["answer"]
                conf = live["confidence"]
                mdl = live.get("raw_model") or MODEL
            except Exception as e:  # fail-closed toward human for push
                answer = False
                conf = 0.15
                mdl = f"{STUB_MODEL}+live_error:{type(e).__name__}"
        else:
            answer, conf = _stub_noul(decision_id, inputs)
        band = band_noul(answer, conf, thr)
        action = dec.get("action_if_true") if answer else dec.get("action_if_false")
        if decision_id == "shopify_push_ok":
            band = "human"
            action = "HOLD_human_confirm"
        result = {"answer": answer, "confidence": conf, "band": band, "action": action}

    elif prim == "choice":
        options = dec.get("options") or ["a", "b", "c"]
        picked = inputs.get("picked") or inputs.get("option") or options[0]
        if picked not in options:
            picked = options[0]
        conf = float(inputs.get("confidence", inputs.get("score", 0.7)))
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
        "model": mdl,
        "live": use_live,
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
