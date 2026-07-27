"""
Sensor service.

Responsible for reading sensor values.
"""

from app.contracts.sensor_contract import SensorServiceContract
from app.domain.sensor_reading import SensorReading
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)
from app.utils.logger import logger


class SensorService(SensorServiceContract):
    """
    Handles sensor data acquisition.
    """

    def __init__(
        self,
        hardware: SensorHardwareContract,
    ) -> None:
        """
        Initialize the sensor service.
        """

        self._hardware = hardware

        logger.info("Sensor service initialized.")

    def read(self) -> SensorReading:
        """
        Read sensor values.
        """

        logger.info("2. Reading sensors...")

        return self._hardware.read()