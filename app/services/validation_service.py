
"""
Validation service.

Responsible for validating monitoring inputs.
"""

import cv2

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
        """

        logger.info("3. Validating monitoring inputs...")

        errors: list[str] = []

        # ==================================================
        # Image Validation
        # ==================================================

        if captured_image.path is None:
            errors.append(
                "Captured image path is missing."
            )

        elif not captured_image.path.exists():
            errors.append(
                "Captured image does not exist."
            )

        elif captured_image.path.stat().st_size == 0:
            errors.append(
                "Captured image is empty."
            )

        else:
            image = cv2.imread(str(captured_image.path))

            if image is None:
                errors.append(
                    "Captured image is not a valid image."
                )

        # ==================================================
        # Sensor Validation
        # ==================================================

        if sensor_reading.soil_moisture is None:
            errors.append(
                "Soil moisture reading is unavailable."
            )

        if sensor_reading.soil_ph is None:
            errors.append(
                "Soil pH reading is unavailable."
            )

        # ==================================================
        # Result
        # ==================================================

        if errors:
            logger.warning(
                "Validation failed with %d error(s).",
                len(errors),
            )

            for error in errors:
                logger.warning(error)

        else:
            logger.info(
                "Monitoring inputs validated successfully."
            )

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=tuple(errors),
        )
