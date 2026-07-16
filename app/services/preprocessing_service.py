"""
Preprocessing service.

Responsible for preprocessing captured images.
"""

from pathlib import Path

from app.contracts.preprocessing_contract import PreprocessingServiceContract
from app.domain.captured_image import CapturedImage
from app.domain.preprocessing_result import PreprocessingResult
from app.utils.logger import logger


class PreprocessingService(PreprocessingServiceContract):
    """
    Handles image preprocessing.
    """

    def process(
        self,
        captured_image: CapturedImage,
    ) -> PreprocessingResult:
        """
        Preprocess a captured image.

        Placeholder implementation.
        """

        logger.info("4. Preprocessing image...")

        return PreprocessingResult(
            processed_image_path=Path("processed_placeholder.jpg"),
            metadata={},
        )