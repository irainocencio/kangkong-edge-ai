"""
ADS1115 sensor hardware.

Reads sensor values from the ADS1115 ADC.
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
        Read all sensors.

        Temporary implementation.
        """

        moisture = self._moisture_channel.voltage
        ph = self._ph_channel.voltage

        return SensorReading(
            soil_moisture=moisture,
            soil_ph=ph,
            temperature=None,
            humidity=None,
            timestamp=datetime.now(),
        )