"""Coverage evidence is bound to the execution environment."""
from pathlib import Path
from cbp.source_hash import environment_fingerprint


def test_environment_fingerprint_is_stable_and_sha256(tmp_path: Path) -> None:
    value = environment_fingerprint(tmp_path)
    assert len(value) == 64
    assert value == environment_fingerprint(tmp_path)
