# CBP 1.2.0 — self-audit (post-fix)

Status: **PASS for re-audit, no publish**. Code candidate `72252b4`, branch
`1.2.0-dev`, PR #1 open. Each item below cites the command, file or hash used.

## [1] Candidate identity / repository state — PASS

| Check | Evidence |
| --- | --- |
| Code candidate | `git rev-parse HEAD` → `72252b4db38b29bb773462e3b3c0520a4a3db7ef` |
| Branch | `1.2.0-dev` |
| PR #1 | `gh pr view 1` → `state=OPEN`, head `72252b4` |
| CI | run `42596785338` — success |
| Action E2E | run `42596785416` — success |
| v1.2.0 tag | `git ls-remote --tags origin refs/tags/v1.2.0` → empty |
| PyPI 1.2.0 | `https://pypi.org/pypi/cbp-action/1.2.0/json` → **404** |
| GitHub Release | `gh release view v1.2.0` → not found |
| v1.1.0 untouched | `git rev-parse 'v1.1.0^{}'` → `f98acf3ed15498b6f16d1a397a5d0f1fe2843fa9` |

## [2] Tests / CI — PASS

- `python -m pytest -q tests` → **406 passed**, 43 warnings.
- Coverage: `python -m coverage run --branch --source=src/cbp,tools -m pytest -q tests`
  then `python -m coverage json` → `security_core=91.64%/90.00%`,
  `cbp=90.56%/80.00%`.
- CI run `42596785338`: all jobs success (4 test-coverage cells, dogfood,
  sarif, checks, quickstart, repo-hygiene). Action E2E `42596785416`: success
  (15/15 payload + consumer parity).

## [3] Build artifacts / attestation — PASS

| Artifact | SHA256 |
| --- | --- |
| `cbp_action-1.2.0-py3-none-any.whl` | `ee365cdde99c6ec453703fbf7dfb74617da9b65fff28b4350e8eebad93c7b6fb` |
| `cbp_action-1.2.0.tar.gz` | `870b52860f8b1a9b6a71300455229084fa0d83456255a1742038804abee16b26` |
| `RC_ASSETS.sha256` | `89e22fc9c91cb63094862e5409e825ec8254839892c84f819b75b09ea95d6dbe` |

- Source: RC run `42596772450`, artifact `cbp-rc`.
- `gh attestation verify <wheel>` → exit 0; `gh attestation verify <sdist>` →
  exit 0; subject digests equal the table above.
- Local `dist/` is **not** the audit artifact: wheel
  `3fdd809ac0eb6b53ccfffd5029febfc29a27e5b8ca2f9108951b4aeaec26cf9b`, sdist
  `c866d9a5d74aaf15b783aee61ea6c074370b8faf6e5987c313344b3f20534b88`.
  `RELEASE_RUNBOOK.md` forbids publishing these.

## [4] Twelve rules — PASS

- `python -m cbp.cli --root . --v12` → 12 PASS, 0 FAIL, 0 WARN,
  `blocking_failed=false`; report `docs/1.2.0/evidence/v12-cbp.json`.
- 6 blocking: CI-001, VER-001, QA-001, DEBT-001, SIGN-001, WT-001.
- 6 warning: BIN-001, DOC-001, CLAIM-001, COV-001, PROOF-001, SLOP-001.
- Current tips: CBS `dcd96732`, CBE `9a1f5f28`, CBM `8acb628`, CBC `11943f14`.
  CBM `CBP-CI-001` is **PASS** (`docs/1.2.0/evidence/v12-cbm.json`); CBM only
  has `CBP-DOC-001 WARN (11)`. No blocking failure on any tip.

## [5] External manifest structure — PASS

| Target | Manifest | Validation |
| --- | --- | --- |
| CBC `11943f14` | `01438d31067f05508454c81af068efc61c9797034c778746b94d77e3de63bac0` | `cbc_viewer.reports.validate_cbp` → PASS; package cbc/cbp/v0.1.0; base; 2 artifacts |
| CBM `8acb628` | `967f15ccd8f222518ceb3c613ffda8d4f2ed04cfede958485f0bd79531e410cb` | `cbm_attach.reports.load_report` → PASS; B3 fields present; gate_status FAIL preserved |

CBM B3 fields: `body_hash_scope=base`, `release_body_hash`,
`artifact_hashes=2`, `evidence_sha256`. **B2 is not claimed**: no real CBE
report with `package_id: "cbm"`.

## [6] Gate provenance — PASS

CBC gate report `213e824392879ce539c6664725d5cd919b7f1d471de8d91b9f75d2557279e78b`:
`package_id=cbc`, `producer_id=cbp`, `version=v0.1.0`.

CBM gate report `ac4d243b94a13a2aa591ba96890fdd4d2f4984c30e6e199c15b9ccaf102be7d3`:
`package_id=cbm`, `producer_id=cbp`, `version=v0.1.0`.

- The two reports are byte-different (hashes above; not `a33971f5…`).
- The manifests' `gates[]` equal the target reports' `gates[]`; CBM's
  `encoding: FAIL` is preserved.
- `cbp manifest` with CBC gate report + `--package-id cbm` → exit 2, no file.
- `cbp manifest` with a `v0.0.0` gate report + `--version v0.1.0` → exit 2.
- Tests: `test_gate_report_package_id_must_match_the_target`,
  `test_gate_report_version_must_match_the_target`,
  `test_manifest_gates_come_from_the_gate_report`,
  `test_gate_report_generator_records_target_identity`.

CBM's `encoding FAIL` on `audit/v1.2.0-rc/b5-probe-declared.stdout.txt`
(invalid UTF-8) is a real target finding, not a CBP provenance defect.

## [7] E2E / docs / release hygiene — PASS

- `E2E_MATRIX.md` tips: CBS `dcd96732`, CBE `9a1f5f28`, CBM `8acb628`,
  CBC `11943f14`; CBM CI-001 PASS.
- CBC manifests recorded: `f897bc90…` (historical), `5f952d9b…` (earlier
  R01–R19), `01438d31…` (current). `EXTERNAL_MANIFEST.md` and
  `AUDIT_PACKAGE.md` use the same values.
- CBP-DOC-001: CBP v12 PASS; the two problematic references were changed to
  CBE/CBS names and the suffix search now ignores `.tmp-*`.
- `docs/1.2.0/RELEASE_RUNBOOK.md` exists and forbids the local `dist/`.
- `git ls-files` has no `.tmp*`, `pytest-current` or `__pycache__`.
- No v1.2.0 tag, no PyPI upload, no GitHub Release; PR #1 is open and unmerged.

## Verdict

All seven items pass for re-audit. The only non-PASS gate result in the train is
CBM's real `encoding FAIL`; it is preserved in the CBM manifest and must be
fixed by CBM, not waived. Release remains blocked on human approval.
