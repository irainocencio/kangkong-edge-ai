"""
Main entry point for the Edge AI Monitoring System.
"""

from app.core.bootstrap import Bootstrap


def main():
    """
    Application entry point.
    """

    bootstrap = Bootstrap()
    application = bootstrap.build()

    application.start()
    application.stop()


if __name__ == "__main__":
    main()