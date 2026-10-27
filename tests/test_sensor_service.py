
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

def test_sensor_service_preserves_raw_ph_voltage():
    hardware = MockSensorHardware(1.92)
    service = SensorService(hardware)

    result = service.read()

    assert result.soil_ph_raw_voltage == pytest.approx(1.92)


def test_sensor_service_calibrates_ph_within_range():
    hardware = MockSensorHardware(1.92)
    service = SensorService(hardware)

    result = service.read()

    assert result.soil_ph == pytest.approx(
        1.958 * 1.92 + 2.843
    )
    assert result.soil_ph_calibration_valid is True


def test_sensor_service_flags_ph_voltage_above_calibration_range():
    hardware = MockSensorHardware(3.50)
    service = SensorService(hardware)

    result = service.read()

    assert result.soil_ph_raw_voltage == pytest.approx(3.50)
    assert result.soil_ph_calibration_valid is False
    assert result.soil_ph is not None


@pytest.mark.parametrize(
    ("voltage", "expected_level"),
    [
        (2.50, "Air / sensor exposed"),
        (1.68, "Dry"),
        (1.03, "Moderate"),
        (0.92, "Wet / saturated"),
        (None, None),
    ],
)
def test_sensor_service_classifies_moisture(voltage, expected_level):
    hardware = MockSensorHardware(1.92)
    hardware.read = lambda: SensorReading(
        soil_moisture=voltage,
        soil_ph=1.92,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )
    service = SensorService(hardware)

    result = service.read()

    assert result.soil_moisture_level == expected_level
