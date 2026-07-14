"""
Lifecycle module.

Responsible for managing the application's startup
and shutdown procedures.
"""

from app.utils.logger import logger


class Lifecycle:
    """
    Manages application startup and shutdown.
    """

    def __init__(self):
        """Initialize the lifecycle manager."""
        pass

    def startup(self):
        """
        Execute the application startup sequence.
        """

        logger.info("=" * 40)
        logger.info("Starting Edge AI Monitoring System...")
        logger.info("Application startup complete.")
        logger.info("=" * 40)

    def shutdown(self):
        """
        Execute the application shutdown sequence.
        """

        logger.info("=" * 40)
        logger.info("Shutting down Edge AI Monitoring System...")
        logger.info("Shutdown complete.")
        logger.info("=" * 40)