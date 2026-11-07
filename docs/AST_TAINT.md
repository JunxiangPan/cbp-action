# AST and Taint Layer

The deep-scan layer is optional and controlled by:

```json
{
  "enable_deep_scan": true,
  "ast_max_bytes": 1000000,
  "external_reports": ["reports/semgrep.json", "reports/codeql.sarif"]
}
```

## Taint rule

`CBP-TAINT-001` tracks request-like sources into dangerous sinks in one file:

```python
x = request.args.get("x")
eval(x)
```

Large files over `ast_max_bytes` are skipped and fall back to the regex layer.

## External reports

Supported report shapes:

- SARIF 2.1.0
- Semgrep JSON (`results[]`)
- SonarQube JSON (`issues[]`)

Reports are normalized and deduplicated by `path`, `line`, `rule`.
