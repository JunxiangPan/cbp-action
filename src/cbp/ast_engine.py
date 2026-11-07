"""AST and single-file taint analysis for the deep-scan layer."""
from __future__ import annotations

import ast
from pathlib import Path

MAX_AST_BYTES = 1_000_000
SOURCE_NAMES = {
    "HttpRequest", "input", "argv", "environ",
    "get_json", "get", "form", "args", "query_params",
}
SINK_NAMES = {
    "eval", "exec", "system", "popen", "Popen", "run", "call",
    "loads", "load",
}


def _call_name(node: ast.Call) -> str:
    func = node.func
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return ""


def _is_source(node: ast.AST) -> bool:
    if isinstance(node, ast.Call):
        return _call_name(node) in SOURCE_NAMES or any(
            isinstance(arg, ast.Attribute) and arg.attr in SOURCE_NAMES for arg in node.args
        )
    if isinstance(node, ast.Attribute):
        return node.attr in SOURCE_NAMES
    return False


def analyze_source(source: str, path: str = "<memory>") -> list[dict]:
    """Track simple assignment taint from request-like sources into dangerous sinks."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    tainted: set[str] = set()
    findings: list[dict] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            value = node.value
            names = []
            if isinstance(node, ast.Assign):
                names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            elif isinstance(node.target, ast.Name):
                names = [node.target.id]
            if value is not None and (_is_source(value) or any(
                isinstance(sub, ast.Name) and sub.id in tainted for sub in ast.walk(value)
            )):
                tainted.update(names)
        if isinstance(node, ast.Call) and _call_name(node) in SINK_NAMES:
            risky = any(isinstance(arg, ast.Name) and arg.id in tainted for arg in node.args)
            if risky or any(_is_source(arg) for arg in node.args):
                findings.append({
                    "path": path,
                    "line": getattr(node, "lineno", 1),
                    "rule": "CBP-TAINT-001",
                    "message": "tainted request value reaches " + _call_name(node),
                    "severity": "error",
                    "tool": "cbp-ast",
                })
    return findings


def scan_file(path: Path, root: Path, max_bytes: int = MAX_AST_BYTES) -> list[dict]:
    """Analyze one Python file; large or non-Python files are skipped (L1 fallback)."""
    if path.suffix.casefold() != ".py":
        return []
    try:
        if path.stat().st_size > max_bytes:
            return []
        source = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    relative = path.relative_to(root).as_posix()
    return analyze_source(source, relative)


def scan_root(root: Path, max_bytes: int = MAX_AST_BYTES) -> list[dict]:
    """Walk Python files and collect AST/taint findings."""
    findings: list[dict] = []
    for path in sorted(root.rglob("*.py")):
        if any(part in {".git", ".venv", "node_modules", "__pycache__", "dist"} for part in path.parts):
            continue
        findings.extend(scan_file(path, root, max_bytes))
    return findings
