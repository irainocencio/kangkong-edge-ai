"""
Hardware provider contract.

Provides access to all hardware implementations.
"""

from abc import ABC, abstractmethod

from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
)
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)


class HardwareProviderContract(ABC):
    """
    Contract for creating hardware implementations.
    """

    @abstractmethod
    def camera(self) -> CameraHardwareContract:
        """
        Return the camera hardware implementation.
        """
        raise NotImplementedError

    @abstractmethod
    def sensor(self) -> SensorHardwareContract:
        """
        Return the sensor hardware implementation.
        """
        raise NotImplementedError