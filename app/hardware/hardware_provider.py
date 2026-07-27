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


class HardwareProvider(HardwareProviderContract):
    """
    Factory for hardware implementations.
    """

    def camera(
        self,
    ) -> CameraHardwareContract:
        """
        Return the appropriate camera hardware implementation.
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