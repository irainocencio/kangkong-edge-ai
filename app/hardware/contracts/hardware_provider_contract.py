"""
Hardware provider contract.

Provides access to all hardware implementations.
"""

from abc import ABC, abstractmethod

from app.hardware.contracts.camera_hardware_contract import (
    CameraHardwareContract,
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