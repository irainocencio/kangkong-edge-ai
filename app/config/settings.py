"""
Application configuration.

Centralized configuration used throughout
the Edge AI Monitoring System.
"""

from pathlib import Path

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOGS_DIR = PROJECT_ROOT / "logs"
DATASETS_DIR = PROJECT_ROOT / "datasets"
MODELS_DIR = PROJECT_ROOT / "models"
DATABASE_DIR = PROJECT_ROOT / "database"

# --------------------------------------------------
# Logging
# --------------------------------------------------

LOG_LEVEL = "INFO"
LOG_FILE = LOGS_DIR / "application.log"

# --------------------------------------------------
# Scheduler
# --------------------------------------------------

MONITORING_INTERVAL_MINUTES = 60

# --------------------------------------------------
# Camera
# --------------------------------------------------

IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480

# --------------------------------------------------
# AI
# --------------------------------------------------

MODEL_PATH = MODELS_DIR / "tflite" / "model.tflite"

# --------------------------------------------------
# Database
# --------------------------------------------------

DATABASE_NAME = "monitoring.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME