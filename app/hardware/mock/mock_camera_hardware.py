"""
Mock camera hardware.

Provides a mock implementation of the camera hardware for
development and testing environments.
"""

import base64
from pathlib import Path

from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
)


class MockCameraHardware(CameraHardwareContract):
    """
    Mock camera implementation.
    """

    def capture_image(
        self,
        output_path: Path,
    ) -> None:
        """
        Simulate capturing a valid image.

        A small embedded PNG keeps the mock independent of OpenCV and
        camera drivers while still allowing validation and preprocessing
        to exercise the complete monitoring pipeline.
        """

        image_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2"
            "AAAAFklEQVR4nGPQ2KJBEmIY1TCqYfhqAAA6YgQQV0N9"
            "IQAAAABJRU5ErkJggg=="
        )

        output_path.write_bytes(image_bytes)
