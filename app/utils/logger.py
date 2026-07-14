"""
Centralized logging configuration.

Provides a shared logger instance for the entire
Edge AI Monitoring System.
"""

import logging

from app.config.settings import LOG_FILE, LOG_LEVEL


def configure_logger() -> logging.Logger:
    """
    Configure and return the application's logger.
    """

    logger = logging.getLogger("EdgeAI")

    # Prevent duplicate handlers if imported multiple times
    if logger.hasHandlers():
        return logger

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    # Ensure the log directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = configure_logger()