"""
Raspberry Pi camera hardware implementation.

Uses Picamera2 to capture images from the CSI camera.
"""

from pathlib import Path

from picamera2 import Picamera2

from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
)


class PiCameraHardware(CameraHardwareContract):
    """
    Raspberry Pi camera implementation using Picamera2.
    """

    def __init__(self) -> None:
        """
        Initialize the Raspberry Pi camera.
        """

        self.camera = Picamera2()

        configuration = self.camera.create_still_configuration()

        self.camera.configure(configuration)

        self.camera.start()

    def capture_image(
        self,
        output_path: Path,
    ) -> None:
        """
        Capture an image and save it to disk.
        """

        self.camera.capture_file(str(output_path))