"""The local-build dogfood branch must have a valid WHEEL_SHA256."""
from __future__ import annotations

import hashlib
from pathlib import Path


def test_local_wheel_manifest_matches_bytes() -> None:
    manifest = Path("dist/WHEEL_SHA256")
    assert manifest.is_file(), "dist/WHEEL_SHA256 missing"
    for line in manifest.read_text(encoding="utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        digest, name = parts[0], parts[1].strip().lstrip("*")
        path = Path("dist") / name
        assert path.is_file(), f"listed asset missing: {name}"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == digest.lower()
