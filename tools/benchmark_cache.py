#!/usr/bin/env python3
"""Measure cold and cached custom-gate runs for a file count."""
from __future__ import annotations

import argparse
import json
import tempfile
import time
from pathlib import Path

from cbp import custom_rules
from cbp.config import GateConfig


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=5000)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="cbp-cache-bench-") as temp:
        root = Path(temp)
        for index in range(args.count):
            (root / f"f{index}.py").write_text("print('ok')\n", encoding="utf-8")
        cfg = GateConfig(root=root, cache_file=".cbp-cache.json", custom_rules=({
            "name": "bench", "pattern": "print", "files": ["*.py"],
            "message": "hit", "mode": "warn", "max_matches": 1,
        },))
        first = time.perf_counter()
        custom_rules.run(cfg)
        cold = time.perf_counter() - first
        second = time.perf_counter()
        custom_rules.run(cfg)
        warm = time.perf_counter() - second
    print(json.dumps({"count": args.count, "cold_seconds": cold, "cached_seconds": warm}, indent=2))
    return 0 if warm < 1.0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
