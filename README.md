# hb-logger

[![CI](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MementoRC/hb-logger)](https://codecov.io/gh/MementoRC/hb-logger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Structured logging utilities for Hummingbot sub-packages.

## Overview

`hb-logger` provides structured logging utilities extracted from `hummingbot` core as a
standalone sub-package. It provides `HummingbotLogger`, a `NETWORK` log level, an explicit
`install()` to register them with `logging`, and exports a `log_encoder` helper for JSON-serialising common
Hummingbot types (`Decimal`, `Enum`, dataclasses). The module name is `logger` (no `hb_`
prefix, per the hb-* ecosystem convention).

## Installation

```bash
pixi add hb-logger
```

## Usage

```python
from logger import HummingbotLogger, NETWORK, log_encoder
import logging
import json

# Importing `logger` changes no global state; call logger.install() to activate it.
logger: HummingbotLogger = logging.getLogger(__name__)  # type: ignore[assignment]

# Log at the custom NETWORK level (between DEBUG and INFO).
logger.log(NETWORK, "WebSocket connection established")

# Serialise Hummingbot types to JSON.
from decimal import Decimal

payload = {"price": Decimal("1.23456")}
print(json.dumps(payload, default=log_encoder))
# {"price": "1.23456"}
```

## Installing into logging

**Breaking change in 1.0.0:** importing `logger` no longer sets the logger class or registers
level names. Call `install()` once at startup (idempotent; returns `True` if anything changed):

```python
install(
    logger_class=HummingbotLogger,
    record_factory=None,
    reclass_prefixes=("hummingbot",),
) -> bool
```

```python
import logger
from logger.struct_logger import StructLogger, StructLogRecord

logger.install(StructLogger, StructLogRecord, reclass_prefixes=("hummingbot",))
```

It registers the `NETWORK` / `EVENT_LOG` / `METRIC_LOG` level names, sets the logger class and
record factory, and re-classes already-created loggers under the given prefixes.

## License

Apache-2.0. See [LICENSE](LICENSE).
