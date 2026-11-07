"""Coverage for gate configuration dispatch branches."""
from pathlib import Path
from cbp.cli import _configured
from cbp.config import GateConfig


def test_all_configuration_branches(tmp_path: Path) -> None:
    cfg = GateConfig(root=tmp_path)
    assert _configured("encoding", cfg) is True
    assert _configured("coverage", cfg) is False
    assert _configured("dependency", cfg) is False
    assert _configured("comments", cfg) is False
    assert _configured("docs", cfg) is False
    assert _configured("claims", cfg) is False
    assert _configured("custom", cfg) is False
    assert _configured("upgrade", cfg) is False
    assert _configured("binary", cfg) is False
    assert _configured("unknown", cfg) is True
    assert _configured("custom", GateConfig(root=tmp_path, packs=({"path": "x"},))) is True


def test_changed_files_reads_git_diff(tmp_path: Path) -> None:
    import subprocess
    from cbp.cli import _changed_files
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=tmp_path, check=True)
    (tmp_path / "a.txt").write_text("a", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "init"], cwd=tmp_path, check=True)
    (tmp_path / "a.txt").write_text("b", encoding="utf-8")
    assert "a.txt" in _changed_files(tmp_path, "HEAD")
