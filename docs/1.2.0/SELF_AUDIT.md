# CBP 1.2.0 — self-audit (release-path fix)

Status: **PASS for re-audit, no publish**. Code candidate `8431712`, branch
`1.2.0-dev`, PR #1 open. Each item cites the command, file or hash used.

## [1] Candidate identity / repository state — PASS

| Check | Evidence |
| --- | --- |
| Code candidate | `git rev-parse HEAD` → `8431712` |
| Branch | `1.2.0-dev` |
| PR #1 | `gh pr view 1` → `OPEN`, head `8431712` |
| CI | run `42601015605` — success |
| Action E2E | run `42601015694` — success |
| v1.2.0 tag | `git ls-remote --tags origin refs/tags/v1.2.0` → empty |
| PyPI 1.2.0 | `https://pypi.org/pypi/cbp-action/1.2.0/json` → **404** |
| GitHub Release | `gh release view v1.2.0` → not found |
| v1.1.0 untouched | `git rev-parse 'v1.1.0^{}'` → `f98acf3ed15498b6f16d1a397a5d0f1fe2843fa9` |

## [2] Tests / CI — PASS

- `python -m pytest -q tests` → **414 passed**, 43 warnings.
- Coverage: `python -m coverage run --branch --source=src/cbp,tools -m pytest -q tests`
  then `python -m coverage json` → `security_core=91.64%/90.00%`,
  `cbp=90.56%/80.00%`.
- CI run `42601015605`: all jobs success. E2E `42601015694`: success
  (15/15 payload + consumer parity).

## [3] Build artifacts / attestation — PASS

| Artifact | SHA256 |
| --- | --- |
| wheel | `9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530` |
| sdist | `7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a` |
| `RC_ASSETS.sha256` | `4b2162c4c6aea24250d6e9af07fd85eb27e6420ba60e5ad21d8d9137469c3a1d` |

- Source: RC run `42601010528`, artifact `cbp-rc`.
- `gh attestation verify <wheel>` → exit 0; `gh attestation verify <sdist>` →
  exit 0; subject digests equal the table.
- Local `dist/` is **not** the audit artifact: wheel
  `3fdd809ac0eb6b53ccfffd5029febfc29a27e5b8ca2f9108951b4aeaec26cf9b`, sdist
  `c866d9a5d74aaf15b783aee61ea6c074370b8faf6e5987c313344b3f20534b88`. The
  runbook forbids publishing them.

## [4] Twelve rules — PASS

- `python -m cbp.cli --root . --v12` → 12 PASS, `blocking_failed=false`.
- 6 blocking: CI-001, VER-001, QA-001, DEBT-001, SIGN-001, WT-001.
- 6 warning: BIN-001, DOC-001, CLAIM-001, COV-001, PROOF-001, SLOP-001.
- Current tips: CBS `dcd96732`, CBE `9a1f5f28`, CBM `8acb628`, CBC `11943f14`.
  CBM CI-001 PASS; no blocking failure on any tip. Matrix in
  `docs/1.2.0/E2E_MATRIX.md`.

## [5] External manifest structure — PASS

| Target | Manifest | Validation |
| --- | --- | --- |
| CBC `11943f14` | `01438d31067f05508454c81af068efc61c9797034c778746b94d77e3de63bac0` | `validate_cbp` → PASS; cbc/cbp/v0.1.0; base; 2 artifacts |
| CBM `8acb628` | `967f15ccd8f222518ceb3c613ffda8d4f2ed04cfede958485f0bd79531e410cb` | `load_report` → PASS; B3 fields present; `gate_status FAIL` preserved |

CBM B3 fields: `body_hash_scope=base`, `release_body_hash`,
`artifact_hashes=2`, `evidence_sha256`. **B2 not claimed** (no real CBE report
with `package_id: "cbm"`). The external-manifest generator code is unchanged
since the CBC/CBM validation; the release-path fix does not touch it.

## [6] Gate provenance — PASS

