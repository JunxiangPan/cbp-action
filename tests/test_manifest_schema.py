"""The public schema must accept a real CONTRACT v1.7 manifest."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "manifest.schema.json").read_text(encoding="utf-8"))
REAL = ROOT / "docs" / "1.2.0" / "evidence" / "cbc-quality-manifest.json"


def test_schema_accepts_real_v17_manifest() -> None:
    jsonschema.validate(json.loads(REAL.read_text(encoding="utf-8")), SCHEMA)


def test_schema_rejects_the_old_counts_shape() -> None:
    try:
        jsonschema.validate({"counts": {"passed": 1, "total": 1}}, SCHEMA)
    except jsonschema.ValidationError:
        return
    raise AssertionError("old counts-only manifest must not validate")
