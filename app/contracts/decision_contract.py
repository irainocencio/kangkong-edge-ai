"""
Decision service contract.

Defines the interface for decision services.
"""

from abc import ABC, abstractmethod

from app.domain.decision_result import DecisionResult
from app.domain.inference_result import InferenceResult


class DecisionServiceContract(ABC):
    """
    Contract for decision services.
    """

    @abstractmethod
    def evaluate(
        self,
        inference_result: InferenceResult,
    ) -> DecisionResult:
        """
        Evaluate the AI inference.

        Returns:
            DecisionResult: The business decision.
        """
        raise NotImplementedError