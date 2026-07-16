"""
Tests for application settings.
"""

from app.config.settings import settings


def test_logging_configuration():
    """
    Logging configuration should be valid.
    """
    assert settings.logging.level == "INFO"
    assert settings.logging.file.name == "application.log"


def test_monitoring_configuration():
    """
    Monitoring configuration should be valid.
    """
    assert settings.monitoring.interval_minutes > 0


def test_camera_configuration():
    """
    Camera configuration should be valid.
    """
    assert settings.camera.width > 0
    assert settings.camera.height > 0
    assert settings.camera.image_format == "jpg"


def test_inference_configuration():
    """
    AI inference configuration should be valid.
    """
    assert settings.inference.model_path.suffix == ".tflite"
    assert 0.0 <= settings.inference.confidence_threshold <= 1.0


def test_storage_configuration():
    """
    Storage configuration should be valid.
    """
    assert settings.storage.logs_directory.name == "logs"
    assert settings.storage.datasets_directory.name == "datasets"
    assert settings.storage.models_directory.name == "models"
    assert settings.storage.database_path.name == "monitoring.db"