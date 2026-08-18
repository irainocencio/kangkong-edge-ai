"""
Dashboard service.

Responsible for updating the monitoring dashboard.
"""

import json
from dataclasses import asdict
from enum import Enum
from pathlib import Path

from app.config.settings import settings

from app.contracts.dashboard_contract import (
    DashboardServiceContract,
)
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class DashboardService(
    DashboardServiceContract,
):
    """
    Handles dashboard updates.
    """

    def update(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Publish the latest monitoring result as dashboard-ready JSON.
        """

        logger.info("8. Updating dashboard...")

        output_path = settings.storage.results_directory / "latest.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)

        def serialize(value):
            if isinstance(value, Enum):
                return value.value
            if isinstance(value, Path):
                return str(value)
            return str(value)

        output_path.write_text(
            json.dumps(asdict(monitoring_result), indent=2, default=serialize),
            encoding="utf-8",
        )
        logger.info("Dashboard data updated: %s", output_path)
