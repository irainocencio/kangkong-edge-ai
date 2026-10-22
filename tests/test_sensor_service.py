
"""Tests for sensor reading and calibration."""

from datetime import datetime

import pytest

from app.domain.sensor_reading import SensorReading
from app.services.sensor_service import SensorService


class MockSensorHardware:
    """Provides controlled sensor readings for testing."""

    def __init__(self, soil_ph):
        self.soil_ph = soil_ph

    def read(self) -> SensorReading:
        return SensorReading(
            soil_moisture=0.0,
            soil_ph=self.soil_ph,
            temperature=None,
            humidity=None,
            timestamp=datetime.now(),
        )


@pytest.mark.parametrize(
    ("raw_ph", "expected_ph"),
    [
        (0.0, 2.843),
        (1.0, 4.801),
        (None, None),
    ],
)
def test_sensor_service_calibrates_ph(raw_ph, expected_ph):
    hardware = MockSensorHardware(raw_ph)
    service = SensorService(hardware)

    result = service.read()

    if expected_ph is None:
        assert result.soil_ph is None
    else:
        assert result.soil_ph == pytest.approx(expected_ph)
