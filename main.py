"""
Application entry point.

Starts the Edge AI Monitoring System.
"""

from app.core.bootstrap import Bootstrap


def main():
    """
    Build and execute the application.
    """

    bootstrap = Bootstrap()

    application = bootstrap.build()

    application.run()


if __name__ == "__main__":
    main()