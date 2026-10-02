#!/usr/bin/env python3
"""Deterministic readiness score for each brand store (no LLM).

score = 0.4*packs_ready + 0.2*domain + 0.2*commerce_link + 0.2*branches_enabled
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "registry" / "brands"
ODDHOBBIES = Path("/root/oddhobbies/stores")


def score_store(data: dict) -> dict:
    sid = data["store_id"]
    packs_dir = ODDHOBBIES / sid / "listings"
    packs = len(list(packs_dir.glob("*.json"))) if packs_dir.exists() else 0
    packs_ready = 1.0 if packs >= 1 else 0.0
    has_store_json = (ODDHOBBIES / sid / "store.json").exists()
    domain = (data.get("identity") or {}).get("domain")
    has_domain = bool(domain)
    cl = data.get("commerce_link") or {}
    cl_ok = bool(cl.get("pack_path") and cl.get("r2_commerce_prefix"))
    branches = data.get("branches") or []
    enabled = sum(1 for b in branches if b.get("enabled", True))
    branch_score = min(enabled / 3.0, 1.0) if branches else 0.0

    score = (
        0.4 * packs_ready
        + 0.2 * (1.0 if has_domain else 0.0)
        + 0.2 * (1.0 if cl_ok else 0.0)
        + 0.2 * branch_score
    )
    return {
        "store_id": sid,
        "status": data.get("status"),
        "score": round(score, 3),
        "pack_count": packs,
        "has_store_json": has_store_json,
        "has_domain": has_domain,
        "domain": domain,
        "commerce_link_ok": cl_ok,
        "enabled_branches": enabled,
        "r2_prefix_set": bool((data.get("commerce_link") or {}).get("r2_commerce_prefix")),
        "has_bgraph_branches": bool(branches),
    }


def main() -> int:
    rows = []
    for path in sorted(BRANDS.glob("*.json")):
        data = json.loads(path.read_text())
        rows.append(score_store(data))
    rows.sort(key=lambda r: r["score"], reverse=True)
    print(f"{'store_id':<16} {'score':>6} {'packs':>5} {'branches':>8} domain")
    print("-" * 70)
    for r in rows:
        print(
            f"{r['store_id']:<16} {r['score']:>6.3f} {r['pack_count']:>5} "
            f"{r['enabled_branches']:>8} {r['domain'] or '-'}"
        )
    out = ROOT / "data" / "scores.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"scores": rows}, indent=2) + "\n")
    print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
