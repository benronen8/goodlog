from logging.config import dictConfig
from typing import Any

from .extra_info import set_info


def configure_logging(
        extra_info: dict[str, Any] = None,
) -> None:
    if extra_info is None:
        extra_info = {}
    set_info(**extra_info)
    dictConfig(
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