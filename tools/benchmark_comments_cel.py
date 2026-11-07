#!/usr/bin/env python3
"""Measure the experimental CEL comment detector over N files."""
from __future__ import annotations

import argparse
import tempfile
import time
from pathlib import Path

from cbp import comments_cel


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5000)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="cbp-cel-comments-") as temp:
        root = Path(temp)
        paths = []
        for index in range(args.count):
            path = root / f"f{index}.py"
            path.write_text("print('ok')\n", encoding="utf-8")
            paths.append(path)
        started = time.perf_counter()
        for path in paths:
            comments_cel.matches(path.read_text(encoding="utf-8"))
        elapsed = time.perf_counter() - started
    print(f"count={args.count} seconds={elapsed:.3f} limit=4.000")
    return 0 if elapsed <= 4.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
