"""Explicit, idempotent installation of hb-logger into the process-global logging state."""

import logging
from collections.abc import Callable, Iterable

from logger.levels import LEVEL_NAMES
from logger.logger import HummingbotLogger


def _matches(name: str, prefixes: tuple[str, ...]) -> bool:
    return any(name == prefix or name.startswith(prefix + ".") for prefix in prefixes)


def install(
    logger_class: type[logging.Logger] = HummingbotLogger,
    record_factory: Callable[..., logging.LogRecord] | None = None,
    reclass_prefixes: Iterable[str] = ("hummingbot",),
) -> bool:
    """Install hb-logger into the stdlib ``logging`` module.

    Importing ``logger`` changes no global state; the composition root calls this
    once at startup. It is idempotent: a repeated call with the same arguments
    changes nothing and returns ``False``.

    - registers the NETWORK / EVENT_LOG / METRIC_LOG level names;
    - sets ``logger_class`` as the class for loggers created from now on;
    - sets ``record_factory`` as the LogRecord factory, if given;
    - re-classes loggers that already exist under ``reclass_prefixes`` (a name
      matches a prefix if it equals it or starts with ``prefix + "."``), so a
      logger created before ``install()`` behaves like one created after it.
      Only loggers whose class is a base class of ``logger_class`` are
      re-classed; loggers of an unrelated or more specific class are left alone.

    Returns ``True`` if any global state was changed.
    """
    if not (isinstance(logger_class, type) and issubclass(logger_class, logging.Logger)):
        raise TypeError(f"logger_class must be a subclass of logging.Logger, got {logger_class!r}")
    prefixes = tuple(reclass_prefixes)
    changed = False

    for level, name in LEVEL_NAMES.items():
        if logging.getLevelName(level) != name:
            logging.addLevelName(level, name)
            changed = True

    if logging.getLoggerClass() is not logger_class:
        logging.setLoggerClass(logger_class)
        changed = True

    if record_factory is not None and logging.getLogRecordFactory() is not record_factory:
        logging.setLogRecordFactory(record_factory)
        changed = True

    if prefixes:
        for name, existing in list(logging.Logger.manager.loggerDict.items()):
            if (
                isinstance(existing, logging.Logger)
                and type(existing) is not logger_class
                and issubclass(logger_class, type(existing))
                and _matches(name, prefixes)
            ):
                existing.__class__ = logger_class
                changed = True

    return changed