- CBC gate report `213e8243…`: `package_id=cbc`, `producer_id=cbp`,
  `version=v0.1.0`, PASS.
- CBM gate report `ac4d243b…`: `package_id=cbm`, `producer_id=cbp`,
  `version=v0.1.0`, **FAIL** (`encoding`: invalid UTF-8 in
  `audit/v1.2.0-rc/b5-probe-declared.stdout.txt`).
- The reports are byte-different; the manifests' `gates[]` equal the target
  reports' gates.
- `cbp manifest` with CBC gate + `--package-id cbm` → exit 2, no file.
- `cbp manifest` with `v0.0.0` gate + `--version v0.1.0` → exit 2.
- Tests: `test_gate_report_package_id_must_match_the_target`,
  `test_gate_report_version_must_match_the_target`,
  `test_manifest_gates_come_from_the_gate_report`,
  `test_gate_report_generator_records_target_identity`.

## [7] E2E / docs / release hygiene — PASS

- `E2E_MATRIX.md`: current tips and CBM CI-001 PASS; no blocking failures.
- CBC manifests recorded: `f897bc90…`, `5f952d9b…`, `01438d31…`.
- CBP-DOC-001: CBP v12 PASS; the two problematic references were changed to
  CBE/CBS names, and `.tmp-*` is ignored in every rule walk.
- `RELEASE_RUNBOOK.md` exists and forbids `cbp-dist` and local `dist/`.
- `git ls-files` has no `.tmp*`, `pytest-current` or `__pycache__`.
- No v1.2.0 tag, no PyPI upload, no GitHub Release; PR #1 open and unmerged.

## [8] Release artifact provenance — PASS

- `release.yml` inputs include `rc_run_id`, `ci_run_id`, `release_tag`,
  `e2e_run_id`, `expected_wheel_sha256`, `expected_sdist_sha256`.
- `publish` downloads `gh run download "$RC_RUN_ID" -n cbp-rc -D rc` and
  `quality-manifest-$CI_RUN_ID`; it does **not** download or publish `cbp-dist`.
- It checks wheel `9807d02c…` and sdist `7da76e16…` against the expected inputs,
  checks `rc/RC_ASSETS.sha256`, verifies both RC attestations, and uses
  `rc/*.whl` / `rc/*.tar.gz` in `gh release create`.
- `tools/release_preflight.py` runs the same checks without creating a Release:
  correct inputs → 0 / `PREFLIGHT_OK`; wrong wheel or sdist hash → 3; tag/RC/CI
  commit mismatch → 3.
- Tests: `test_release_preflight.py` (4), `test_release_workflow.py` (4).
- Actual read-only preflight on 2026-11-09 (exit 0):

```text
PREFLIGHT_OK tag=v1.2.0 ci_run=42601015605 rc_run=42601010528 commit=8431712 wheel=9807d02c8b43f002381e8996d943c3b8077fe87ebab8b4530f42ff349f795530 sdist=7da76e1615f0680fa2bf8c0ad979a643b4971808e5b0b7ce4875d436fb35293a
```

Raw: `docs/1.2.0/evidence/preflight.txt`.

## [9] Tag / merge / run consistency — PASS

- The Fast-forward path is documented and is the only supported path for this
  RC: `merge --ff-only 1.2.0-dev`, tag `v1.2.0` at `8431712`; then
  `tag_commit == rc_run.head_sha == ci_run.head_sha == 8431712`; the actual
  preflight above printed `commit=8431712`.
- `release.yml` and the preflight reject any disagreement with exit 3.
- The runbook explicitly forbids tagging a GitHub merge commit and reusing RC
  run `42601010528`; a merge commit would require new CI, new RC, new
  attestation, and a new audit.

## Verdict

All nine items pass for re-audit. The only non-PASS gate result in the train is
CBM's real `encoding FAIL`; it is preserved and must be fixed by CBM, not
waived. Release remains blocked on human approval.
