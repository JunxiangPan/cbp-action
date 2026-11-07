#!/usr/bin/env python3
"""Verify a CBP release: body, wheel hash, manifest hash, and OIDC attestation."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path

import certifi
import requests


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--asset-dir", required=True)
    parser.add_argument("--body", default="docs/RELEASE_BODY.md")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    args = parser.parse_args()
    headers = {"Accept": "application/vnd.github+json", "Authorization": "Bearer " + args.token}
    response = requests.get(
        f"https://api.github.com/repos/{args.repo}/releases/tags/{args.tag}",
        headers=headers,
        timeout=30,
        verify=certifi.where(),
    )
    response.raise_for_status()
    release = response.json()
    body = Path(args.body).read_text(encoding="utf-8")
    if body.replace("\r\n", "\n") != release["body"].replace("\r\n", "\n"):
        print("VERIFY_ALL=FAIL release body mismatch")
        return 1
    assets = {item["name"]: item for item in release.get("assets", [])}
    wheel_name = next((name for name in assets if name.endswith(".whl")), "")
    if not wheel_name:
        print("VERIFY_ALL=FAIL wheel asset missing")
        return 1
    asset_dir = Path(args.asset_dir)
    wheel = asset_dir / wheel_name
    manifest = asset_dir / "quality-manifest.json"
    manifest_seal = asset_dir / "quality-manifest.json.sha256"
    if not wheel.is_file() or not manifest.is_file() or not manifest_seal.is_file():
        print("VERIFY_ALL=FAIL local assets missing")
        return 1
    wheel_sha = sha256(wheel)
    if wheel_sha != str(assets[wheel_name].get("digest", "")).removeprefix("sha256:"):
        print("VERIFY_ALL=FAIL wheel hash mismatch")
        return 1
    manifest_sha = sha256(manifest)
    if manifest_sha != manifest_seal.read_text(encoding="utf-8").split()[0]:
        print("VERIFY_ALL=FAIL manifest hash mismatch")
        return 1
    attestation = requests.get(
        f"https://api.github.com/repos/{args.repo}/attestations/sha256:{wheel_sha}",
        headers=headers,
        timeout=30,
        verify=certifi.where(),
    )
    if attestation.status_code != 200:
        print(f"VERIFY_ALL=FAIL attestation HTTP {attestation.status_code}")
        return 1
    print(f"VERIFY_ALL=VALID wheel={wheel_sha} manifest={manifest_sha} attestations=200 body=OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
