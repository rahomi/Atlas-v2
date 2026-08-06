"""Unit tests for Atlas package basics."""

from __future__ import annotations

import io
from contextlib import redirect_stdout

import atlas


def test_version() -> None:
    """The package should expose a version string."""
    assert isinstance(atlas.__version__, str)
    assert atlas.__version__ == "0.1.0"


def test_main_prints_version() -> None:
    """The main entry point should print the package name and version."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        atlas.main()
    output = buf.getvalue().strip()
    assert "Atlas v2" in output
    assert "0.1.0" in output