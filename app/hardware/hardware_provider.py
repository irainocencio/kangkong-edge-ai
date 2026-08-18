"""
Hardware provider.

Selects the appropriate hardware implementations
for the current platform.
"""

import os
import platform

from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
)
from app.hardware.contracts.hardware_provider_contract import (
    HardwareProviderContract,
)
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)


class HardwareProvider(HardwareProviderContract):
    """
    Factory for hardware implementations.
    """

    @staticmethod
    def _use_raspberry_pi() -> bool:
        """Select hardware explicitly, with safe ARM Linux auto-detection."""

        mode = os.getenv("KANGKONG_HARDWARE", "auto").lower()
        if mode not in {"auto", "mock", "raspberry_pi"}:
            raise ValueError(
                "KANGKONG_HARDWARE must be auto, mock, or raspberry_pi"
            )
        if mode != "auto":
            return mode == "raspberry_pi"
        return platform.system() == "Linux" and platform.machine().lower() in {
            "armv7l",
            "aarch64",
            "arm64",
        }

    def camera(
        self,
    ) -> CameraHardwareContract:
        """
        Return the appropriate camera implementation.
        """

        if self._use_raspberry_pi():

            from app.hardware.raspberry_pi.picamera2_hardware import (
                PiCameraHardware,
            )

            return PiCameraHardware()

        from app.hardware.mock.mock_camera_hardware import (
            MockCameraHardware,
        )

        return MockCameraHardware()

    def sensor(
        self,
    ) -> SensorHardwareContract:
        """
        Return the appropriate sensor implementation.
        """

        if self._use_raspberry_pi():

            from app.hardware.raspberry_pi.ads1115_sensor_hardware import (
                ADS1115SensorHardware,
            )

            return ADS1115SensorHardware()

        from app.hardware.mock.mock_sensor_hardware import (
            MockSensorHardware,
        )

        return MockSensorHardware()
