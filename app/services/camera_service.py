"""
Camera service.

Responsible for capturing images.
"""

from datetime import datetime

import cv2

from app.config.settings import settings
from app.contracts.camera_contract import CameraServiceContract
from app.domain.captured_image import CapturedImage
from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
)
from app.utils.logger import logger


class CameraService(CameraServiceContract):
    """
    Handles image acquisition.
    """

    def __init__(
        self,
        hardware: CameraHardwareContract,
    ) -> None:
        """
        Initialize the camera service.
        """

        self._hardware = hardware

        logger.info("Camera service initialized.")

    def capture(self) -> CapturedImage:
        """
        Capture an image and return its metadata.
        """

        logger.info("1. Capturing image...")

        # Generate timestamp
        timestamp = datetime.now()

        # Ensure the output directory exists
        raw_images_directory = (
            settings.storage.raw_images_directory
        )

        raw_images_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Generate image filename
        filename = (
            f"image_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
        )

        image_path = raw_images_directory / filename

        # Capture the image using the hardware implementation
        self._hardware.capture_image(image_path)

        # Read actual image dimensions
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(
                f"Unable to load captured image: {image_path}"
            )

        height, width = image.shape[:2]

        logger.info(
            "Image capture completed: %s",
            image_path,
        )

        # Build the domain model
        return CapturedImage(
            path=image_path,
            timestamp=timestamp,
            width=width,
            height=height,
        )
