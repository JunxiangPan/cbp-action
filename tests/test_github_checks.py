"""GitHub Checks parser."""
from tools.github_checks import parse_gates


def test_parse_gate_statuses() -> None:
    text = "encoding: PASS\ncoverage: FAIL\ncustom: SKIPPED (not configured)\nCBP_RESULT=FAIL"
    assert parse_gates(text) == [("encoding", "PASS"), ("coverage", "FAIL"), ("custom", "SKIPPED")]


def test_annotations_include_file_and_line() -> None:
    from tools.github_checks import annotations

    result = annotations("src/a.py:3: bad thing")
    assert result[0]["path"] == "src/a.py"
    assert result[0]["start_line"] == 3
    assert result[0]["annotation_level"] == "failure"
