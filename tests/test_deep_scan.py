"""Deep AST scan and external report integration."""
import json
from pathlib import Path
from cbp import custom_rules
from cbp.config import GateConfig


def test_deep_scan_reports_taint(tmp_path: Path) -> None:
    (tmp_path / "a.py").write_text("x = request.args.get('x')\neval(x)\n", encoding="utf-8")
    cfg = GateConfig(root=tmp_path, enable_deep_scan=True)
    passed, detail = custom_rules.run(cfg)
    assert passed is False and "CBP-TAINT-001" in detail


def test_external_sarif_is_merged(tmp_path: Path) -> None:
    report = tmp_path / "r.sarif"
    report.write_text(json.dumps({"runs": [{"tool": {"driver": {"name": "CodeQL"}}, "results": [{
        "ruleId": "x", "level": "error", "message": {"text": "bad"},
        "locations": [{"physicalLocation": {"artifactLocation": {"uri": "a.py"}, "region": {"startLine": 2}}}],
    }]}]}), encoding="utf-8")
    cfg = GateConfig(root=tmp_path, external_reports=("r.sarif",))
    passed, detail = custom_rules.run(cfg)
    assert passed is False and "CodeQL" not in detail and "bad" in detail
