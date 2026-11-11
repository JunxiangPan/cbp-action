# CBF adoption — CBP

Status: **PENDING_CBF_0.1.0**

- surfaces: `git` / `api` / `local-ai`
- planned gate: `cbf gate --surface git`
- planned CI job: `cbf-privacy-gate`
- evidence format: `cbf-evidence/v1`

CBP has **not** integrated CBF. There is **no CBF PASS**, and CBP does not
claim CBF compatibility. CBF is an independent project; CBP does not import it
and does not require it to be installed for normal development.

## Phase 0 (current)

- Adoption documented here.
- The `cbf-privacy-gate` CI job name is reserved in this document only; no
  workflow file is added in Phase 0.
- Existing CI does not fake a CBF result and does not use `continue-on-error`
  or `if: false` to bypass it.
- No GitHub Release, PyPI upload, or git push is claimed to have CBF evidence.

## Phase 1 (after CBF 0.1.0rc1)

- Add `cbf.policy.json` pinned to the CBF policy version/hash.
- Wire `cbf-privacy-gate` into the release path and add the local pre-push
  `cbf gate --surface git`.
- Block GitHub Release / PyPI on CBF failure; record `cbf-evidence/v1`.

## Boundary

CBF is a release/upload privacy gate, not a replacement for CBP's evidence
gate. CBP does not modify its frozen quality-manifest schema or import CBF.
