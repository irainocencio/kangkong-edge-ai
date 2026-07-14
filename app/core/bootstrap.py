"""
Bootstrap module.

Responsible for constructing and wiring the application's
core components before execution.
"""

from app.core.application import Application
from app.core.lifecycle import Lifecycle
from app.core.scheduler import Scheduler
from app.core.monitoring_manager import MonitoringManager


class Bootstrap:
    """
    Builds and initializes the application's dependencies.
    """

    def __init__(self):
        """Initialize the bootstrap process."""
        pass

    def build(self):
        """
        Build and configure all application components.
        """

        lifecycle = Lifecycle()
        scheduler = Scheduler()
        monitoring_manager = MonitoringManager()

        application = Application(
            lifecycle=lifecycle,
            scheduler=scheduler,
            monitoring_manager=monitoring_manager
        )

        return application