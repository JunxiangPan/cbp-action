"""Release asset inventory checks: exact names and SHA256 digests."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen


def _api_headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "cbp-verify-assets"}
    if token:
        headers["Authorization"] = "Bearer " + token
    return headers


def asset_digests(repository: str, tag: str, token: str | None = None) -> dict[str, str]:
    """Fetch release asset digests using only the Python standard library."""
    request = Request(
        f"https://api.github.com/repos/{repository}/releases/tags/{tag}",
        headers=_api_headers(token),
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return {
        item["name"]: str(item.get("digest", "")).removeprefix("sha256:")
        for item in payload.get("assets", [])
    }


def expected_digests(asset_dir: Path) -> dict[str, str]:
    result = {}
    for path in sorted(asset_dir.iterdir()):
        if path.is_file() and path.suffix in {".whl", ".gz", ".json", ".md"}:
            result[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _compare(expected: dict[str, str], remote: dict[str, str]) -> tuple[bool, str]:
    extra = sorted(set(remote) - set(expected))
    missing = sorted(set(expected) - set(remote))
    wrong = sorted(
        name for name in set(expected) & set(remote)
        if remote[name].lower() != expected[name].lower()
    )
    if extra or missing or wrong:
        return False, f"ERRATA assets extra={extra} missing={missing} wrong={wrong}"
    return True, f"RELEASE_ASSETS_OK count={len(expected)}"


def verify_assets(asset_dir: Path, repository: str, tag: str, token: str | None = None) -> tuple[bool, str]:
    """Reject extra assets or assets whose SHA256 differs from the local set."""
    return _compare(expected_digests(asset_dir), asset_digests(repository, tag, token))


def verify_from_manifest(manifest: Path, repository: str, tag: str, token: str | None = None) -> tuple[bool, str]:
    """Verify release assets against a local ``hash filename`` manifest.

    The manifest itself is allowed in the release asset list but is not
    self-hashed; every other asset must appear exactly once with a matching
    SHA256. Missing, extra, and wrong-hash assets all fail closed.
    """
    expected: dict[str, str] = {manifest.name: ""}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            expected[parts[1].strip().lstrip("*")] = parts[0].strip()
    remote = asset_digests(repository, tag, token)
    extra = sorted(set(remote) - set(expected))
    missing = sorted(set(expected) - set(remote))
    wrong = sorted(
        name for name in set(expected) & set(remote)
        if name != manifest.name and remote[name].lower() != expected[name].lower()
    )
    if extra or missing or wrong:
        return False, f"ERRATA assets extra={extra} missing={missing} wrong={wrong}"
    return True, f"RELEASE_ASSETS_OK count={len(expected)}"
