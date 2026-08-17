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

        Notification providers will be integrated
        after the decision logic has been completed.
        """

        logger.info("9. Checking alerts...")

        if not monitoring_result.validation.is_valid:
            logger.warning(
                "Alert evaluation skipped because the "
                "monitoring result is invalid."
            )
            return

        logger.debug(
            "Alert evaluation completed for monitoring "
            "cycle at %s.",
            monitoring_result.completed_at,
        )