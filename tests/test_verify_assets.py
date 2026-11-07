"""Asset inventory and release verification helpers."""
from __future__ import annotations

import hashlib
from pathlib import Path
import pytest
from cbp import verify_release as vr
from cbp import verify_release_assets as va


def test_expected_assets_exact(tmp_path: Path) -> None:
    (tmp_path / "a.whl").write_bytes(b"a")
    (tmp_path / "b.tar.gz").write_bytes(b"b")
    (tmp_path / "ignore.txt").write_bytes(b"x")
    expected = va.expected_digests(tmp_path)
    assert expected == {"a.whl": hashlib.sha256(b"a").hexdigest(), "b.tar.gz": hashlib.sha256(b"b").hexdigest()}


def test_verify_assets_detects_wrong_extra_missing(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "a.whl").write_bytes(b"a")
    monkeypatch.setattr(va, "asset_digests", lambda *a, **k: {"a.whl": "0" * 64, "extra.whl": "1" * 64})
    passed, detail = va.verify_assets(tmp_path, "o/r", "v1")
    assert passed is False
    assert "extra" in detail and "wrong" in detail
    monkeypatch.setattr(va, "asset_digests", lambda *a, **k: {})
    assert va.verify_assets(tmp_path, "o/r", "v1")[0] is False


def test_verify_body_helpers(tmp_path: Path, monkeypatch) -> None:
    assert vr._sha("a\r\nb") == vr._sha("a\nb")
    monkeypatch.setenv("GH_TOKEN", "t")
    assert vr.token_from_env() == "t"
    assert vr.verify("o/r", "v1", tmp_path / "missing.md")[0] is False
    body = tmp_path / "body.md"
    body.write_text("x", encoding="utf-8")
    monkeypatch.setattr(vr, "fetch_release_body", lambda *a, **k: "y")
    assert vr.verify("o/r", "v1", body)[0] is False
    monkeypatch.setattr(vr, "fetch_release_body", lambda *a, **k: "x")
    assert vr.verify("o/r", "v1", body)[0] is True


def test_fetch_release_body_error(monkeypatch) -> None:
    class Bad:
        status_code = 500
    monkeypatch.setattr("requests.get", lambda *a, **k: Bad())
    with pytest.raises(RuntimeError):
        vr.fetch_release_body("o/r", "v1")


def test_fetch_and_asset_digests_success(monkeypatch) -> None:
    class Good:
        status_code = 200
        def raise_for_status(self):
            return None
        def json(self):
            return {"body": "hello", "assets": [{"name": "a.whl", "digest": "sha256:abc"}]}
    monkeypatch.setattr("requests.get", lambda *a, **k: Good())
    assert vr.fetch_release_body("o/r", "v1") == "hello"
    class Response:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return False
        def read(self):
            return b'{"assets":[{"name":"a.whl","digest":"sha256:abc"}]}'
    monkeypatch.setattr(va, "urlopen", lambda *a, **k: Response())
    assert va.asset_digests("o/r", "v1") == {"a.whl": "abc"}


def test_verify_assets_success(tmp_path: Path, monkeypatch) -> None:
    (tmp_path / "a.whl").write_bytes(b"a")
    digest = hashlib.sha256(b"a").hexdigest()
    monkeypatch.setattr(va, "asset_digests", lambda *a, **k: {"a.whl": digest})
    assert va.verify_assets(tmp_path, "o/r", "v1")[0] is True


def test_verify_from_manifest(tmp_path: Path, monkeypatch) -> None:
    manifest = tmp_path / "RELEASE_ASSETS.sha256"
    manifest.write_text("abc *a.whl\n", encoding="utf-8")
    monkeypatch.setattr(va, "asset_digests", lambda *a, **k: {"a.whl": "abc", "RELEASE_ASSETS.sha256": "self"})
    assert va.verify_from_manifest(manifest, "o/r", "v1")[0] is True
    monkeypatch.setattr(va, "asset_digests", lambda *a, **k: {"a.whl": "abc", "RELEASE_ASSETS.sha256": "self", "extra.md": "x"})
    assert va.verify_from_manifest(manifest, "o/r", "v1")[0] is False
