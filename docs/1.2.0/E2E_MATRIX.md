# CBP 1.2.0 — Real-repository E2E matrix

Status: **RC evidence**. No repository outside `cbp-action-release` was modified.

## Method

```bash
python -m cbp.cli --root <repo> --v12 --v12-report <report>.json
```

Read-only: the rule engine only reads files, runs `git status` (no index writes)
and parses YAML/Python text. Reports were written outside the scanned
repositories. Windows paths were passed in native form (`D:\...`) because
`git -C` does not accept MSYS `/d/...` paths.

| Repository | Tip |
| --- | --- |
| CBP (`1.2.0-dev`) | this branch (Step 1–3) |
| CBS | `80e54e1` |
| CBE | `3390898` |
| CBM | `00d984e` |
| CBC | `ae18d0c` |

## Matrix

`P` = PASS, `W(n)` = WARN with n findings, `F(n)` = FAIL with n findings.

| Rule | CBP | CBS | CBE | CBM | CBC |
| --- | --- | --- | --- | --- | --- |
| CBP-CI-001 TEST_ROOTS_IN_CI | P | P | P | **F(1)** | P |
| CBP-VER-001 VERSION_SYNC | P | P | P | P | P |
| CBP-QA-001 QA_COUNTS_CONSISTENT | P | P | P | P | P |
| CBP-DEBT-001 DEBT_EVIDENCE | P | P | P | P | P |
| CBP-SIGN-001 SIGN_TOOLS_IN_TAG | P | P | P | P | P |
| CBP-WT-001 WORKTREE_CLEAN_AFTER_GATES | P | P | P | P | P |
| CBP-BIN-001 BINARY_AUTHENTICODE | P | W(1) | P | P | P |
| CBP-DOC-001 DOC_REFERENCES_EXIST | P | W(29) | W(4) | W(12) | P |
| CBP-CLAIM-001 CAPABILITY_CLAIMS | P | P | P | P | P |
| CBP-COV-001 COVERAGE_HARD | P | P | P | P | P |
| CBP-PROOF-001 PROOF_HIGH_TIER | P | P | P | P | P |
| CBP-SLOP-001 DOCSTRING_SLOP | P | P | P | P | P |
| **Exit** | 0 | 0 | 0 | **3** | 0 |

## Blocking failure

| Repository | Rule | Finding | Classification |
| --- | --- | --- | --- |
| CBM | CBP-CI-001 | `tests: test root is not executed by any workflow` | **true positive**. `cbm-attach.yml` has no test step; the repo has no CI test job and no remote. Not waived: fixing it belongs to CBM. |

No other blocking rule failed. There is no unexplained blocking failure.

## Warnings

Warning rules do not block in 1.2.0 (they will in 1.2.1); they are recorded here
so the baseline can be reviewed.

| Repository | Rule | Count | Classification |
| --- | --- | ---: | --- |
| CBS | CBP-BIN-001 | 1 | true positive: `START-INSTALLER.exe` has no Authenticode blob |
| CBS | CBP-DOC-001 | 29 | true positive: documentation drift (old status docs, removed tests, runtime-only paths). Sample: `DEPLOYMENT.md:18 → docs/STATUS_v1.6.1.md` |
| CBE | CBP-DOC-001 | 4 | true positive: `docs/E2E_MATRIX_V1.md` names CBE-08…CBE-11 test files that are not implemented yet |
| CBM | CBP-DOC-001 | 12 | mixed: `docs/v1.7/*` is external contract namespace (skipped); `tools/dogfood_manifest.py` is CBP-owned and `tools/release_body_v17.py` is CBS-owned; `cbm-evidence/*` is a runtime path. Baselined, not waived. |

No warning is a false positive after the fixes below.

## False positives found and fixed in the implementation

| Symptom | Fix | Fixture |
| --- | --- | --- |
| Inline `run: pytest` ignored (CBC/CBS) | parse both block and inline `run:` | `test_ci_001_passes_when_the_root_runs` |
| Bare `pytest` (no path) did not cover roots | treat a pytest line without any root path as covering all roots | `test_ci_001_ignores_a_path_in_a_comment` |
| `passed`/`PASSED` QA status rejected | accept PASS/PASSED/FAIL/FAILED/SKIP/SKIPPED/WARN/PARTIAL | `test_qa_001_passes_consistent_counts` |
| `examples/…/tests` treated as a project test root | ignore examples/fixtures/vendor/third_party | CBP self-run (12/12) |
| `docs/v1.7/*`, `schemas/v1.7/*` treated as local | external contract namespace | CBE run (DOC 14 → 4) |
| Planned links flagged | skip lines marked pending/planned/not yet/future/todo | CBE E2E matrix |
| Bare filenames flagged | resolve a bare filename as weak, never fatal | CBP self-run |
| Command names in backticks / code fences / headings flagged as claims | strip code spans and fences, skip headings and CLI usage | CBE run (CLAIM 14 → 0) |
| `claim this …` as a prohibited claim | soft marker `claim this` | CBS run (CLAIM 2 → 0) |

The fixtures were added or extended; no test was deleted to make a rule pass.

## Consumer parity (1.1.0 vs 1.2.0)

The same manifest files were parsed by the published 1.1.0 wheel and by the
1.2.0 worktree.

| Reader | Manifest | Result |
| --- | --- | --- |
| 1.1.0 | 1.1.0 (`quality-manifest.json` from the v1.1.0 release) | exit 0 |
| 1.2.0 | 1.1.0 | exit 0 (the new fields are optional) |
| 1.2.0 | 1.2.0 (with `body_hash_scope`, `artifact_repository`) | exit 0 |
| 1.1.0 | 1.2.0 | exit 2: `manifest: unexpected key(s) artifact_repository, body_hash_scope` |

Conclusion: compatibility is one-way. 1.2.0 reads old manifests, but a pinned
1.1.0 consumer rejects a 1.2.0 manifest. Upgrade consumers (CBS/CBE/CBM) before
a producer starts emitting 1.2.0 manifests. CBM and CBC need `body_hash_scope`
anyway, so they must move to 1.2.0 before their real E2E.

## Waivers used

None. The only blocking failure is genuine, and every warning is a true
positive after the implementation fixes above. A waiver would have hidden a real
finding, so no waiver file is shipped with the 1.2.0 RC.

## Reproduction

```bash
python -m cbp.cli --root "D:\path\to\repo" --v12 --v12-report report.json
python -m cbp.cli --root "D:\path\to\repo" --v12 --v12-only CBP-CI-001
```
