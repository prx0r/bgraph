from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
    )


def test_score_runs() -> None:
    r = run("score.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "oddhobb" in r.stdout
    scores = json.loads((ROOT / "data" / "scores.json").read_text())
    assert len(scores["scores"]) >= 3
    # oddhobb has packs → should rank high
    top = scores["scores"][0]["store_id"]
    assert top == "oddhobb"


def test_actuate_dry_run_writes_receipts() -> None:
    r = run("actuate.py", "--dry-run")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "dry-run" in r.stdout.lower() or "P0" in r.stdout
    receipts = list((ROOT / "data" / "decisions").glob("actuate-*.json"))
    assert len(receipts) >= 8  # 3 stores * 4 decisions minimum-ish
    latest = json.loads((ROOT / "data" / "actuate_latest.json").read_text())
    assert latest["mode"] == "dry-run"
    # shopify push must be human/hold in P0
    holds = latest.get("human_actions") or []
    assert any("shopify" in str(x.get("decision_id")) for x in holds) or len(holds) >= 1


def test_actuate_requires_dry_run() -> None:
    r = run("actuate.py")
    assert r.returncode == 2


def test_jev_stub_noul() -> None:
    sys.path.insert(0, str(SCRIPTS))
    import jev
    rec = jev.decide(
        "brand_ready",
        "oddhobb",
        {"pack_count": 15, "has_store_json": True, "has_domain": True, "commerce_link_ok": True},
    )
    assert rec["answer"] is True
    assert rec["band"] in {"auto", "confirm", "human"}
    rec2 = jev.decide(
        "shopify_push_ok",
        "oddhobb",
        {"brand_ready": True, "pack_count": 15},
    )
    assert rec2["band"] == "human"  # P0 fail-closed human


def test_docs_and_registry_exist() -> None:
    for rel in [
        "docs/COORDINATION.md",
        "jev/decisions.json",
        "registry/engines.yaml",
        "registry/content/README.md",
        "scripts/score.py",
        "scripts/actuate.py",
        "scripts/jev.py",
    ]:
        assert (ROOT / rel).exists(), rel
