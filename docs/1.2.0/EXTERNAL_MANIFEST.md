# External-package quality-manifest generator (1.2.0 field capability)

Status: **RC only**. This adds fields and one command, not a thirteenth rule.

## Gap

CBC's `validate_cbp()` requires a CONTRACT §5 manifest with
`artifact_hashes`, `release_body_hash`, `evidence_sha256`, gate counts and
`body_hash_scope`. CBP 1.2.0 RC had no command for an arbitrary target package:
`--report-json` is a gate report, `--v12-report` is a rule report, and
`tools/dogfood_manifest.py` is hard-coded to `package_id: "cbp"`.

## Command

```bash
python -m cbp.cli manifest \
  --root <target> \
  --package-id cbc \
  --producer-id cbp \
  --version v0.1.0 \
  --gate-report <target gate report>.json \
  --artifact <target wheel> \
  --artifact <target sdist> \
  --release-body <target base body>.md \
  --body-hash-scope base \
  --evidence <gate report>.json \
  --artifact-repository owner/repo \
  --out quality-manifest.json
```

`--artifact` and `--evidence` are repeatable; `--artifact-sha256 NAME=HEX`
adds an expected digest check.

## Output

Always includes:

```text
schema_version, package_id, producer_id, version,
gate_status, applicable_gate_count, skip_count, skip_ratio,
blocking_skip, gates[], artifact_hashes, release_body_hash,
evidence_sha256, body_hash_scope
```

`package_id` is the subject under test, `producer_id` is the component that ran
the gates. `artifact_hashes` maps each artifact basename to a bare sha256.
`release_body_hash` hashes the **base** body: the bytes before
`<!-- CBC-EVIDENCE-BEGIN -->` when that marker is present, otherwise the whole
file. `evidence_sha256` is the canonical self-hash, or a canonical hash over the
manifest plus the evidence file digests when `--evidence` is used.

## Exit codes and failure modes

| Situation | Exit |
| --- | --- |
| manifest written | 0 |
| missing gate report / artifact / release body / evidence | 2 |
| `body_hash_scope` missing or not `base` | 2 |
| artifact digest mismatch (`--artifact-sha256`) | 2 |
| gate report has an invalid gate, or SKIPPED without a reason | 2 |
| skip ratio inconsistent with counts | 2 |
| gate report `FAIL` | 0, manifest keeps `FAIL` (never rewritten to PASS) |

Nothing is written on a failure; `--out` is only touched after all inputs and
hashes validate.

## Real E2E — CBC

Target: `cbc-event` HEAD `48d9762` (read-only; artifacts built from a `git
archive` copy in a temporary directory). Gate report: a real CBP 1.2.0 run on
CBC (`PASS`, 1 applicable gate, 8 not-configured skips not counted).

The first run produced `f897bc905d4cebfa82cc83f137440cb0a024e0dd060eaa022bca1fb7a3942724`.
For the R01–R19 run the artifacts were rebuilt, so the same `855fed7` generator
was used again; the manifest used for the cases is
`5f952d9bf82413520b87d31a41fba85f49e8242e203f83cc32e6c3d33a5cab20`:

```text
package_id cbc, producer_id cbp, version v0.1.0
body_hash_scope base, gate_status PASS
release_body_hash f63a222681b1e8a67f8de06f693e877a66fd58fe68714819315e42cbe41156de
artifact_hashes 2 (rebuilt cbc_event wheel + sdist)
```

Validation with CBC's own code:

```text
from cbc_viewer.reports import validate_cbp
CBC_VALIDATE_CBP=PASS
```

Release-chain cases `R02`–`R19` were run with CBC's own `verify_release` on a
release dir built from a real CBE report (minimal disclosed pack), the real CBC
wheel/sdist and the real manifest: **18/18 assertions matched** (17 executed;
R16 skipped on Windows because symlink creation needs a privilege). `R01` needs
an actually uploaded release and is **NOT RUN**; no upload is claimed. See
`docs/1.2.0/evidence/cbc-r01-r19/`.

The manifest blocker recorded in `cbc-event/audit/0.1.0-rc/CBP_MANIFEST_GAP.md`
is removed. The body used here is assembled from the real CBC CHANGELOG and is
labelled as such; it is not an official GitHub Release body (CBC has no release).

## Real E2E — CBM (B3 only)

Target: CBM HEAD `45c49bc` (read-only; artifacts built from an archive copy).
Generated manifest: `bc5461e61a4167dfae21fdf12fe169fa8339c7f20eac09f861799d89926196c1`,
`package_id cbm`, `producer_id cbp`, `version v0.1.0`, `body_hash_scope base`,
2 artifact hashes, `release_body_hash` + `evidence_sha256` present.

Validation with CBM's own loader:

```text
from cbm_attach.reports import load_report
CBM_LOAD=PASS package_id=cbm version=v0.1.0
B3_FIELDS {'body_hash_scope': 'base', 'release_body_hash': True,
           'artifact_hashes': 2, 'evidence_sha256': True}
```

**B3 is field-level complete.** B2 is **not** complete: there is still no real
CBE report with `package_id: "cbm"` + `producer_id`. CBM's full identity check
(`identity_errors`) will still report the missing CBE side. This run does not
claim B2, and does not claim a second producer.

## Test coverage

`tests/test_package_manifest.py` (12 tests): subject/producer written; base body
excludes the CBC appendix; missing gate/artifact/body; missing or `full` scope;
artifact hash mismatch; stable artifact/evidence hashes; a `FAIL` report stays
`FAIL`; SKIPPED without a reason is rejected. Full suite: **402 passed**.
