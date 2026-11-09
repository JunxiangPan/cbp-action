# CBP 1.2.0 — RC audit package

Status: **STOPPED FOR HUMAN AUDIT**. Nothing was published to PyPI or as a
GitHub Release. Merging the draft PR, tagging, and publishing are owner actions.

## Candidate identity

| Item | Value |
| --- | --- |
| Branch | `1.2.0-dev` |
| RC commit | `bb8d4d6` (WT-001 extension + temp-file hygiene) |
| Draft PR | https://github.com/JunxiangPan/cbp-action/pull/1 |
| PR CI | run `42543611171` — success (4 matrix cells, dogfood, sarif, checks) |
| Action E2E | run `42543611163` — success (15/15 payload + consumer parity) |
| RC build + attest | run `42543607201` — success |
| wheel | `cbp_action-1.2.0-py3-none-any.whl`<br>`06f8c3d383d39ae4e42cee2a69abdaebdc15cae9fce63a65baf05da4d0998285` |
| sdist | `cbp_action-1.2.0.tar.gz`<br>`49592d6bd5ae90450cfa6e7e6f2487829d40c97e77d8f2b7d0f4fe6c7113d844` |
| Attestation | `gh attestation verify` exit 0 for both; subject digest equals the local hash; repository `JunxiangPan/cbp-action` |
| PyPI | `https://pypi.org/pypi/cbp-action/1.2.0/json` → **404** |
| GitHub Release | `v1.2.0` → **not found** |

Post-RC owner request (2026-11-09): extend CBP-WT-001 to reject conflict markers
in tracked files, add the clean/committed-marker fixtures, and run a real E2E
against CBS `contract/v1.7.1`. That change produced commit `9ee52fb`; a follow-up removed accidentally
tracked `.tmp-*` reports and fixed the ignore rule, producing `bb8d4d6`, the
current candidate. It supersedes `5da8b87`. The E2E failed as expected on three
committed markers in CBS `.github/workflows/vm-proof.yml:15/16/18`
(`docs/1.2.0/E2E_MATRIX.md`).

The RC workflow builds and attests only; it never uploads to a package index or
creates a release (`attest-build-provenance` + artifact upload).

## Test evidence

- Local: **390 passed**, 43 warnings.
- CI coverage: `security_core=91.64%/90.00%`, `cbp=90.55%/80.00%`.
- `docs/1.2.0/E2E_MATRIX.md`: 5 repositories × 12 rules, read-only, plus the
  requested CBS `contract/v1.7.1` E2E (exit 3, three committed conflict
  markers in `.github/workflows/vm-proof.yml:15/16/18`).

## Twelve rules — fixtures, tests, exit codes

| ID | Rule | Severity | Fixtures (positive / negative / false-positive guard) | Exit |
| --- | --- | --- | --- | --- |
| CBP-CI-001 | TEST_ROOTS_IN_CI | blocking | `test_ci_001_passes_when_the_root_runs` / `test_ci_001_fails_when_the_root_is_missing` / `test_ci_001_ignores_a_path_in_a_comment` | 3 |
| CBP-VER-001 | VERSION_SYNC | blocking | `test_ver_001_passes_when_sources_agree` / `test_ver_001_fails_on_a_mismatch` / `test_ver_001_ignores_older_changelog_headings` | 3 |
| CBP-QA-001 | QA_COUNTS_CONSISTENT | blocking | `test_qa_001_passes_consistent_counts` / `test_qa_001_fails_on_a_count_mismatch` / `test_qa_001_fails_when_covered_zero_contradicts_coverage` | 3 |
| CBP-DEBT-001 | DEBT_EVIDENCE | blocking | `test_debt_001_passes_with_evidence` / `test_debt_001_fails_without_evidence` / `test_debt_001_ignores_lowercase_prose` | 3 |
| CBP-SIGN-001 | SIGN_TOOLS_IN_TAG | blocking | `test_sign_001_passes_when_the_script_exists` / `test_sign_001_fails_when_the_script_is_missing` / `test_sign_001_ignores_a_path_in_a_comment` | 3 |
| CBP-WT-001 | WORKTREE_CLEAN_AFTER_GATES | blocking | `test_worktree_rule_passes_on_a_clean_tree` / `test_worktree_rule_detects_a_tracked_change` / `test_worktree_rule_fails_on_a_committed_conflict_marker` / `test_worktree_rule_flags_an_end_marker_without_a_start` / `test_worktree_rule_accepts_a_separator_without_a_conflict` / `test_worktree_rule_ignores_untracked_conflict_markers` | 3 |
| CBP-BIN-001 | BINARY_AUTHENTICODE | warning | `test_bin_001_passes_with_a_signature_blob` / `test_bin_001_fails_on_an_unsigned_installer` / `test_bin_001_passes_without_installers` | 0 (1.2.1: 3) |
| CBP-DOC-001 | DOC_REFERENCES_EXIST | warning | `test_doc_001_passes_when_the_path_exists` / `test_doc_001_fails_on_a_missing_path` / `test_doc_001_ignores_bare_prose_paths` | 0 (1.2.1: 3) |
| CBP-CLAIM-001 | CAPABILITY_CLAIMS | warning | `test_claim_001_passes_with_evidence` / `test_claim_001_fails_without_evidence` / `test_claim_001_accepts_an_audit_only_marker` | 0 (1.2.1: 3) |
| CBP-COV-001 | COVERAGE_HARD | warning | `test_cov_001_passes_with_a_hard_gate` / `test_cov_001_fails_when_downgraded` | 0 (1.2.1: 3) |
| CBP-PROOF-001 | PROOF_HIGH_TIER | warning | `test_proof_001_passes_with_all_markers` / `test_proof_001_fails_when_a_marker_is_missing` | 0 (1.2.1: 3) |
| CBP-SLOP-001 | DOCSTRING_SLOP | warning | `test_slop_001_ignores_a_few_template_docstrings` / `test_slop_001_fails_above_the_threshold` | 0 (1.2.1: 3) |

