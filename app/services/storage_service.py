"""
Storage service.

Responsible for persisting monitoring results.
"""

import json
import sqlite3
from dataclasses import asdict
from enum import Enum
from pathlib import Path

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
        Save a monitoring result as JSON and to SQLite.
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

        def serialize(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, Path):
                return str(value)
            return str(value)

        with output_path.open(
            mode="w",
            encoding="utf-8",
        ) as file:

            json.dump(
                asdict(monitoring_result),
                file,
                indent=4,
                default=serialize,
            )

        database_path = settings.storage.database_path
        database_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(database_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS monitoring_results (
                    completed_at TEXT PRIMARY KEY,
                    image_path TEXT NOT NULL,
                    soil_moisture REAL,
                    soil_ph REAL,
                    prediction TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    should_alert INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    result_path TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                INSERT OR REPLACE INTO monitoring_results VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    monitoring_result.completed_at.isoformat(),
                    str(monitoring_result.captured_image.path),
                    monitoring_result.sensor_reading.soil_moisture,
                    monitoring_result.sensor_reading.soil_ph,
                    monitoring_result.inference.prediction.value,
                    monitoring_result.inference.confidence,
                    int(monitoring_result.decision.should_alert),
                    monitoring_result.decision.reason,
                    str(output_path),
                ),
            )

        logger.info(
            "Monitoring result saved: %s and %s",
            output_path,
            database_path,
        )
