# CBP 1.2.0 release runbook

Status: **NOT EXECUTED**. Release requires explicit human approval. No tag, no
PyPI upload, no GitHub Release, and no PR merge has been performed.

## Authoritative RC artifact

Only the `cbp-rc` bundle from the audit RC run may be released. The CI
`cbp-dist` bundle is **not** a release input; it is used only for the
quality-manifest.

| Item | Value |
| --- | --- |
| Candidate commit | `d3ec73e` |
| RC run | https://github.com/JunxiangPan/cbp-action/actions/runs/42599351558 |
| CI run (manifest) | https://github.com/JunxiangPan/cbp-action/actions/runs/42599359187 |
| e2e run | https://github.com/JunxiangPan/cbp-action/actions/runs/42599359071 |
| Artifact | `cbp-rc` |
| wheel | `cbp_action-1.2.0-py3-none-any.whl` — `dafc9662eba03d2e2002f91a14708aa0384eeaf1d45926f72f8104c9196407d6` |
| sdist | `cbp_action-1.2.0.tar.gz` — `e58524e7edee996d1e41f3281f0ff6e4be0fea0d078c862b0aa5861b21059418` |
| `RC_ASSETS.sha256` | `8a28b2873d5b2d462929d57c909fdac57567d14b1d7b6835706178e1707d9358` |

The tag, RC run head and CI run head must all be candidate `d3ec73e`. Any
mismatch is exit 3 and no Release is created.

## Preflight (no Release, no PyPI)

```bash
python tools/release_preflight.py \
  --rc-run-id 42599351558 \
  --ci-run-id 42599359187 \
  --tag v1.2.0 \
  --expected-wheel-sha256 dafc9662eba03d2e2002f91a14708aa0384eeaf1d45926f72f8104c9196407d6 \
  --expected-sdist-sha256 e58524e7edee996d1e41f3281f0ff6e4be0fea0d078c862b0aa5861b21059418 \
  --e2e-run-id 42599359071 \
  --repository JunxiangPan/cbp-action
```

It downloads `cbp-rc` and `quality-manifest-42599359187`, checks both hashes,
`RC_ASSETS.sha256`, the manifest hash, the release body generation, and
tag/RC/CI commit equality. It prints `PREFLIGHT_OK` or exits 3.

## Release path (Fast-forward, recommended)

The tag must point at the same commit as the RC and CI runs. The RC run is for
`d3ec73e`; do not tag a merge commit that has no RC run.

```bash
git checkout main
git merge --ff-only 1.2.0-dev
git push origin main
git tag -a v1.2.0 d3ec73e -m "CBP v1.2.0"
git push origin v1.2.0
```

Then dispatch `release.yml` with:

```text
rc_run_id              42599351558
ci_run_id              42599359187
release_tag            v1.2.0
e2e_run_id             42599359071
expected_wheel_sha256  dafc9662eba03d2e2002f91a14708aa0384eeaf1d45926f72f8104c9196407d6
expected_sdist_sha256  e58524e7edee996d1e41f3281f0ff6e4be0fea0d078c862b0aa5861b21059418
```

`release.yml` downloads `cbp-rc`, verifies both hashes and `RC_ASSETS.sha256`,
requires `tag == RC head == CI head`, verifies the RC attestations, generates
the body from the RC wheel, and creates the Release from `rc/*`. Any mismatch
exits 3 before `gh release create`. PyPI publishes the Release assets.

### Merge-commit alternative (not recommended)

If a GitHub merge commit is used, its SHA differs from `d3ec73e`. The RC run
`42599351558` can no longer be used. You must run CI and RC again on the merge
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
3. Run the Fast-forward sequence above so the tag commit is `d3ec73e`.
4. Run the preflight command; require `PREFLIGHT_OK`.
5. Dispatch `release.yml` with the exact inputs above.
6. Verify the Release assets equal `dafc9662…` / `e58524e7…`, PyPI digests match
   the Release assets, and both `gh attestation verify` calls pass.
7. Consumer order: upgrade CBM and CBC consumers first (they need
   `body_hash_scope: "base"`), then CBE/CBP producers, then the CBS
   orchestrator. Do not emit 1.2.0 manifests before consumers can parse them.

## Approval

Release still requires explicit human approval. This runbook is documentation
only; none of the steps above has been executed.
