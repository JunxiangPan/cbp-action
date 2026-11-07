"""Bind coverage evidence to the exact measured source bytes."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Iterable


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def measured_files(root: Path, data: dict) -> list[Path]:
    files = data.get("files", {})
    result = []
    for raw in sorted(files):
        path = root / str(raw).replace("\\", "/")
        if path.suffix == ".py" and path.is_file():
            result.append(path)
    return result


def compute(root: Path, files: Iterable[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda item: _relative(root, item)):
        digest.update(_relative(root, path).encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest()


def environment_fingerprint(root: Path) -> str:
    """Fingerprint the interpreter, OS, and commit used to measure coverage."""
    try:
        commit = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=10, check=False).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        commit = ""
    payload = {
        "python": sys.version,
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "os": os.name,
        "commit": commit,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def stamp(coverage_path: Path, root: Path) -> str:
    data = json.loads(coverage_path.read_text(encoding="utf-8"))
    value = compute(root, measured_files(root, data))
    data["source_files_hash"] = value
    data["environment_fingerprint"] = environment_fingerprint(root)
    coverage_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    return value
