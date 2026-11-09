# CBP 1.2.0 release runbook

Status: **NOT EXECUTED**. Release requires explicit human approval. No tag, no
PyPI upload, no GitHub Release, and no PR merge has been performed.

## Authoritative RC artifact

Only the artifact produced by the audit RC run may be released.

| Item | Value |
| --- | --- |
| Code candidate | `72252b4` |
| RC workflow run | https://github.com/JunxiangPan/cbp-action/actions/runs/42596772450 |
| Artifact name | `cbp-rc` |
| wheel | `cbp_action-1.2.0-py3-none-any.whl` — `ee365cdde99c6ec453703fbf7dfb74617da9b65fff28b4350e8eebad93c7b6fb` |
| sdist | `cbp_action-1.2.0.tar.gz` — `870b52860f8b1a9b6a71300455229084fa0d83456255a1742038804abee16b26` |
| `RC_ASSETS.sha256` | `89e22fc9c91cb63094862e5409e825ec8254839892c84f819b75b09ea95d6dbe` |

Verify before any upload:

```bash
gh run download 42596772450 --repo JunxiangPan/cbp-action -n cbp-rc -D rc
sha256sum rc/cbp_action-1.2.0-py3-none-any.whl rc/cbp_action-1.2.0.tar.gz
gh attestation verify rc/cbp_action-1.2.0-py3-none-any.whl --repo JunxiangPan/cbp-action
gh attestation verify rc/cbp_action-1.2.0.tar.gz --repo JunxiangPan/cbp-action
```

## Local `dist/` is not the audit artifact

The local working-tree build is **not** release evidence:

```text
dist/cbp_action-1.2.0-py3-none-any.whl  3fdd809ac0eb6b53ccfffd5029febfc29a27e5b8ca2f9108951b4aeaec26cf9b
dist/cbp_action-1.2.0.tar.gz            c866d9a5d74aaf15b783aee61ea6c074370b8faf6e5987c313344b3f20534b88
```

Do not upload, tag, or attest these files. A local build is not reproducible
against the RC run and has no attestation.

## Superseded artifacts

Do not release any of these:

| Wheel | Sdist | Status |
| --- | --- | --- |
| `9469a8e9…` | `98b8916c…` | superseded by `72252b4` provenance fix |
| `589ab147…` | `4415f229…` | superseded |
| `40b0f5f8…` | `e30fa831…` | early RC, superseded |
| `06f8c3d3…` | `49592d6b…` | superseded |

## If a rebuild is required

1. Make the code change and push to `1.2.0-dev`.
2. Wait for the `cbp-rc` push run; it builds wheel + sdist and attests both.
3. Download the new `cbp-rc` artifact and verify both attestations.
4. Update this runbook, `AUDIT_PACKAGE.md`, `SELF_AUDIT.md`, `E2E_MATRIX.md`.
5. Mark the previous wheel/sdist **superseded** here; never overwrite a hash.

## Release steps (do not execute now)

1. Human re-audit of `docs/1.2.0/SELF_AUDIT.md`, `AUDIT_PACKAGE.md`,
   `RULE_MATRIX.md`, `E2E_MATRIX.md`, `EXTERNAL_MANIFEST.md` and the evidence
   bundle.
2. Human approval to release.
3. Merge PR #1 with the reviewed commit. Do not rewrite the RC candidate.
4. Create tag `v1.2.0` on the merge commit; the tag must not move.
5. Upload the exact wheel/sdist above to PyPI through the approved publish
   workflow; verify PyPI digests equal the release assets.
6. Create the GitHub Release from the same tag; attach wheel, sdist,
   `RELEASE_ASSETS.sha256`, `quality-manifest.json`, `quality-manifest.json.sha256`,
   and release notes. Verify `gh attestation verify`.
7. Consumer order: upgrade **CBM and CBC consumers first** (they need
   `body_hash_scope: "base"`), then upgrade CBE/CBP producers, then the CBS
   orchestrator. Do not let a producer emit 1.2.0 manifests before consumers can
   parse the new fields.
8. Post-release: verify `CONSUMER_VIEW_OK`, PyPI/Release digest equality,
   `--require-gate-pass`, and the 12-rule report on the release commit.

## Approval

Release still requires explicit human approval. This runbook is documentation
only; none of the steps above has been executed.
