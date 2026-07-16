"""
Inference service.

Responsible for running AI inference.
"""

from datetime import datetime

from app.contracts.inference_contract import InferenceServiceContract
from app.domain.enums import PlantHealthStatus
from app.domain.inference_result import InferenceResult
from app.domain.preprocessing_result import PreprocessingResult
from app.utils.logger import logger


class InferenceService(InferenceServiceContract):
    """
    Handles AI inference.
    """

    def predict(
        self,
        preprocessing_result: PreprocessingResult,
    ) -> InferenceResult:
        """
        Run AI inference.

        Placeholder implementation.
        """

        logger.info("5. Running AI inference...")

        return InferenceResult(
            prediction=PlantHealthStatus.HEALTHY,
            confidence=1.0,
            model_version="placeholder",
            timestamp=datetime.now(),
        )