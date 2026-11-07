"""Structured logging utilities for Hummingbot sub-packages."""

import dataclasses
from decimal import Decimal
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from logger.__about__ import __version__
from logger._install import install
from logger.levels import EVENT_LOG_LEVEL, METRICS_LOG_LEVEL, NETWORK
from logger.logger import HummingbotLogger


def log_encoder(obj: object) -> str | dict[str, object]:
    if isinstance(obj, (Decimal, Enum)):
        return str(obj)
    elif dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")


__all__ = [
    "__version__",
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
    "NETWORK",
    "EVENT_LOG_LEVEL",
    "METRICS_LOG_LEVEL",
    "HummingbotLogger",
    "install",
    "log_encoder",
]
