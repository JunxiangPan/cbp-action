# Governance verification (test PR)

This file is created only to verify merge blocking with a **green** `cbp-gate`.

Expected:
- cbp-gate: success
- merge: blocked by branch protection (required review / required checks)
- PR is closed without merge.

Real configuration checked separately:

- main: require PR, 1 approval, required check `cbp-gate`, enforce admins, no force push, no deletion.
- tags: active ruleset for `refs/tags/v*`, block update/delete, no bypass.
- tag map: v1.2.0..v1.3.2 pinned in `docs/tags-expected.json`.
