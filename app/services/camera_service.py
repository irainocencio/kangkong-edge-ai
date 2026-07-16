"""
Camera service.

Responsible for capturing images from the camera.
"""

from datetime import datetime
from pathlib import Path

from app.contracts.camera_contract import CameraServiceContract
from app.domain.captured_image import CapturedImage
from app.utils.logger import logger


class CameraService(CameraServiceContract):
    """
    Handles image acquisition.
    """

    def capture(self) -> CapturedImage:
        """
        Capture an image.

        Placeholder implementation.
        """

        logger.info("1. Capturing image...")

        return CapturedImage(
            path=Path("placeholder.jpg"),
            timestamp=datetime.now(),
            width=0,
            height=0,
        )