Waiver tests: `test_a_matching_waiver_suppresses_the_finding`,
`test_waiver_must_match_the_exact_path`, `test_an_expired_waiver_is_not_applied`,
`test_malformed_waiver_is_an_input_error`,
`test_warning_baseline_suppresses_until_expiry`,
`test_expired_baseline_does_not_suppress`.

CLI tests: `test_cli_v12_exit_codes_and_report`,
`test_cli_v12_blocks_on_a_blocking_rule`,
`test_cli_rejects_unsupported_body_scope`.

## Waivers and baseline

None are shipped or active for the RC.

- Entry schema: `{"rule", "path", "reason", "expires"}`; all four are required.
- Expired entries are not applied and are printed as `EXPIRED …`.
- Malformed or missing entries are an input error (exit 2).
- A waiver binds one rule to one exact path (or `*` for a documented global
  exception). A path mismatch does not suppress anything.
- Warning baselines use the same schema and the same expiry rule; 1.2.1 will
  turn unbaselined warnings into blocking findings.

## Consumer parity

| Reader | Manifest | Result |
| --- | --- | --- |
| 1.1.0 | 1.1.0 | exit 0 |
| 1.2.0 | 1.1.0 | exit 0 (new fields optional) |
| 1.2.0 | 1.2.0 | exit 0 |
| 1.1.0 | 1.2.0 | exit 2 — `unexpected key(s) artifact_repository, body_hash_scope` |

Upgrade order: consumers before producers. CBM/CBC require `body_hash_scope`
for their real E2E, so they must move to 1.2.0 before the train can pass.

## Unresolved items

1. **Publish approval** — owner decision. No tag, no PyPI upload, no Release.
2. **CBM CBP-CI-001** — true positive: CBM has no CI test job. It is outside
   this repository and was not waived.
3. **Warning baselines** — CBS (BIN 1, DOC 29), CBE (DOC 4), CBM (DOC 12) are
   recorded in `E2E_MATRIX.md`. They are warnings in 1.2.0; 1.2.1 needs an
   accepted baseline with expiry before they block.
4. **RC rebuild policy** — the RC workflow ignores docs-only pushes
   (`paths-ignore: docs/**, *.md`). Code commits still rebuild and require
   re-attestation. The candidate for this audit is `bb8d4d6` / run
   `42543607201`; `5da8b87` and `9ee52fb` are superseded.

## Reproduction

```bash
python -m pytest -q tests
python -m cbp.cli --root . --v12 --v12-report v12-report.json
gh run view 42543607201 --repo JunxiangPan/cbp-action
gh attestation verify cbp_action-1.2.0-py3-none-any.whl --repo JunxiangPan/cbp-action
```

Stop here. Human audit is required before tagging 1.2.0 or publishing.
