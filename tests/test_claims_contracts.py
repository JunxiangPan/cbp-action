"""Release-body contract: version, wheel hash, and PyPI link."""
import hashlib
from pathlib import Path
from cbp.claims_gate import _body_problem
from cbp.config import GateConfig


def _setup(tmp_path: Path, body: str):
    wheel = tmp_path / "cbp_action-1.0.2-py3-none-any.whl"
    wheel.write_bytes(b"wheel")
    (tmp_path / "body.md").write_text(body, encoding="utf-8")
    cfg = GateConfig(root=tmp_path, release_body="body.md", release_version="1.0.2",
                     release_artifact=wheel.name, pypi_project="cbp-action")
    return cfg


def test_correct_contract_passes(tmp_path: Path) -> None:
    digest = hashlib.sha256(b"wheel").hexdigest()
    body = f"v1.0.2\nQUALITY_COUNTS: 1/1\nAll 1 gates.\n{digest}\nhttps://pypi.org/project/cbp-action/1.0.2/\n"
    cfg = _setup(tmp_path, body)
    assert _body_problem(tmp_path / "body.md", "1/1", 1, cfg) == ""


def test_wrong_hash_and_link_are_rejected(tmp_path: Path) -> None:
    body = "v1.0.2\nQUALITY_COUNTS: 1/1\nAll 1 gates.\n" + "0" * 64 + "\nhttps://pypi.org/project/cbp-action/9.9.9/\n"
    cfg = _setup(tmp_path, body)
    problem = _body_problem(tmp_path / "body.md", "1/1", 1, cfg)
    assert "SHA256" in problem
