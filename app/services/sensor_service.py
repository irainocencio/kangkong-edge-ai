
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


PH_CALIBRATION_MIN_VOLTAGE = 0.66
PH_CALIBRATION_MAX_VOLTAGE = 3.30


class SensorService(SensorServiceContract):
    """Handles sensor data acquisition and calibration."""

    def __init__(
        self,
        hardware: SensorHardwareContract,
    ) -> None:
        self._hardware = hardware
        logger.info("Sensor service initialized.")

    @staticmethod
    def _classify_moisture(
        voltage: float | None,
    ) -> str | None:
        """Classify moisture using the observed calibration points."""

        if voltage is None:
            return None

        if voltage >= 2.40:
            return "Air / sensor exposed"

        if voltage > 1.35:
            return "Dry"

        if voltage > 0.98:
            return "Moderate"

        return "Wet / saturated"

    def read(self) -> SensorReading:
        """Read raw sensor voltages and derive interpreted values."""

        logger.info("2. Reading sensors...")

        raw_reading = self._hardware.read()
        raw_ph_voltage = raw_reading.soil_ph

        calibrated_ph = (
            1.958 * raw_ph_voltage + 2.843
            if raw_ph_voltage is not None
            else None
        )

        ph_calibration_valid = (
            PH_CALIBRATION_MIN_VOLTAGE
            <= raw_ph_voltage
            <= PH_CALIBRATION_MAX_VOLTAGE
            if raw_ph_voltage is not None
            else None
        )

        moisture_level = self._classify_moisture(
            raw_reading.soil_moisture
        )

        logger.info(
            "Soil moisture voltage: %s",
            raw_reading.soil_moisture,
        )
        logger.info("Soil moisture category: %s", moisture_level)
        logger.info("Raw soil pH voltage: %s", raw_ph_voltage)
        logger.info("Estimated soil pH: %s", calibrated_ph)
        logger.info(
            "pH calibration range valid: %s",
            ph_calibration_valid,
        )

        return SensorReading(
            soil_moisture=raw_reading.soil_moisture,
            soil_ph=calibrated_ph,
            temperature=raw_reading.temperature,
            humidity=raw_reading.humidity,
            timestamp=raw_reading.timestamp,
            soil_ph_raw_voltage=raw_ph_voltage,
            soil_moisture_level=moisture_level,
            soil_ph_calibration_valid=ph_calibration_valid,
        )
