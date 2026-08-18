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

    def run(self, continuous: bool = False):
        """
        Execute the application.
        """

        self.lifecycle.startup()

        try:
            if continuous:
                self.scheduler.run_forever()
            else:
                self.scheduler.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.lifecycle.shutdown()
