"""Release asset inventory checks: exact names and SHA256 digests."""
from __future__ import annotations

import hashlib
from pathlib import Path

import certifi
import requests


def asset_digests(repository: str, tag: str, token: str | None = None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    response = requests.get(
        f"https://api.github.com/repos/{repository}/releases/tags/{tag}",
        headers=headers, timeout=30, verify=certifi.where(),
    )
    response.raise_for_status()
    return {
        item["name"]: str(item.get("digest", "")).removeprefix("sha256:")
        for item in response.json().get("assets", [])
    }


def expected_digests(asset_dir: Path) -> dict[str, str]:
    result = {}
    for path in sorted(asset_dir.iterdir()):
        if path.is_file() and path.suffix in {".whl", ".gz", ".json", ".md"}:
            result[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def verify_assets(asset_dir: Path, repository: str, tag: str, token: str | None = None) -> tuple[bool, str]:
    """Reject extra assets or assets whose SHA256 differs from the local set."""
    expected = expected_digests(asset_dir)
    remote = asset_digests(repository, tag, token)
    extra = sorted(set(remote) - set(expected))
    missing = sorted(set(expected) - set(remote))
    wrong = sorted(
        name for name in set(expected) & set(remote)
        if remote[name].lower() != expected[name].lower()
    )
    if extra or missing or wrong:
        return False, f"ERRATA assets extra={extra} missing={missing} wrong={wrong}"
    return True, f"RELEASE_ASSETS_OK count={len(expected)}"


def verify_from_manifest(manifest: Path, repository: str, tag: str, token: str | None = None) -> tuple[bool, str]:
    """Verify release assets against a local ``hash filename`` manifest."""
    expected: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            expected[parts[1].strip().lstrip("*")] = parts[0].strip()
    remote = asset_digests(repository, tag, token)
    extra = sorted(set(remote) - set(expected))
    missing = sorted(set(expected) - set(remote))
    wrong = sorted(
        name for name in set(expected) & set(remote)
        if remote[name].lower() != expected[name].lower()
    )
    if extra or missing or wrong:
        return False, f"ERRATA assets extra={extra} missing={missing} wrong={wrong}"
    return True, f"RELEASE_ASSETS_OK count={len(expected)}"
