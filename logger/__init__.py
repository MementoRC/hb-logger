"""Structured logging utilities for Hummingbot sub-packages."""

import dataclasses
import logging
from decimal import Decimal
from enum import Enum
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from logger.__about__ import __version__
from logger.logger import HummingbotLogger

NETWORK = DEBUG + 6


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
    "HummingbotLogger",
    "log_encoder",
]
logging.setLoggerClass(HummingbotLogger)
logging.addLevelName(NETWORK, "NETWORK")
