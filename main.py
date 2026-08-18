"""
Application entry point.

Starts the Edge AI Monitoring System.
"""

import argparse

from app.core.bootstrap import Bootstrap


def main():
    """
    Build and execute the application.
    """

    parser = argparse.ArgumentParser(description="Kangkong edge monitoring system")
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="run repeatedly using the configured monitoring interval",
    )
    args = parser.parse_args()

    bootstrap = Bootstrap()

    application = bootstrap.build()

    application.run(continuous=args.continuous)


if __name__ == "__main__":
    main()
