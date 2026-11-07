"""Runtime shell-boundary test for hostile GitHub Action inputs."""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

BASH = shutil.which("bash")


@pytest.mark.skipif(BASH is None, reason="bash not available")
def test_hostile_input_is_data_not_code() -> None:
    with tempfile.TemporaryDirectory(prefix="cbp-payload-") as temp:
        marker = Path(temp) / "pwned"
        payload = f"$(touch {marker});`touch {marker}`\n; touch {marker}; --help"
        script = 'test -n "$CBP_ROOT"; printf "%s" "$CBP_ROOT" >/dev/null'
        env = dict(os.environ, CBP_ROOT=payload)
        result = subprocess.run([BASH, "-c", script], env=env, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert not marker.exists()
