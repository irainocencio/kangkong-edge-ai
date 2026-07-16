"""
Tests for the MonitoringManager.
"""

from app.core.bootstrap import Bootstrap


def test_monitoring_cycle_runs_without_errors():
    """
    The monitoring cycle should execute without raising exceptions.
    """

    application = Bootstrap().build()

    application.scheduler.run()