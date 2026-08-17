"""
Sensor service.

Responsible for reading and calibrating sensor values.
"""

from app.contracts.sensor_contract import SensorServiceContract
from app.domain.sensor_reading import SensorReading
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)
from app.utils.logger import logger


class SensorService(SensorServiceContract):
    """
    Handles sensor data acquisition and calibration.
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
        Read and calibrate sensor values.
        """

        logger.info("2. Reading sensors...")

        # Read raw sensor voltages
        reading = self._hardware.read()

        # Calibrate soil pH
        calibrated_ph = (
            1.958 * reading.soil_ph + 2.843
            if reading.soil_ph is not None
            else None
        )

        logger.info(
            "Soil Moisture Voltage: %.3f V",
            reading.soil_moisture,
        )

        logger.info(
            "Soil pH Voltage: %.3f V",
            reading.soil_ph,
        )

        logger.info(
            "Calibrated Soil pH: %.2f",
            calibrated_ph,
        )

        return SensorReading(
            soil_moisture=reading.soil_moisture,
            soil_ph=calibrated_ph,
            temperature=reading.temperature,
            humidity=reading.humidity,
            timestamp=reading.timestamp,
        )