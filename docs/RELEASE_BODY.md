# CBP v1.0.4 — Release-evidence gate

CBP v1.0.4 makes asset verification a mandatory release step.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.4-py3-none-any.whl
sha256: 5bf44c8f18145c614f7920b8de694844d59fe5ffc68646b28d0bba85117cd0ac
```

https://pypi.org/project/cbp-action/1.0.4/

## What changed

- Release workflow generates `RELEASE_ASSETS.sha256`, uploads it, and verifies body plus assets after publishing.
- `--verify-release` fails closed (exit 2) when the asset manifest is missing.
- `verify_release_assets` uses only the Python standard library; no requests/certifi runtime dependency.
- Weekly scheduled re-verification checks the latest release.
- E2E tests cover missing manifest, extra asset, and wrong hash.
- `security_core` remains enforced at 90.0.

## Erratum for v1.0.3

v1.0.3's asset verification was only activated when a local
`dist/RELEASE_ASSETS.sha256` existed, and the release workflow did not
generate it. The wheel's three-way hash was correct; the asset inventory
check was not. v1.0.4 closes this gap.
