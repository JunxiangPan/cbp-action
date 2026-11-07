"""Small edge branches in the core gates."""
import json
from pathlib import Path
from cbp import coverage_gate, dependency_gate, docs_gate, comment_gate
from cbp.config import GateConfig


def test_coverage_ratchet_unreadable(tmp_path: Path) -> None:
    (tmp_path / "c.json").write_text(json.dumps({"files": {}}), encoding="utf-8")
    (tmp_path / "a.json").write_text('{"files": {}}', encoding="utf-8")
    (tmp_path / "r.json").write_text("not json", encoding="utf-8")
    cfg = GateConfig(root=tmp_path, coverage_json="c.json", coverage_allowlist="a.json", coverage_ratchet="r.json")
    passed, detail = coverage_gate.run(cfg)
    assert passed is False and "ratchet" in detail


def test_coverage_invalid_mode(tmp_path: Path) -> None:
    (tmp_path / "c.json").write_text(json.dumps({"files": {}}), encoding="utf-8")
    (tmp_path / "a.json").write_text('{"files": {}}', encoding="utf-8")
    cfg = GateConfig(root=tmp_path, coverage_json="c.json", coverage_allowlist="a.json",
                     coverage_groups=({"name": "x", "files": ["x.py"], "mode": "bad"},))
    passed, detail = coverage_gate.run(cfg)
    assert passed is False and "invalid mode" in detail


def test_dependency_missing_lock(tmp_path: Path) -> None:
    cfg = GateConfig(root=tmp_path, dependency_lock="missing.lock", install_command="i.sh")
    assert dependency_gate.run(cfg)[0] is False


def test_docs_missing_manifest(tmp_path: Path) -> None:
    cfg = GateConfig(root=tmp_path, docs_manifest="missing.json")
    assert docs_gate.run(cfg)[0] is False


def test_comment_suppression_out_of_range() -> None:
    assert comment_gate._suppressed([], 4, "CBP-CMT-001") is False


def test_comment_suppression_marker(tmp_path: Path) -> None:
    lines = ["# cbp: ignore=CBP-CMT-001"]
    assert comment_gate._suppressed(lines, 1, "CBP-CMT-001") is True


def test_dependency_invalid_lock(tmp_path: Path) -> None:
    (tmp_path / "bad.lock").write_text("unpinned", encoding="utf-8")
    cfg = GateConfig(root=tmp_path, dependency_lock="bad.lock", install_command="i.sh")
    assert dependency_gate.run(cfg)[0] is False


def test_docs_hash_mismatch(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "a.md").write_text("x", encoding="utf-8")
    (tmp_path / "manifest.json").write_text(json.dumps({"files": [{"path": "docs/a.md", "sha256": "0" * 64}]}), encoding="utf-8")
    cfg = GateConfig(root=tmp_path, docs_manifest="manifest.json")
    assert docs_gate.run(cfg)[0] is False
