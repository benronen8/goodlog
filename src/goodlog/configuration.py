from logging.config import dictConfig as _configure_logging
from typing import Any

from .extra_info import set_info


def configure_logging(
        extra_info: dict[str, Any],
) -> None:
    set_info(**extra_info)

    _configure_logging(
        config={
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "json_formatter": {
                    "()": "goodlog.formats.JSONFormatter",
                }
            },
            "handlers": {
                "stdout": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "formatter": "json_formatter",
                    "filters": ["context"],
                }
            },
            "filters": {
                "context": {
                    "()": "goodlog.filters.ContextFilter"
                },
            },
            "root": {
                "handlers": ["stdout"],
                "level": "INFO",
            },
        }
    )