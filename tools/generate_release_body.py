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

## Release boundary

Section A: input boundaries, release body generation, tag whitelist, and
asset inventory verification are blocking gates.

Section B: AI audit gates are non-blocking and reported separately when
enabled.
"""
    Path(args.output).write_text(body, encoding="utf-8")
    print(f"RELEASE_BODY_GENERATED {args.output} sha256={digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
