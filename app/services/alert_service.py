"""
Alert service.

Responsible for evaluating and sending alerts.
"""

from app.contracts.alert_contract import AlertServiceContract
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class AlertService(AlertServiceContract):
    """
    Handles alert evaluation.
    """

    def check(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Evaluate whether an alert should be sent.

        Placeholder implementation.
        """

        logger.info("9. Checking alerts...")