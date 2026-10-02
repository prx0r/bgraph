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


def test_validate_green() -> None:
    r = run("validate.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "OK:" in r.stdout


def test_export_all() -> None:
    r = run("export_graph.py")
    assert r.returncode == 0, r.stdout + r.stderr
    for sid in ("oddhobb", "grimoirer", "stonedoorway"):
        path = ROOT / "exports" / f"{sid}.json"
        assert path.exists(), path
        data = json.loads(path.read_text())
        assert data["store_id"] == sid
        assert data["counts"]["nodes"] > 0
        # every branch node present for enabled brands
        if data["store_id"] == "oddhobb":
            ids = {n["id"] for n in data["nodes"]}
            assert "oddhobb/youtube" in ids
            assert "identity:oddhobb" in ids


def test_brand_status_runs() -> None:
    r = run("brand_status.py")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "oddhobb" in r.stdout and "grimoirer" in r.stdout


def test_r2_layout_runs() -> None:
    r = run("r2_layout.py", "--store", "oddhobb")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "content/stores/oddhobb" in r.stdout


def test_instantiate_creates_valid_brand() -> None:
    sid = "zztestbrand"
    path = ROOT / "registry" / "brands" / f"{sid}.json"
    if path.exists():
        path.unlink()
    r = run(
        "instantiate_brand.py",
        "--store-id", sid,
        "--name", "ZZ Test",
        "--domain", "zztestbrand.com",
        "--email", "hello@zztestbrand.com",
        "--handle", "@zztestbrand",
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert path.exists()
    data = json.loads(path.read_text())
    assert data["store_id"] == sid
    assert data["identity"]["domain"] == "zztestbrand.com"
    # validate still passes with extra brand
    r2 = run("validate.py")
    assert r2.returncode == 0, r2.stdout + r2.stderr
    # cleanup
    path.unlink()
    exp = ROOT / "exports" / f"{sid}.json"
    if exp.exists():
        exp.unlink()
    r3 = run("validate.py")
    assert r3.returncode == 0


def test_oddhobb_site_block() -> None:
    data = json.loads((ROOT / "registry" / "brands" / "oddhobb.json").read_text())
    site = data.get("site") or {}
    assert site.get("primary_host") == "oddhobb.com"
    assert data["commerce_link"]["pack_path"] == "oddhobbies/stores/oddhobb"


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
                mid = str(m.get("method_id", ""))
                if mid.startswith(("yt.", "ig.", "tt.", "pin.", "x.")):
                    assert m["gate"] == "human_confirm", (path.name, mid)


def test_docs_exist() -> None:
    for rel in [
        "AGENTS.md",
        "README.md",
        "RESOURCES.md",
        "TODO.md",
        "docs/architecture/ARCHITECTURE.md",
        "docs/architecture/R2-CONTENT.md",
        "docs/architecture/PUBLISH-METHODS.md",
        "docs/integrations/INTEGRATIONS.md",
        "docs/integrations/SITE.md",
        "docs/integrations/COMMERCE.md",
        "docs/operations/BRAND-ADD.md",
        "docs/operations/DAILY-LOOP.md",
        "templates/brand.template.json",
        "schemas/brand-organiser.v1.schema.json",
    ]:
        assert (ROOT / rel).exists(), rel
