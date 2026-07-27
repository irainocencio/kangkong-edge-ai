"""
Mock camera hardware.

Provides a mock implementation of the camera hardware for
development and testing environments.
"""

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
        Simulate capturing an image.

        Creates an empty placeholder file.
        """

        output_path.touch(exist_ok=True)