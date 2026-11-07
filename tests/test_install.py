import inspect
import logging
import subprocess
import sys
import uuid
from collections.abc import Iterator

import pytest

from logger import HummingbotLogger, install
from logger.levels import LEVEL_NAMES
from logger.struct_logger import StructLogger, StructLogRecord


@pytest.fixture(autouse=True)
def restore_logging_state() -> Iterator[None]:
    old_class = logging.getLoggerClass()
    old_factory = logging.getLogRecordFactory()
    old_names = {
        level: (logging._levelToName.get(level), logging._nameToLevel.get(name))  # noqa: SLF001
        for level, name in LEVEL_NAMES.items()
    }
    before = set(logging.Logger.manager.loggerDict)
    yield
    logging.setLoggerClass(old_class)
    logging.setLogRecordFactory(old_factory)
    for level, name in LEVEL_NAMES.items():
        old_name, _ = old_names[level]
        if old_name is None:
            logging._levelToName.pop(level, None)  # noqa: SLF001
            logging._nameToLevel.pop(name, None)  # noqa: SLF001
        else:
            logging._levelToName[level] = old_name  # noqa: SLF001
    for key in set(logging.Logger.manager.loggerDict) - before:
        del logging.Logger.manager.loggerDict[key]


def _prefix() -> str:
    return f"hbtest_install_{uuid.uuid4().hex}"


def test_import_has_no_side_effects() -> None:
    code = (
        "import logging\n"
        "import logger, logger.struct_logger\n"
        "assert logging.getLoggerClass() is logging.Logger\n"
        "assert logging.getLogRecordFactory() is logging.LogRecord\n"
        "for lvl in (14, 15, 16):\n"
        "    assert logging.getLevelName(lvl) == f'Level {lvl}', lvl\n"
    )
    subprocess.run([sys.executable, "-c", code], check=True)


def test_install_is_idempotent() -> None:
    prefix = _prefix()
    assert install(StructLogger, StructLogRecord, reclass_prefixes=(prefix,)) is True
    assert logging.getLoggerClass() is StructLogger
    assert logging.getLogRecordFactory() is StructLogRecord
    for level, name in LEVEL_NAMES.items():
        assert logging.getLevelName(level) == name
    assert install(StructLogger, StructLogRecord, reclass_prefixes=(prefix,)) is False
    assert logging.getLoggerClass() is StructLogger
    assert logging.getLogRecordFactory() is StructLogRecord


def test_install_reclasses_existing_loggers_under_prefix() -> None:
    prefix = _prefix()
    exact = logging.getLogger(prefix)
    inside = logging.getLogger(f"{prefix}.a")
    sibling = logging.getLogger(f"{prefix}x.b")
    other = logging.getLogger(f"other_{uuid.uuid4().hex}.c")
    install(StructLogger, reclass_prefixes=(prefix,))
    assert isinstance(exact, StructLogger)
    assert isinstance(inside, StructLogger)
    assert not isinstance(sibling, StructLogger)
    assert not isinstance(other, StructLogger)
    assert isinstance(logging.getLogger(f"{prefix}.new"), StructLogger)


def test_install_does_not_reclass_unrelated_class() -> None:
    prefix = _prefix()

    class Other(logging.Logger):
        pass

    unrelated = Other(f"{prefix}.o")
    logging.Logger.manager.loggerDict[f"{prefix}.o"] = unrelated
    install(StructLogger, reclass_prefixes=(prefix,))
    assert type(unrelated) is Other


def test_reclassing_is_safe_no_instance_state() -> None:
    assert vars(HummingbotLogger("n")).keys() == vars(logging.Logger("n")).keys()
    assert vars(StructLogger("n")).keys() == vars(logging.Logger("n")).keys()
    assert "__slots__" not in HummingbotLogger.__dict__
    assert "__slots__" not in StructLogger.__dict__

    prefix = _prefix()
    log = logging.getLogger(f"{prefix}.b")
    assert type(log) is logging.Logger
    install(StructLogger, StructLogRecord, reclass_prefixes=(prefix,))
    assert type(log) is StructLogger

    records: list[logging.LogRecord] = []

    class Capture(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            records.append(record)

    log.addHandler(Capture())
    log.setLevel(logging.DEBUG)
    log.propagate = False
    log.event_log({"k": 1})  # type: ignore[attr-defined]
    log.network("msg")  # type: ignore[attr-defined]
    log.notify("msg")  # type: ignore[attr-defined]
    assert [r.levelname for r in records] == ["EVENT_LOG", "NETWORK", "INFO"]
    assert records[0].getMessage() == '{"k": 1}'


def test_install_rejects_non_logger_class() -> None:
    with pytest.raises(TypeError):
        install(object)  # type: ignore[arg-type]


def test_install_default_prefix() -> None:
    default = inspect.signature(install).parameters["reclass_prefixes"].default
    assert default == ("hummingbot",)
