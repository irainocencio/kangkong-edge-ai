"""
Preprocessing service.

Responsible for preprocessing captured images.
"""

from pathlib import Path

import cv2

from app.config.settings import settings
from app.contracts.preprocessing_contract import (
    PreprocessingServiceContract,
)
from app.domain.captured_image import CapturedImage
from app.domain.preprocessing_result import (
    PreprocessingResult,
)
from app.utils.logger import logger


class PreprocessingService(
    PreprocessingServiceContract,
):
    """
    Handles image preprocessing.
    """

    def process(
        self,
        captured_image: CapturedImage,
    ) -> PreprocessingResult:
        """
        Load, resize, and save the captured image.

        Returns:
            PreprocessingResult: Information about the
            processed image.
        """

        logger.info("4. Preprocessing image...")

        # Ensure output directory exists
        processed_directory = (
            settings.storage.processed_images_directory
        )

        processed_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Load image
        image = cv2.imread(
            str(captured_image.path),
        )

        if image is None:
            raise ValueError(
                f"Unable to load image: {captured_image.path}"
            )

        # Resize image
        resized_image = cv2.resize(
            image,
            (
                settings.camera.width,
                settings.camera.height,
            ),
        )

        # Generate processed filename
        output_path = (
            processed_directory
            / captured_image.path.name
        )

        # Save processed image
        saved = cv2.imwrite(
            str(output_path),
            resized_image,
        )

        if not saved:
            raise OSError(
                f"Unable to save processed image: {output_path}"
            )

        logger.info(
            "Processed image saved: %s",
            output_path,
        )

        return PreprocessingResult(
            processed_image_path=output_path,
            metadata={
                "width": str(
                    settings.camera.width,
                ),
                "height": str(
                    settings.camera.height,
                ),
                "format": settings.camera.image_format,
            },
        )
