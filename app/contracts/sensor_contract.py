"""
Sensor service contract.

Defines the interface for sensor reading services.
"""

from abc import ABC, abstractmethod

from app.domain.sensor_reading import SensorReading


class SensorServiceContract(ABC):
    """
    Contract for sensor services.
    """

    @abstractmethod
    def read(self) -> SensorReading:
        """
        Read sensor values.

        Returns:
            SensorReading: The collected sensor data.
        """
        raise NotImplementedError