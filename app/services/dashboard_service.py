"""
Dashboard service.

Responsible for updating the monitoring dashboard.
"""

from app.contracts.dashboard_contract import DashboardServiceContract
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class DashboardService(DashboardServiceContract):
    """
    Handles dashboard updates.
    """

    def update(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Update the dashboard.

        Placeholder implementation.
        """

        logger.info("8. Updating dashboard...")