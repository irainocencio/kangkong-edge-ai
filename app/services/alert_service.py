"""
Alert service.

Responsible for evaluating and sending alerts.
"""

import json
from datetime import datetime, timedelta

from app.config.settings import settings

from app.contracts.alert_contract import AlertServiceContract
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class AlertService(AlertServiceContract):
    """
    Handles alert evaluation.
    """

    def __init__(self) -> None:
        self._last_alert_at: datetime | None = None

    def check(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Evaluate whether an alert should be sent.

        Write actionable alerts to an append-only JSON Lines outbox.
        """

        logger.info("9. Checking alerts...")

        if not monitoring_result.validation.is_valid:
            logger.warning(
                "Alert evaluation skipped because the "
                "monitoring result is invalid."
            )
            return

        if (
            not settings.alerts.enabled
            or not monitoring_result.decision.should_alert
        ):
            return

        now = datetime.now()
        cooldown = timedelta(minutes=settings.alerts.cooldown_minutes)
        if self._last_alert_at and now - self._last_alert_at < cooldown:
            logger.info("Alert suppressed during cooldown period.")
            return

        outbox = settings.storage.results_directory / "alerts.jsonl"
        outbox.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "created_at": now.isoformat(),
            "level": "warning",
            "health_status": monitoring_result.decision.health_status.value,
            "confidence": monitoring_result.inference.confidence,
            "reason": monitoring_result.decision.reason,
            "image": str(monitoring_result.captured_image.path),
        }
        with outbox.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload) + "\n")

        self._last_alert_at = now
        logger.warning("Alert queued: %s", monitoring_result.decision.reason)

        logger.debug(
            "Alert evaluation completed for monitoring "
            "cycle at %s.",
            monitoring_result.completed_at,
        )
