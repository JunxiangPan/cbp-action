"""Static input-boundary checks for composite action and release workflow."""
from pathlib import Path


def _run_blocks(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks = []
    current = []
    in_run = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("run: |"):
            in_run = True
            current = []
            continue
        if in_run:
            if line.strip() and not line.startswith((" ", "\t")):
                in_run = False
                blocks.append("\n".join(current))
            else:
                current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def test_action_run_blocks_do_not_interpolate_inputs() -> None:
    for block in _run_blocks(Path("action.yml")):
        assert "${{ inputs." not in block


def test_release_run_blocks_do_not_interpolate_inputs() -> None:
    for block in _run_blocks(Path(".github/workflows/release.yml")):
        assert "${{ inputs." not in block
