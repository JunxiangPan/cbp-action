# CBP v1.0.0 — Release-evidence gate

Prove the green build was not faked.

CBP v1.0.0 is the first stable release. It is not an AI-code detector; it is a
release-evidence gate for encoding, coverage, dependencies, comments, docs,
claims, binaries, custom rules, and upgrades.

## What is in 1.0.0

- Nine gates with explicit PASS / FAIL / SKIPPED status.
- `cbp init` and zero-config quick start.
- LCOV and Cobertura coverage adapters.
- Source-hash and environment-fingerprint coverage binding.
- CEL policy layer for comments, claims, dependency, docs, and custom.
- Rule packs with SHA256 verification and recursive `extends`.
- `cbp policy test` fixtures.
- SARIF, GitHub Checks API, and Code Scanning integration.
- Deterministic wheel normalization and double-build comparison.
- Content-addressed custom-gate cache.
- AST taint layer (`CBP-TAINT-001`) and external report aggregation for
  SARIF / Semgrep / SonarQube findings.
- PyPI trusted publishing through GitHub OIDC; no long-lived PyPI token.

## Quality evidence

```text
QUALITY_COUNTS: 9/9
```

```text
CBP gates: 9/9 PASS
Test suite: 197 passed
5k file scan: 6.44s
5k cached scan: 0.31s
5k AST scan: 4.05s
```

The release assets include `quality-manifest.json` and its SHA256, pinned to the
CI run id and commit SHA.

## PyPI and artifact identity

```text
cbp-action 1.0.0
https://pypi.org/project/cbp-action/1.0.0/

cbp_action-1.0.0-py3-none-any.whl
sha256: 79e75a33eb41363772bc8a0879b6b81cc5a72be2c70660dcf134daabdbfecfe4
```

GitHub Release and PyPI use the same wheel hash.

## P1-5 CEL decision

The CEL policy layer is active. A pure-CEL comment detector was attempted and
measured:

```text
5000 files: 5.149s
limit:      4.000s
```

It exceeded the performance red line, so the CEL detection path is disabled and
the Python detector remains the production engine. This is documented in
`docs/P1_5_DECISION.md`; the CEL policy decision layer remains enabled.

## Install

```bash
pipx install cbp-action
```

```yaml
- uses: JunxiangPan/cbp-action@v1.0.0
  with:
    root: .
    mode: enforce
```

For production, pin the full commit SHA.

## Known boundary

- AST taint analysis is single-file and assignment-level, not interprocedural.
- External reports are normalized into CBP findings; they do not replace the
  original tools.
- The CEL detection layer for comments is disabled after exceeding the
  4-second red line.
