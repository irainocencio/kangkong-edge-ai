
"""Tests for monitoring input validation."""

from datetime import datetime

import cv2
import numpy as np

from app.domain.captured_image import CapturedImage
from app.domain.sensor_reading import SensorReading
from app.services.validation_service import ValidationService


def create_valid_image(image_path):
    """Create a valid JPEG image for validation tests."""

    image = np.zeros((480, 640, 3), dtype=np.uint8)
    success = cv2.imwrite(str(image_path), image)

    assert success is True
    return image_path


def test_valid_inputs_pass_validation(tmp_path):
    """Existing image and available sensor readings should be valid."""

    image_path = tmp_path / "plant.jpg"
    create_valid_image(image_path)

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=1.2,
        soil_ph=5.1,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is True
    assert result.errors == ()


def test_missing_image_fails_validation(tmp_path):
    """A nonexistent image path should fail validation."""

    image_path = tmp_path / "missing.jpg"

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=1.2,
        soil_ph=5.1,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Captured image does not exist." in result.errors


def test_empty_image_fails_validation(tmp_path):
    """An empty image file should fail validation."""

    image_path = tmp_path / "empty.jpg"
    image_path.write_bytes(b"")

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=1.2,
        soil_ph=5.1,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Captured image is empty." in result.errors


def test_missing_soil_moisture_fails_validation(tmp_path):
    """Missing soil moisture should fail validation."""

    image_path = tmp_path / "plant.jpg"
    create_valid_image(image_path)

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=None,
        soil_ph=5.1,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Soil moisture reading is unavailable." in result.errors


def test_missing_soil_ph_fails_validation(tmp_path):
    """Missing soil pH should fail validation."""

    image_path = tmp_path / "plant.jpg"
    create_valid_image(image_path)

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=1.2,
        soil_ph=None,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Soil pH reading is unavailable." in result.errors


def test_both_missing_sensor_readings_are_reported(tmp_path):
    """Both missing required readings should be reported."""

    image_path = tmp_path / "plant.jpg"
    create_valid_image(image_path)

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=None,
        soil_ph=None,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Soil moisture reading is unavailable." in result.errors
    assert "Soil pH reading is unavailable." in result.errors
    assert len(result.errors) == 2


def test_corrupted_image_fails_validation(tmp_path):
    """A nonempty but undecodable image should fail validation."""

    image_path = tmp_path / "corrupted.jpg"
    image_path.write_bytes(b"this is not a valid image")

    captured_image = CapturedImage(
        path=image_path,
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor_reading = SensorReading(
        soil_moisture=1.2,
        soil_ph=5.1,
        temperature=None,
        humidity=None,
        timestamp=datetime.now(),
    )

    service = ValidationService()

    result = service.validate(captured_image, sensor_reading)

    assert result.is_valid is False
    assert "Captured image is not a valid image." in result.errors
