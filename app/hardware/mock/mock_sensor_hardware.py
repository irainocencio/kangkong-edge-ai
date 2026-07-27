"""
Mock sensor hardware.

Used during Windows development.
"""

from datetime import datetime

from app.domain.sensor_reading import SensorReading
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)


class MockSensorHardware(SensorHardwareContract):
    """
    Mock implementation for sensor hardware.
    """

    def read(self) -> SensorReading:

        return SensorReading(
            soil_moisture=0.0,
            soil_ph=0.0,
            temperature=None,
            humidity=None,
            timestamp=datetime.now(),
        )