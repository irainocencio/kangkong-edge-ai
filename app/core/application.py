"""
Application module.

Contains the top-level Application class responsible for
managing the lifecycle of the Edge AI Monitoring System.
"""

from app.core.lifecycle import Lifecycle
from app.core.scheduler import Scheduler
from app.core.monitoring_manager import MonitoringManager


class Application:
    """
    Represents the entire monitoring application.
    """

    def __init__(
        self,
        lifecycle: Lifecycle,
        scheduler: Scheduler,
        monitoring_manager: MonitoringManager
    ):
        """
        Initialize the application with its core components.
        """

        self.lifecycle = lifecycle
        self.scheduler = scheduler
        self.monitoring_manager = monitoring_manager

    def start(self):
        """
        Start the application.
        """

        self.lifecycle.startup()

        # Temporary implementation:
        # Execute one monitoring cycle manually.
        self.monitoring_manager.run_cycle()

    def stop(self):
        """
        Stop the application.
        """

        self.lifecycle.shutdown()