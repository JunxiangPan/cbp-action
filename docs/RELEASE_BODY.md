# CBP v1.0.5 — Release-evidence gate

CBP v1.0.5 fixes the GitHub Action shell input boundary.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.5-py3-none-any.whl
sha256: c6d2a8b2ea711855875cce54b0ac2548937f7145bcee95a09066e15e421798a2
```

https://pypi.org/project/cbp-action/1.0.5/

## What changed

- All `${{ inputs.* }}` values are passed through `env`; run blocks reference quoted environment variables.
- Release `ci_run_id` is digit-whitelisted and `release_tag` is semantic-version-whitelisted.
- Permissions are declared per job; only the publish job gets write/OIDC/attestation scope.
- Static E2E tests fail if a future run block interpolates untrusted inputs.
- Release asset inventory is mandatory: missing `RELEASE_ASSETS.sha256` exits 2.

## Erratum for v1.0.4

v1.0.4 still interpolated `${{ inputs.* }}` inside shell run blocks. Its asset
checks were valid, but the action input boundary was not. v1.0.5 fixes that.
