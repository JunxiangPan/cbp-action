# CBP v1.0.2 — Release-evidence gate

CBP v1.0.2 fixes release discipline: claims now verifies version, wheel hash, and PyPI link.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.2-py3-none-any.whl
sha256: 8a910d2e2fc01028e4d1bd7313fb7371c523816e38de60dd5bc1cfd16e207bbd
```

https://pypi.org/project/cbp-action/1.0.2/

## What changed

- claims gate enforces the release version, artifact SHA256, and PyPI link.
- coverage ratchet restored to the v1.0.0 historical floor: cbp 85.59%, security_core 87.18%.
- E2E test rejects a release body that names the wrong version.
- GitHub Checks API implementation creates per-gate check runs with annotations.

## Boundary

The `scan_engine=cel` comments experiment remains disabled after measuring
5.149s for 5,000 files against the 4.000s red line. Python remains the default.
