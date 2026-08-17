"""
ADS1115 sensor hardware.

Reads raw sensor voltages from the ADS1115 ADC.
"""

from datetime import datetime

import adafruit_ads1x15.ads1115 as ADS
import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn

from app.domain.sensor_reading import SensorReading
from app.hardware.contracts.sensor_hardware_contract import (
    SensorHardwareContract,
)
from app.utils.logger import logger


class ADS1115SensorHardware(SensorHardwareContract):
    """
    Raspberry Pi implementation for the ADS1115.

    This class is responsible only for acquiring raw sensor
    voltages from the ADC. Calibration and interpretation
    are handled by SensorService.
    """

    def __init__(self) -> None:
        """
        Initialize the ADS1115 and sensor channels.
        """

        logger.info("Initializing ADS1115...")

        i2c = busio.I2C(
            board.SCL,
            board.SDA,
        )

        ads = ADS.ADS1115(i2c)

        self._moisture_channel = AnalogIn(
            ads,
            ADS.P0,
        )

        self._ph_channel = AnalogIn(
            ads,
            ADS.P1,
        )

        logger.info("ADS1115 initialized successfully.")

    def read(self) -> SensorReading:
        """
        Read the raw sensor voltages.

        Returns:
            SensorReading: Raw voltage readings acquired from
            the ADS1115. These values are not yet calibrated.
        """

        moisture_voltage = self._moisture_channel.voltage
        ph_voltage = self._ph_channel.voltage

        logger.debug(
            "Raw sensor readings | Moisture: %.3f V | pH: %.3f V",
            moisture_voltage,
            ph_voltage,
        )

        return SensorReading(
            soil_moisture=moisture_voltage,
            soil_ph=ph_voltage,
            temperature=None,
            humidity=None,
            timestamp=datetime.now(),
        )