"""
Dashboard service.

Responsible for updating the monitoring dashboard.
"""

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
        Publish the latest monitoring result.

        The dashboard implementation will be added
        during the presentation layer development.
        """

        logger.info("8. Updating dashboard...")

        logger.debug(
            "Dashboard update prepared for monitoring "
            "cycle completed at %s",
            monitoring_result.completed_at,
        )