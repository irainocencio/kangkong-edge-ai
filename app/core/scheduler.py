"""
Scheduler module.

Responsible for triggering monitoring cycles.
"""

import time

from app.config.settings import settings

from app.utils.logger import logger


class Scheduler:
    """
    Controls when monitoring cycles are executed.
    """

    def __init__(self, monitoring_manager):
        """
        Initialize the scheduler.

        Args:
            monitoring_manager: MonitoringManager instance.
        """
        self.monitoring_manager = monitoring_manager

    def run(self):
        """
        Execute one monitoring cycle.
        """

        logger.info("Scheduler started.")

        self.monitoring_manager.run_cycle()

        logger.info("Scheduler finished.")

    def run_forever(self) -> None:
        """Run monitoring cycles at the configured interval until interrupted."""

        interval_seconds = settings.monitoring.interval_minutes * 60
        logger.info(
            "Continuous scheduler started (interval: %s minute(s)).",
            settings.monitoring.interval_minutes,
        )
        while True:
            started_at = time.monotonic()
            try:
                self.monitoring_manager.run_cycle()
            except Exception:
                logger.exception("Monitoring cycle failed; the scheduler will continue.")
            elapsed = time.monotonic() - started_at
            time.sleep(max(0.0, interval_seconds - elapsed))
