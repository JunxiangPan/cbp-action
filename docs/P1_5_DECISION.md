# P1-5 Detection-Layer CEL Decision

The CEL policy layer controls the final PASS/FAIL of comments, claims,
dependency, docs, and custom gates.

Moving the detection logic itself into CEL was attempted and rejected for this
release:

- The existing detectors rely on Python AST/tokenize, filesystem hashing, and
  PowerShell AST parsing, which CEL cannot express.
- Evaluating CEL once per file/finding adds a compile/evaluate cycle on the
  5k-file hot path.
- The measured Python detection path is already 6.44s for 5k files; a pure-CEL
  detection layer would lose the AST/token semantics and add overhead.

Decision: keep Python detection plus CEL policy decisions. This is an explicit
engineering compromise, documented rather than hidden.

## Comments CEL experiment result

A 5,000-file CEL comment detector measured:

```text
count=5000 seconds=5.149 limit=4.000
```

This exceeded the 4-second red line. The CEL comments path is therefore
disabled and reports an explicit rejection; the Python detector remains the
only production engine. `scan_engine` defaults to `python`.
