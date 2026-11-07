# CBP v1.0.3 — Release-evidence gate

CBP v1.0.3 closes the release-discipline gaps found by external review.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.3-py3-none-any.whl
sha256: d0a6537e53c1f6b5b1087736bdbbc4cac0fe108903f5da034030bd181dac5dae
```

https://pypi.org/project/cbp-action/1.0.3/

## What changed

- `action.yml` verifies `dist/WHEEL_SHA256` before installing the wheel.
- Release assets are built automatically; `RELEASE_NOTES.generated.md` is part of `gh release create`.
- `--verify-release` checks the release asset inventory and rejects extra, missing, or wrong-hash assets.
- `security_core` coverage floor is 90.0, with 90.02 measured.
- README version sequence and PyPI instructions corrected.
- CHANGELOG covers 1.0.0 through 1.0.3.
- VM chaos evidence is explicitly a v1.1.0 roadmap item.
