"""Custom log levels. Their names are registered by ``logger.install()``, not at import."""

from logging import DEBUG

NETWORK = DEBUG + 6
EVENT_LOG_LEVEL = 15
METRICS_LOG_LEVEL = 14

LEVEL_NAMES: dict[int, str] = {
    NETWORK: "NETWORK",
    EVENT_LOG_LEVEL: "EVENT_LOG",
    METRICS_LOG_LEVEL: "METRIC_LOG",
}
