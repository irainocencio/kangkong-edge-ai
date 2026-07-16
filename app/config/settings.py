"""
Application configuration.

Centralized configuration used throughout
the Edge AI Monitoring System.
"""

from dataclasses import dataclass
from pathlib import Path

# ==================================================
# Project Paths
# ==================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOGS_DIR = PROJECT_ROOT / "logs"
DATASETS_DIR = PROJECT_ROOT / "datasets"
MODELS_DIR = PROJECT_ROOT / "models"
DATABASE_DIR = PROJECT_ROOT / "database"

# Future directories
RAW_IMAGES_DIR = DATASETS_DIR / "raw"
PROCESSED_IMAGES_DIR = DATASETS_DIR / "processed"

# ==================================================
# Logging
# ==================================================

LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "application.log"

# ==================================================
# Scheduler
# ==================================================

MONITORING_INTERVAL_MINUTES = 60

# ==================================================
# Camera
# ==================================================

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# Future camera settings
IMAGE_FORMAT = "jpg"
CAMERA_ROTATION = 0

# ==================================================
# Sensor
# ==================================================

# Reserved for future sensor configuration
SOIL_MOISTURE_CHANNEL = 0
SOIL_PH_CHANNEL = 1

# ==================================================
# AI
# ==================================================

MODEL_PATH = MODELS_DIR / "tflite" / "model.tflite"

CONFIDENCE_THRESHOLD = 0.80

# ==================================================
# Decision
# ==================================================

# Reserved for future decision logic
NITROGEN_DEFICIENCY_THRESHOLD = 0.80

# ==================================================
# Dashboard
# ==================================================

DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000

# ==================================================
# Alert
# ==================================================

ALERTS_ENABLED = True
ALERT_COOLDOWN_MINUTES = 30

# ==================================================
# Database
# ==================================================

DATABASE_NAME = "monitoring.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# ==================================================
# Typed Configuration
# ==================================================


@dataclass(frozen=True, slots=True)
class LoggingConfig:
    """Logging configuration."""

    level: str
    file: Path


@dataclass(frozen=True, slots=True)
class MonitoringConfig:
    """Monitoring scheduler configuration."""

    interval_minutes: int


@dataclass(frozen=True, slots=True)
class CameraConfig:
    """Camera configuration."""

    width: int
    height: int
    image_format: str
    rotation: int


@dataclass(frozen=True, slots=True)
class SensorConfig:
    """Sensor configuration."""

    soil_moisture_channel: int
    soil_ph_channel: int


@dataclass(frozen=True, slots=True)
class InferenceConfig:
    """AI inference configuration."""

    model_path: Path
    confidence_threshold: float


@dataclass(frozen=True, slots=True)
class DecisionConfig:
    """Decision configuration."""

    nitrogen_deficiency_threshold: float


@dataclass(frozen=True, slots=True)
class DashboardConfig:
    """Dashboard configuration."""

    host: str
    port: int


@dataclass(frozen=True, slots=True)
class AlertConfig:
    """Alert configuration."""

    enabled: bool
    cooldown_minutes: int


@dataclass(frozen=True, slots=True)
class StorageConfig:
    """Storage configuration."""

    database_path: Path
    database_directory: Path
    logs_directory: Path
    datasets_directory: Path
    raw_images_directory: Path
    processed_images_directory: Path
    models_directory: Path


@dataclass(frozen=True, slots=True)
class ApplicationSettings:
    """Root application configuration."""

    logging: LoggingConfig
    monitoring: MonitoringConfig
    camera: CameraConfig
    sensors: SensorConfig
    inference: InferenceConfig
    decision: DecisionConfig
    dashboard: DashboardConfig
    alerts: AlertConfig
    storage: StorageConfig


settings = ApplicationSettings(
    logging=LoggingConfig(
        level=LOG_LEVEL,
        file=LOG_FILE,
    ),
    monitoring=MonitoringConfig(
        interval_minutes=MONITORING_INTERVAL_MINUTES,
    ),
    camera=CameraConfig(
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT,
        image_format=IMAGE_FORMAT,
        rotation=CAMERA_ROTATION,
    ),
    sensors=SensorConfig(
        soil_moisture_channel=SOIL_MOISTURE_CHANNEL,
        soil_ph_channel=SOIL_PH_CHANNEL,
    ),
    inference=InferenceConfig(
        model_path=MODEL_PATH,
        confidence_threshold=CONFIDENCE_THRESHOLD,
    ),
    decision=DecisionConfig(
        nitrogen_deficiency_threshold=NITROGEN_DEFICIENCY_THRESHOLD,
    ),
    dashboard=DashboardConfig(
        host=DASHBOARD_HOST,
        port=DASHBOARD_PORT,
    ),
    alerts=AlertConfig(
        enabled=ALERTS_ENABLED,
        cooldown_minutes=ALERT_COOLDOWN_MINUTES,
    ),
    storage=StorageConfig(
        database_path=DATABASE_PATH,
        database_directory=DATABASE_DIR,
        logs_directory=LOGS_DIR,
        datasets_directory=DATASETS_DIR,
        raw_images_directory=RAW_IMAGES_DIR,
        processed_images_directory=PROCESSED_IMAGES_DIR,
        models_directory=MODELS_DIR,
    ),
)