"""hb_compat — drop-in replacement layer for hummingbot.logger consumers.

For this sub-package the compat surface is intentionally empty.

The hummingbot logger has no callable contract that consumers need to
validate against via Protocol typing or string-classname adapters. After
the Phase 0 callback-registration refactor (see hb-logger#1), the
HummingbotLogger module is fully self-contained:

  - It exposes the same public API as hummingbot.logger (HummingbotLogger,
    INFO, NETWORK, log_encoder, ApplicationWarning, CLIHandler, StructLogger).
  - Consumers that previously caused the logger.py -> HummingbotApplication
    cycle now register two callback handlers at app startup:

        HummingbotLogger.register_notify_handler(app.notify)
        HummingbotLogger.register_network_handler(app.add_application_warning)

  - When no handler is registered (e.g. unit tests, embedded use), notify()
    and network() degrade to silent no-ops while standard logging still
    runs unconditionally.

Drop-in compatibility is therefore handled entirely by the
[tool.hummingbot.supersedes] table in pyproject.toml plus the registration
call wired into hummingbot.client.hummingbot_application.__init__. No
runtime shim is required in this layer.
"""

__all__: list[str] = []
