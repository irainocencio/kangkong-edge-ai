"""
Centralized logging configuration.
"""

import logging


def configure_logger() -> logging.Logger:
    """
    Configure and return the application's logger.
    """

    logger = logging.getLogger("EdgeAI")

    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = configure_logger()