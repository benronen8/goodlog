# goodlog

Structured JSON logging for Python — configure once, log everywhere.

## Install

```bash
pip install goodlog
```

## Quick start

```python
import goodlog

# Configure logging once at application startup
goodlog.configure_logging(global_extra_info={"service": "my-app"})

# Create a logger and use it
logger = goodlog.create_logger(__name__)
logger.info("Application started")
```

Logs are emitted as JSON to stdout:

```json
{"logger_name": "__main__", "timestamp": "2025-01-01 12:00:00,000", "log_level": "INFO", "message": "Application started", "extra_info": {"service": "my-app"}, ...}
```

## Adding contextual info

Use `add()` / `remove()` or the `ephemeral_info_context` context manager to attach extra fields to all logs within a scope:

```python
import goodlog

goodlog.configure_logging()
logger = goodlog.create_logger(__name__)

# Manually add/remove
goodlog.add(request_id="abc-123")
logger.info("Processing request")
goodlog.remove()

# Or use the context manager
with goodlog.ephemeral_info_context(user_id=42):
    logger.info("User action")  # includes user_id in extra_info
```

## Links

- Source: https://github.com/benronen8/goodlog
- Docs: https://benronen8.github.io/goodlog
