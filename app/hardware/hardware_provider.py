"""
Hardware provider.

Selects the appropriate hardware implementations
for the current platform.
"""

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

    def camera(
        self,
    ) -> CameraHardwareContract:
        """
        Return the appropriate camera implementation.
        """

        if platform.system() == "Linux":

            from app.hardware.raspberry_pi.pi_camera_hardware import (
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

        if platform.system() == "Linux":

            from app.hardware.raspberry_pi.ads1115_sensor_hardware import (
                ADS1115SensorHardware,
            )

            return ADS1115SensorHardware()

        from app.hardware.mock.mock_sensor_hardware import (
            MockSensorHardware,
        )

        return MockSensorHardware()