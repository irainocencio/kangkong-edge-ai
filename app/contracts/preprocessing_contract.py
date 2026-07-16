"""
Preprocessing service contract.

Defines the interface for preprocessing services.
"""

from abc import ABC, abstractmethod

from app.domain.captured_image import CapturedImage
from app.domain.preprocessing_result import PreprocessingResult


class PreprocessingServiceContract(ABC):
    """
    Contract for preprocessing services.
    """

    @abstractmethod
    def process(
        self,
        captured_image: CapturedImage,
    ) -> PreprocessingResult:
        """
        Preprocess a captured image.

        Returns:
            PreprocessingResult: The preprocessing result.
        """
        raise NotImplementedError