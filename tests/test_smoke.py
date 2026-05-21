"""Smoke test ensures package imports."""

import logger


def test_import() -> None:
    assert logger.__version__
