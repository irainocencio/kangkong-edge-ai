"""
Decision service.

Responsible for evaluating AI inference results.
"""

from app.contracts.decision_contract import DecisionServiceContract
from app.domain.decision_result import DecisionResult
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
        Evaluate AI inference.

        Placeholder implementation.
        """

        logger.info("6. Evaluating monitoring result...")

        return DecisionResult(
            health_status=inference_result.prediction,
            should_alert=False,
            reason="Placeholder implementation",
        )