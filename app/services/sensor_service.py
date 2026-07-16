"""
Sensor service.

Responsible for reading sensor values.
"""

from datetime import datetime

from app.contracts.sensor_contract import SensorServiceContract
from app.domain.sensor_reading import SensorReading
from app.utils.logger import logger


class SensorService(SensorServiceContract):
    """
    Handles sensor data acquisition.
    """

    def read(self) -> SensorReading:
        """
        Read sensor values.

        Placeholder implementation.
        """

        logger.info("2. Reading sensors...")

        return SensorReading(
            soil_moisture=0.0,
            soil_ph=0.0,
            temperature=None,
            humidity=None,
            timestamp=datetime.now(),
        )