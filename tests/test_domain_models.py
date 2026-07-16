"""
Tests for domain models.
"""

from datetime import datetime
from pathlib import Path

from app.domain.captured_image import CapturedImage
from app.domain.sensor_reading import SensorReading
from app.domain.validation_result import ValidationResult
from app.domain.preprocessing_result import PreprocessingResult
from app.domain.inference_result import InferenceResult
from app.domain.decision_result import DecisionResult
from app.domain.monitoring_result import MonitoringResult

from app.domain.enums import (
    PlantHealthStatus,
)


def test_captured_image_creation():
    image = CapturedImage(
        path=Path("image.jpg"),
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    assert image.width == 640
    assert image.height == 480


def test_sensor_reading_creation():
    reading = SensorReading(
        soil_moisture=65.5,
        soil_ph=6.5,
        temperature=28.0,
        humidity=75.0,
        timestamp=datetime.now(),
    )

    assert reading.soil_moisture == 65.5
    assert reading.soil_ph == 6.5


def test_validation_result_creation():
    result = ValidationResult(
        is_valid=True,
        errors=(),
    )

    assert result.is_valid
    assert len(result.errors) == 0


def test_preprocessing_result_creation():
    result = PreprocessingResult(
        processed_image_path=Path("processed.jpg"),
        metadata={},
    )

    assert result.processed_image_path.name == "processed.jpg"


def test_inference_result_creation():
    result = InferenceResult(
        prediction=PlantHealthStatus.HEALTHY,
        confidence=0.95,
        model_version="1.0",
        timestamp=datetime.now(),
    )

    assert result.prediction == PlantHealthStatus.HEALTHY


def test_decision_result_creation():
    result = DecisionResult(
        health_status=PlantHealthStatus.HEALTHY,
        should_alert=False,
        reason="Plant is healthy.",
    )

    assert result.should_alert is False
    assert result.reason == "Plant is healthy."


def test_monitoring_result_creation():

    image = CapturedImage(
        path=Path("image.jpg"),
        timestamp=datetime.now(),
        width=640,
        height=480,
    )

    sensor = SensorReading(
        soil_moisture=60,
        soil_ph=6.8,
        temperature=27,
        humidity=70,
        timestamp=datetime.now(),
    )

    validation = ValidationResult(
        is_valid=True,
        errors=(),
    )

    preprocessing = PreprocessingResult(
        processed_image_path=Path("processed.jpg"),
        metadata={},
    )

    inference = InferenceResult(
        prediction=PlantHealthStatus.HEALTHY,
        confidence=0.95,
        model_version="1.0",
        timestamp=datetime.now(),
    )

    decision = DecisionResult(
        health_status=PlantHealthStatus.HEALTHY,
        should_alert=False,
        reason="Plant is healthy.",
    )

    monitoring = MonitoringResult(
        captured_image=image,
        sensor_reading=sensor,
        validation=validation,
        preprocessing=preprocessing,
        inference=inference,
        decision=decision,
        completed_at=datetime.now(),
    )

    assert monitoring.decision.should_alert is False