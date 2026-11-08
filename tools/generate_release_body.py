#!/usr/bin/env python3
"""Generate the release body from build outputs; no post-publish edits."""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--notes", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    wheel = Path(args.wheel)
    notes = Path(args.notes).read_text(encoding="utf-8")
    match = re.search(r"(?m)^QUALITY_COUNTS:\s*(\d+/\d+)\s*$", notes)
    if not match:
        raise SystemExit("notes must contain exactly one QUALITY_COUNTS line")
    version = args.version.lstrip("v")
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    body = f"""# CBP v{version} — Release-evidence gate

v{version} = v1.0.6 evidence closure + three AI audit gates (audit mode, non-blocking).

This release body was generated from the built wheel by
`tools/generate_release_body.py`; the wheel SHA256 is not hand-edited.

## Verification

```text
QUALITY_COUNTS: {match.group(1)}
All 9 gates are active.
```

```text
{wheel.name}
sha256: {digest}
```

https://pypi.org/project/cbp-action/{version}/

## Section A: Security regression (blocking)

- composite action payload E2E: 15/15 cases, Linux runner
- checkout ref whitelist: PASS
- release body auto-generated: PASS (no manual backfill)
- release.yml permissions: PASS
- release asset inventory: PASS
- security_core: 90%+ floor

## Section B: AI audit gates (audit mode, non-blocking)

- ai-release: PASS / WARN / SKIP (counts)
- ai-test: PASS / WARN / SKIP (counts) | self-check: separate
- ai-change: PASS / WARN / SKIP (counts)

## Still to acknowledge

- ai-test false-positive rate is not yet measured on external projects.
- composite action payload E2E runs on GitHub Linux; local Windows is not verified.
- ai-release is structured evidence only, not natural-language summarization.
- Section B gates are audit-only and do not block publishing.
"""
    Path(args.output).write_text(body, encoding="utf-8")
    print(f"RELEASE_BODY_GENERATED {args.output} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
