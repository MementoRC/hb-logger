# hb-logger

[![CI](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MementoRC/hb-logger)](https://codecov.io/gh/MementoRC/hb-logger)
[![PyPI version](https://badge.fury.io/py/hb-logger.svg)](https://badge.fury.io/py/hb-logger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Structured logging utilities for Hummingbot sub-packages.

## Overview

`hb-logger` provides structured logging utilities extracted from `hummingbot` core as a
standalone sub-package. It registers `HummingbotLogger` as the default Python logger class,
adds a `NETWORK` log level, and exports a `log_encoder` helper for JSON-serialising common
Hummingbot types (`Decimal`, `Enum`, dataclasses). The module name is `logger` (no `hb_`
prefix, per the hb-* ecosystem convention).

## Installation

```bash
pip install hb-logger
```

Or with pixi:

```bash
pixi add hb-logger
```

## Usage

```python
from logger import HummingbotLogger, NETWORK, log_encoder
import logging
import json

# HummingbotLogger is set as the default logger class on import.
logger: HummingbotLogger = logging.getLogger(__name__)  # type: ignore[assignment]

# Log at the custom NETWORK level (between DEBUG and INFO).
logger.log(NETWORK, "WebSocket connection established")

# Serialise Hummingbot types to JSON.
from decimal import Decimal

payload = {"price": Decimal("1.23456")}
print(json.dumps(payload, default=log_encoder))
# {"price": "1.23456"}
```

## License

Apache-2.0. See [LICENSE](LICENSE).
