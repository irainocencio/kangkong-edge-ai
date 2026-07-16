"""
Sensor reading domain model.

Represents all sensor measurements collected during a monitoring cycle.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class SensorReading:
    """
    Represents the sensor values collected during a monitoring cycle.
    """

    soil_moisture: float | None
    soil_ph: float | None
    temperature: float | None
    humidity: float | None
    timestamp: datetime