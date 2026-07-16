"""
Tests for the Bootstrap composition root.
"""

from app.core.bootstrap import Bootstrap
from app.core.application import Application


def test_bootstrap_build_returns_application():
    """
    Bootstrap should construct an Application instance.
    """

    bootstrap = Bootstrap()

    application = bootstrap.build()

    assert isinstance(application, Application)


def test_bootstrap_build_is_not_none():
    """
    Bootstrap should always return a valid application.
    """

    bootstrap = Bootstrap()

    application = bootstrap.build()

    assert application is not None


def test_application_has_scheduler():
    """
    Built application should contain a scheduler.
    """

    application = Bootstrap().build()

    assert application.scheduler is not None


def test_application_has_lifecycle():
    """
    Built application should contain a lifecycle manager.
    """

    application = Bootstrap().build()

    assert application.lifecycle is not None