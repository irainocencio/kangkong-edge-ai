"""
Inference service contract.

Defines the interface for AI inference services.
"""

from abc import ABC, abstractmethod

from app.domain.inference_result import InferenceResult
from app.domain.preprocessing_result import PreprocessingResult


class InferenceServiceContract(ABC):
    """
    Contract for inference services.
    """

    @abstractmethod
    def predict(
        self,
        preprocessing_result: PreprocessingResult,
    ) -> InferenceResult:
        """
        Run AI inference.

        Returns:
            InferenceResult: The AI inference result.
        """
        raise NotImplementedError