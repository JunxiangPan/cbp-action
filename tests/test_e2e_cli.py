"""End-to-end CLI wiring tests: no library-only functions allowed."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _run(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run([sys.executable, "-m", "cbp.cli", *args], cwd=cwd, capture_output=True, text=True, env=env)


def test_policy_test_is_reachable_from_cli(tmp_path: Path) -> None:
    fixture = tmp_path / "fixture.json"
    fixture.write_text(json.dumps({"cases": [{
        "name": "hit", "cel": 'files.exists(t, t.matches(".*secret.*"))',
        "files": {"a": "secret"}, "expect": True,
    }]}), encoding="utf-8")
    result = _run(["policy", "test", str(fixture)], tmp_path)
    assert result.returncode == 0, result.stderr
    assert "POLICY_TEST=PASS" in result.stdout


def test_packs_only_repository_triggers_custom_gate(tmp_path: Path) -> None:
    import hashlib
    pack = tmp_path / "pack.json"
    pack.write_text(json.dumps({
        "name": "baseline", "version": "1.0.0",
        "rules": [{"name": "pack-rule", "pattern": "print", "files": ["*.py"],
                   "message": "pack hit", "mode": "enforce", "max_matches": 1}],
    }), encoding="utf-8")
    digest = hashlib.sha256(pack.read_bytes()).hexdigest()
    (tmp_path / "a.py").write_text("print('x')\n", encoding="utf-8")
    (tmp_path / "cbp.json").write_text(json.dumps({
        "schema_version": "1.0.0", "enable_claims": False,
        "packs": [{"path": "pack.json", "sha256": digest}],
    }), encoding="utf-8")
    result = _run(["--root", str(tmp_path)], tmp_path)
    assert result.returncode == 1
    assert "custom: FAIL" in result.stdout
    assert "pack hit" in result.stdout
