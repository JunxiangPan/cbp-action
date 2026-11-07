#!/usr/bin/env python3
"""Benchmark the AST/taint layer on a synthetic tree."""
from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

from cbp import ast_engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5000)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="cbp-ast-bench-") as temp:
        root = Path(temp)
        for index in range(args.count):
            (root / f"f{index}.py").write_text("x = 1", encoding="utf-8")
        started = time.perf_counter()
        findings = ast_engine.scan_root(root)
        elapsed = time.perf_counter() - started
    print(json.dumps({"count": args.count, "seconds": elapsed, "findings": len(findings)}, indent=2))
    return 0 if elapsed <= 15.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
