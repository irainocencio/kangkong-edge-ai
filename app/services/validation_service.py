"""
Validation service.

Responsible for validating monitoring inputs.
"""

from app.contracts.validation_contract import ValidationServiceContract
from app.domain.captured_image import CapturedImage
from app.domain.sensor_reading import SensorReading
from app.domain.validation_result import ValidationResult
from app.utils.logger import logger


class ValidationService(ValidationServiceContract):
    """
    Handles validation of monitoring inputs.
    """

    def validate(
        self,
        captured_image: CapturedImage,
        sensor_reading: SensorReading,
    ) -> ValidationResult:
        """
        Validate monitoring inputs.

        Placeholder implementation.
        """

        logger.info("3. Validating monitoring inputs...")

        return ValidationResult(
            is_valid=True,
            errors=(),
        )