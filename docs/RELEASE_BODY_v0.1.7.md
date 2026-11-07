# CBP v0.1.7 — Release-evidence gate

Prove the green build was not faked.

This release is not an AI-code detector. It verifies release evidence: coverage
freshness, dependency hashes, documentation history, release-note claims,
binary provenance, and the configured custom rules.

## What changed in 0.1.7

- Real wall-clock regex timeout: the optional `regex` package is used when
  available; otherwise matches run in an isolated child process and are killed
  on timeout.
- Generic inline suppression for file/line findings:
  `# cbp: ignore` or `# cbp: ignore=CBP-CMT-001`.
- Coverage ratchet: a group that drops below `coverage-ratchet.json` fails.
- LCOV and Cobertura XML coverage readers in addition to coverage.py JSON.
- Prebuilt wheel installed by `action.yml`; no editable source install.
- All workflow Actions are pinned to full commit SHAs.
- PyPI Trusted Publishing via GitHub OIDC; no long-lived PyPI token.
- Path-escape, required-artifact integrity, naked-subprocess, and Python
  environment-path checks from earlier releases remain active.

## Dogfood evidence

```text
QUALITY_COUNTS: 9/9
```

```text
gates: encoding, coverage, dependency, comments, docs,
       claims, custom, upgrade, binary — all PASS
cbp coverage:            87.56% (threshold 80%)
security_core coverage:  89.05% (threshold 89%)
test suite:              158 passed
```

The release assets include `quality-manifest.json` pinned to the CI run id and
commit SHA, plus its SHA256 and the generated release notes.

## PyPI

Published as:

```text
cbp-action 0.1.7
https://pypi.org/project/cbp-action/0.1.7/
```

```text
cbp_action-0.1.7-py3-none-any.whl
sha256: 3aa6901ee50db8429107cabe3e97db539c53ea585b3511e613d0fd081682d00b
```

Install:

```bash
pipx install cbp-action
```

## GitHub Action

```yaml
- uses: JunxiangPan/cbp-action@v0.1.7
  with:
    root: .
    mode: enforce
```

For production use, pin the full commit SHA rather than the mutable tag.

## Known boundary

- The release body uses `v0.1.7`; for strict supply-chain use, pin the commit.
- `regex` is optional; without it the child-process fallback is used.
