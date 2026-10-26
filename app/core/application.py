"""
Application module.

Coordinates the application's lifecycle and monitoring components.
"""


class Application:
    """Main application class."""

    def __init__(
        self,
        lifecycle,
        scheduler,
        monitoring_manager,
        monitoring_controller,
    ):
        """Initialize the application and its core components.

        Args:
            lifecycle: Lifecycle manager.
            scheduler: Scheduler instance.
            monitoring_manager: Monitoring workflow coordinator.
            monitoring_controller: Controller for manual monitoring cycles.
        """
        self.lifecycle = lifecycle
        self.scheduler = scheduler
        self.monitoring_manager = monitoring_manager
        self.monitoring_controller = monitoring_controller

    def run(self, continuous: bool = False):
        """Execute the application."""
        self.lifecycle.startup()

        try:
            if continuous:
                self.scheduler.run_forever()
            else:
                self.scheduler.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.monitoring_controller.shutdown()
            self.lifecycle.shutdown()
