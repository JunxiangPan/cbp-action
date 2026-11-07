"""AST taint engine tests."""
from pathlib import Path
from cbp.ast_engine import analyze_source, scan_file


def test_request_to_eval_is_tainted() -> None:
    findings = analyze_source("x = request.args.get('x')\neval(x)\n", "a.py")
    assert findings and findings[0]["rule"] == "CBP-TAINT-001"


def test_constant_to_eval_is_safe() -> None:
    assert analyze_source("eval('1+1')\n", "a.py") == []


def test_large_file_is_skipped(tmp_path: Path) -> None:
    path = tmp_path / "big.py"
    path.write_text("x = request.args.get('x')\neval(x)\n" + "#" * 20, encoding="utf-8")
    assert scan_file(path, tmp_path, max_bytes=5) == []
