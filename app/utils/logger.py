"""
Centralized logging configuration.
"""

import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_DIR = PROJECT_ROOT / "logs"


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

    # Ensure logs directory exists
    LOGS_DIR.mkdir(exist_ok=True)

    # Console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File output
    file_handler = logging.FileHandler(
        LOGS_DIR / "application.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = configure_logger()