"""External report normalization."""
import json
from pathlib import Path
from cbp.report_aggregator import aggregate, normalize


def test_sarif_semgrep_sonar_are_normalized(tmp_path: Path) -> None:
    sarif = tmp_path / "s.sarif"
    sarif.write_text(json.dumps({"runs": [{"tool": {"driver": {"name": "CodeQL"}}, "results": [{
        "ruleId": "js/x", "level": "error", "message": {"text": "bad"},
        "locations": [{"physicalLocation": {"artifactLocation": {"uri": "src/a.py"}, "region": {"startLine": 3}}}],
    }]}]}), encoding="utf-8")
    semgrep = tmp_path / "semgrep.json"
    semgrep.write_text(json.dumps({"results": [{"check_id": "py.x", "path": "src/b.py", "start": {"line": 4},
                                               "extra": {"message": "bad", "severity": "ERROR"}}]}), encoding="utf-8")
    sonar = tmp_path / "sonar.json"
    sonar.write_text(json.dumps({"issues": [{"rule": "python:S1", "component": "src/c.py", "line": 5,
                                             "message": "bad", "severity": "MAJOR"}]}), encoding="utf-8")
    findings = aggregate(tmp_path, ["s.sarif", "semgrep.json", "sonar.json"])
    assert [item["tool"] for item in findings] == ["CodeQL", "semgrep", "sonarqube"]
    assert normalize(sarif)[0]["line"] == 3
