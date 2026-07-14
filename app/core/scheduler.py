"""
Scheduler module.

Responsible for triggering monitoring cycles.
"""

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
        Execute one scheduled monitoring cycle.

        This is currently a placeholder implementation.
        Future versions will execute according to the
        configured monitoring interval.
        """

        logger.info("Scheduler started.")

        self.monitoring_manager.run_cycle()

        logger.info("Scheduler finished.")