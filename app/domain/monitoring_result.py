"""
Monitoring result domain model.

Represents the complete result of a monitoring cycle.
"""

from dataclasses import dataclass
from datetime import datetime

from app.domain.captured_image import CapturedImage
from app.domain.sensor_reading import SensorReading
from app.domain.validation_result import ValidationResult
from app.domain.preprocessing_result import PreprocessingResult
from app.domain.inference_result import InferenceResult
from app.domain.decision_result import DecisionResult


@dataclass(frozen=True, slots=True)
class MonitoringResult:
    """
    Represents the complete monitoring cycle.
    """

    captured_image: CapturedImage
    sensor_reading: SensorReading
    validation: ValidationResult
    preprocessing: PreprocessingResult
    inference: InferenceResult
    decision: DecisionResult
    completed_at: datetime