# hb-logger

> Status: scaffolding — initial standardization in progress.

Structured logging utilities for Hummingbot sub-packages.

<!--
Badges — uncomment after first green CI run:

[![CI](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml/badge.svg)](https://github.com/MementoRC/hb-logger/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/MementoRC/hb-logger)](https://codecov.io/gh/MementoRC/hb-logger)
[![PyPI version](https://badge.fury.io/py/hb-logger.svg)](https://badge.fury.io/py/hb-logger)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
-->

## Overview

`hb-logger` provides structured logging utilities extracted from `hummingbot` core as a
standalone sub-package. The module name is `logger` (no `hb_` prefix, per the hb-* ecosystem
convention).

## Installation

```bash
pip install hb-logger
```

Or with pixi:

```bash
pixi add hb-logger
```

## Development

```bash
# Install dev environment
pixi install

# Run tests
pixi run test

# Run linting and formatting
pixi run quality

# Run full check suite
pixi run check
```

## License

Apache-2.0. See [LICENSE](LICENSE).
