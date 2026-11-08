# CBP v1.0.9 — Release-evidence gate

Release evidence for v1.0.9.

This release body was generated from the built wheel by
`tools/generate_release_body.py`; the wheel SHA256 is not hand-edited.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.9-py3-none-any.whl
sha256: 77c9c40cb29b2e02ed57925d1c186ca7fd7e87677627c0cb2b78eb1b37d00400
```

https://pypi.org/project/cbp-action/1.0.9/

## Section A: Security regression (blocking)

- main CI: https://github.com/JunxiangPan/cbp-action/actions/runs/42480475240 PASS
- v1.0.6 verify: https://github.com/JunxiangPan/cbp-action/actions/runs/42462244338 PASS
- v1.0.7 verify: https://github.com/JunxiangPan/cbp-action/actions/runs/42463773268 PASS
- composite action payload E2E (15 hostile inputs): https://github.com/JunxiangPan/cbp-action/actions/runs/42480718091 PASS 15/15
- single build artifact re-verified: https://github.com/JunxiangPan/cbp-action/actions/runs/42480475240 PASS
- SARIF upload: https://github.com/JunxiangPan/cbp-action/actions/runs/42480475240 PASS
- Python 3.10: PASS (tested in the OS x Python matrix)
- checkout ref whitelist: PASS
- release body auto-generated: PASS (no manual backfill)
- release.yml permissions: PASS
- release asset inventory: PASS
- security_core: 90%+ floor

## Section B: AI audit gates (audit mode, non-blocking)

- ai-release / ai-test / ai-change run in the main CI `ai-audit` job; that job
  prints `AI_GATE_SUMMARY` with PASS / WARN / SKIP counts: https://github.com/JunxiangPan/cbp-action/actions/runs/42480475240
- Section B gates are audit-only and do not block publishing.

## Still to acknowledge

- ai-test false-positive rate is not yet measured on external projects.
- composite action payload E2E runs on GitHub Linux; local Windows is not verified.
- ai-release is structured evidence only, not natural-language summarization.
- Section B gates are audit-only and do not block publishing.

## Post-release verification (appended after publish)

This section was appended through the ERRATA mechanism after the release was
published, so it is not part of the body that clean-verify compared at publish
time. The wheel it names is unchanged.

- consumer parity: https://github.com/JunxiangPan/cbp-action/actions/runs/42480905065 PASS
- installed wheel == release asset digest == PyPI digest: sha256 77c9c40cb29b2e02ed57925d1c186ca7fd7e87677627c0cb2b78eb1b37d00400
- provenance: `gh attestation verify` PASS for that same wheel

