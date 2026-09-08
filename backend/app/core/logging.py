import json
import logging
import sys
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps(
            {
                "timestamp": datetime.now(UTC).isoformat(),
                "level": record.levelname,
                "event": record.getMessage(),
                "request_id": getattr(record, "request_id", None),
                "method": getattr(record, "method", None),
                "route": getattr(record, "route", None),
                "status": getattr(record, "status", None),
                "duration_ms": getattr(record, "duration_ms", None),
            }
        )


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("inventory.http")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
    logger.propagate = False
    return logger
