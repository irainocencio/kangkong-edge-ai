"""
Sensor hardware contract.

Defines the interface for physical sensor hardware.
"""

from abc import ABC, abstractmethod

from app.domain.sensor_reading import SensorReading


class SensorHardwareContract(ABC):
    """
    Contract for sensor hardware implementations.
    """

    @abstractmethod
    def read(self) -> SensorReading:
        """
        Read all available sensor values.
        """
        raise NotImplementedError