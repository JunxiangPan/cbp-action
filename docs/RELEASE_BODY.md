# CBP v1.0.7 — Release-evidence gate

v1.0.7 = v1.0.6 evidence closure + three AI audit gates (audit mode, non-blocking).

This release body was generated from the built wheel by
`tools/generate_release_body.py`; the wheel SHA256 is not hand-edited.

## Verification

```text
QUALITY_COUNTS: 9/9
All 9 gates are active.
```

```text
cbp_action-1.0.7-py3-none-any.whl
sha256: f857611a2f90e8d67bb5637ca22561f4e8d704e36de2ddaa49164b8264cb1cce
```

https://pypi.org/project/cbp-action/1.0.7/

## Section A: Security regression (blocking)

- composite action payload E2E: 15/15 cases, Linux runner
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
