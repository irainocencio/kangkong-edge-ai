"""
Application module.

Coordinates the application's lifecycle and delegates
monitoring execution to the scheduler.
"""


class Application:
    """
    Main application class.
    """

    def __init__(self, lifecycle, scheduler):
        """
        Initialize the application.

        Args:
            lifecycle: Lifecycle manager.
            scheduler: Scheduler instance.
        """

        self.lifecycle = lifecycle
        self.scheduler = scheduler

    def run(self):
        """
        Execute the application.
        """

        self.lifecycle.startup()

        self.scheduler.run()

        self.lifecycle.shutdown()