# CBP 1.2.0 release runbook

Status: **NOT EXECUTED**. Release requires explicit human approval. No tag, no
PyPI upload, no GitHub Release, and no PR merge has been performed.

## Authoritative RC artifact

Only the `cbp-rc` bundle from the audit RC run may be released. The CI
`cbp-dist` bundle is **not** a release input; it is used only for the
quality-manifest.

| Item | Value |
| --- | --- |
| Candidate commit | `8431712` |
| RC run | https://github.com/JunxiangPan/cbp-action/actions/runs/42601010528 |
| CI run (manifest) | https://github.com/JunxiangPan/cbp-action/actions/runs/42601015605 |
| e2e run | https://github.com/JunxiangPan/cbp-action/actions/runs/42601015694 |
| Artifact | `cbp-rc` |
| wheel | `cbp_action-1.2.0-py3-none-any.whl` — `9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530` |
| sdist | `cbp_action-1.2.0.tar.gz` — `7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a` |
| `RC_ASSETS.sha256` | `4b2162c4c6aea24250d6e9af07fd85eb27e6420ba60e5ad21d8d9137469c3a1d` |

The tag, RC run head and CI run head must all be candidate `8431712`. Any
mismatch is exit 3 and no Release is created.

## Preflight (no Release, no PyPI)

The tag does not exist yet, so pass `--tag-commit`; the tool resolves the
abbreviated SHA and compares it with the RC/CI heads.

```bash
python tools/release_preflight.py \
  --rc-run-id 42601010528 \
  --ci-run-id 42601015605 \
  --tag v1.2.0 \
  --tag-commit 8431712 \
  --expected-wheel-sha256 9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530 \
  --expected-sdist-sha256 7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a \
  --e2e-run-id 42601015694 \
  --repository JunxiangPan/cbp-action
```

Actual output on 2026-11-09:

```text
PREFLIGHT_OK tag=v1.2.0 ci_run=42601015605 rc_run=42601010528 commit=8431712 wheel=9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530 sdist=7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a
```

Raw copy: `docs/1.2.0/evidence/preflight.txt` (exit code 0).

Failure handling:

- `TAG_NOT_FOUND` / `rev-parse` failure: confirm `--tag-commit 8431712`; do not
  create a tag just to make preflight pass.
- hash mismatch: stop. Do not edit the expected hash to make it pass.
- RC/CI commit mismatch: stop. Do not tag.
- quality-manifest missing: stop and inspect CI run `42601015605`.

## HUMAN ONLY — release commands (not executed)

```bash
git checkout main
git merge --ff-only 8431712
git push origin main

git tag -a v1.2.0 8431712 -m "CBP v1.2.0"
git push origin v1.2.0

gh workflow run release.yml \
  --repo JunxiangPan/cbp-action \
  --ref v1.2.0 \
  -f rc_run_id=42601010528 \
  -f ci_run_id=42601015605 \
  -f release_tag=v1.2.0 \
  -f e2e_run_id=42601015694 \
  -f expected_wheel_sha256=9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530 \
  -f expected_sdist_sha256=7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a
```

`release.yml` downloads `cbp-rc`, verifies both hashes and `RC_ASSETS.sha256`,
requires `tag == RC head == CI head`, verifies the RC attestations, generates
the body from the RC wheel, and creates the Release from `rc/*`. Any mismatch
exits 3 before `gh release create`. PyPI publishes the Release assets.

### Merge-commit alternative (not recommended)

If a GitHub merge commit is used, its SHA differs from `8431712`. The RC run
`42601010528` can no longer be used. You must run CI and RC again on the merge
commit, re-attest, re-run preflight, and have the result re-audited. Do not tag a
merge commit and reuse an older RC run.

## Forbidden artifacts

Do not upload, tag, or attest these:

```text
local dist wheel  3fdd809ac0eb6b53ccfffd5029febfc29a27e5b8ca2f9108951b4aeaec26cf9b
local dist sdist  c866d9a5d74aaf15b783aee61ea6c074370b8faf6e5987c313344b3f20534b88
```

### Superseded RC artifacts

| Wheel | Sdist | Status |
| --- | --- | --- |
| `dafc9662…` | `e58524e7…` | superseded by the preflight short-SHA fix |
| `ee365cdd…` | `870b5286…` | superseded by the release-path fix |
| `9469a8e9…` | `98b8916c…` | superseded |
| `589ab147…` | `4415f229…` | superseded |
| `40b0f5f8…` | `e30fa831…` | early RC |
| `06f8c3d3…` | `49592d6b…` | early RC |

## Release steps (do not execute now)

1. Human re-audit of `SELF_AUDIT.md`, `AUDIT_PACKAGE.md`, `RULE_MATRIX.md`,
   `E2E_MATRIX.md`, `EXTERNAL_MANIFEST.md`, the evidence bundle, and this
   runbook.
2. Explicit human approval to release.
3. Run the HUMAN ONLY Fast-forward sequence above so the tag commit is
   `8431712`.
4. Run the preflight command; require `PREFLIGHT_OK`.
5. Dispatch `release.yml` with the exact inputs above.
6. Verify the Release assets equal `9807d02c…` / `7da76e16…`, PyPI digests match
   the Release assets, and both `gh attestation verify` calls pass.
7. Consumer order: upgrade CBM and CBC consumers first (they need
   `body_hash_scope: "base"`), then CBE/CBP producers, then the CBS
   orchestrator. Do not emit 1.2.0 manifests before consumers can parse them.

## Approval

Release still requires explicit human approval. This runbook is documentation
only; none of the steps above has been executed.
