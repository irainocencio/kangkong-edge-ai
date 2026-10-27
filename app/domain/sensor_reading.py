
"""
Sensor reading domain model.

Represents all sensor measurements collected during a monitoring cycle.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class SensorReading:
    """
    Represents raw sensor measurements and interpreted values.

    soil_moisture:
        Raw soil moisture voltage in volts.

    soil_ph:
        Estimated soil pH after calibration in the sensor service.
        For hardware readings, this field contains the raw pH voltage.

    soil_ph_raw_voltage:
        Raw pH sensor voltage preserved by the sensor service.

    soil_moisture_level:
        Interpreted moisture category, if available.

    soil_ph_calibration_valid:
        Whether the raw pH voltage is within the documented
        calibration range.
    """

    soil_moisture: float | None
    soil_ph: float | None
    temperature: float | None
    humidity: float | None
    timestamp: datetime

    soil_ph_raw_voltage: float | None = None
    soil_moisture_level: str | None = None
    soil_ph_calibration_valid: bool | None = None
