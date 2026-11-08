# CBP v1.0.8 — Release-evidence gate

v1.0.8 = v1.0.6 evidence closure + three AI audit gates (audit mode, non-blocking).

This release body was generated from the built wheel by
`tools/generate_release_body.py`; the wheel SHA256 is not hand-edited.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.8-py3-none-any.whl
sha256: 22eeaeab0fe2015b27d20873b471e270238056ef1cb65597a6c4a3d130076189
```

https://pypi.org/project/cbp-action/1.0.8/

## Section A: Security regression (blocking)

- main CI: not recorded PASS
- v1.0.6 verify: https://github.com/JunxiangPan/cbp-action/actions/runs/42462244338 PASS
- v1.0.7 verify: https://github.com/JunxiangPan/cbp-action/actions/runs/42463773268 PASS
- composite action payload E2E: not recorded PASS 15/15
- double build: not recorded PASS (byte-identical)
- SARIF upload: not recorded PASS
- Python 3.10: SKIPPED (setup-python 504; explicit, not removed from matrix)
- checkout ref whitelist: PASS
- release body auto-generated: PASS (no manual backfill)
- release.yml permissions: PASS
- release asset inventory: PASS
- security_core: 90%+ floor

## Section B: AI audit gates (audit mode, non-blocking)

- ai-release: PASS / WARN / SKIP (counts)
- ai-test: PASS / WARN / SKIP (counts) | self-check: separate
- ai-change: PASS / WARN / SKIP (counts)

## Still to acknowledge

- ai-test false-positive rate is not yet measured on external projects.
- composite action payload E2E runs on GitHub Linux; local Windows is not verified.
- ai-release is structured evidence only, not natural-language summarization.
- Section B gates are audit-only and do not block publishing.
