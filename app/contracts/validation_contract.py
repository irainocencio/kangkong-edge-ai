"""
Validation service contract.

Defines the interface for validation services.
"""

from abc import ABC, abstractmethod

from app.domain.captured_image import CapturedImage
from app.domain.sensor_reading import SensorReading
from app.domain.validation_result import ValidationResult


class ValidationServiceContract(ABC):
    """
    Contract for validation services.
    """

    @abstractmethod
    def validate(
        self,
        captured_image: CapturedImage,
        sensor_reading: SensorReading,
    ) -> ValidationResult:
        """
        Validate monitoring inputs.

        Returns:
            ValidationResult: The validation result.
        """
        raise NotImplementedError