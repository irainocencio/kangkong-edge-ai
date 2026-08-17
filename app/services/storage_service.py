"""
Storage service.

Responsible for persisting monitoring results.
"""

import json
from dataclasses import asdict

from app.config.settings import settings
from app.contracts.storage_contract import (
    StorageServiceContract,
)
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class StorageService(StorageServiceContract):
    """
    Handles persistence of monitoring results.
    """

    def save(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Save a monitoring result as JSON.
        """

        logger.info("7. Saving monitoring result...")

        results_directory = (
            settings.storage.results_directory
        )

        results_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            monitoring_result.completed_at.strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".json"
        )

        output_path = results_directory / filename

        with output_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(monitoring_result),
                file,
                indent=4,
                default=str,
            )

        logger.info(
            "Monitoring result saved: %s",
            output_path,
        )