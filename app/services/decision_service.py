"""
Decision service.

Responsible for evaluating AI inference results.
"""

from app.contracts.decision_contract import DecisionServiceContract
from app.config.settings import settings
from app.domain.decision_result import DecisionResult
from app.domain.enums import PlantHealthStatus
from app.domain.inference_result import InferenceResult
from app.utils.logger import logger


class DecisionService(DecisionServiceContract):
    """
    Handles business decision evaluation.
    """

    def evaluate(
        self,
        inference_result: InferenceResult,
    ) -> DecisionResult:
        """
        Convert inference output into an actionable monitoring decision.
        """

        logger.info("6. Evaluating monitoring result...")

        status = inference_result.prediction
        confidence = inference_result.confidence

        should_alert = (
            status == PlantHealthStatus.POSSIBLE_NITROGEN_DEFICIENCY
            and confidence >= settings.decision.nitrogen_deficiency_threshold
        )

        if should_alert:
            reason = "Possible nitrogen deficiency detected with high confidence."
        elif status == PlantHealthStatus.POSSIBLE_NITROGEN_DEFICIENCY:
            reason = "Possible deficiency detected, but confidence is below the alert threshold."
        elif status == PlantHealthStatus.UNKNOWN:
            reason = "Insufficient visible vegetation for a reliable classification."
        else:
            reason = "Plant canopy appears healthy."

        return DecisionResult(
            health_status=status,
            should_alert=should_alert,
            reason=reason,
        )
