from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_validate() -> None:
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK:" in r.stdout


def run_export() -> None:
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "export_graph.py")], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    exports = list((ROOT / "exports").glob("*.json"))
    assert len(exports) >= 3, exports


def test_validate_and_export() -> None:
    run_validate()
    run_export()
    for sid in ("oddhobb", "grimoirer", "stonedoorway"):
        path = ROOT / "exports" / f"{sid}.json"
        assert path.exists(), path
        data = json.loads(path.read_text())
        assert data["store_id"] == sid
        assert data["counts"]["nodes"] > 0


def test_oddhobb_branches_enabled() -> None:
    data = json.loads((ROOT / "registry" / "brands" / "oddhobb.json").read_text())
    enabled = [b["branch_id"] for b in data["branches"] if b.get("enabled")]
    assert "youtube" in enabled and "instagram" in enabled
    assert data["identity"]["domain"] == "oddhobb.com"
    assert data["identity"]["email"] == "hello@oddhobb.com"


def test_grimoirer_handle() -> None:
    data = json.loads((ROOT / "registry" / "brands" / "grimoirer.json").read_text())
    yt = next(b for b in data["branches"] if b["branch_id"] == "youtube")
    assert yt["account"]["handle"] == "@thegrimoirer"


def test_stonedoorway_scaffold() -> None:
    data = json.loads((ROOT / "registry" / "brands" / "stonedoorway.json").read_text())
    assert data["status"] == "scaffold"
    assert all(not b.get("enabled", True) for b in data["branches"])


def test_publish_gates_human() -> None:
    for path in (ROOT / "registry" / "brands").glob("*.json"):
        data = json.loads(path.read_text())
        for b in data["branches"]:
            for m in b.get("posting_methods") or []:
                if str(m.get("method_id", "")).startswith(("yt.", "ig.", "tt.", "pin.", "x.")):
                    assert m["gate"] == "human_confirm", (path.name, m)
