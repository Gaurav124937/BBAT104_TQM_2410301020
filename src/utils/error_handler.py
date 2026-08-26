from __future__ import annotations
import logging

logger=logging.getLogger("library_app")

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

def log_exception(context: str, exc: Exception) -> None:
    logger.exception("%s: %s", context, exc)

def user_error_message(exc: Exception) -> str:
    message=str(exc).strip()
    return message or "The operation could not be completed."
