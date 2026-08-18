"""Tests for environment-aware hardware selection."""

from app.hardware.hardware_provider import HardwareProvider
from app.hardware.mock.mock_camera_hardware import MockCameraHardware
from app.hardware.mock.mock_sensor_hardware import MockSensorHardware


def test_explicit_mock_hardware(monkeypatch):
    monkeypatch.setenv("KANGKONG_HARDWARE", "mock")
    provider = HardwareProvider()

    assert isinstance(provider.camera(), MockCameraHardware)
    assert isinstance(provider.sensor(), MockSensorHardware)


def test_invalid_hardware_mode(monkeypatch):
    monkeypatch.setenv("KANGKONG_HARDWARE", "invalid")

    try:
        HardwareProvider().camera()
    except ValueError as error:
        assert "KANGKONG_HARDWARE" in str(error)
    else:
        raise AssertionError("Invalid hardware mode should fail")
