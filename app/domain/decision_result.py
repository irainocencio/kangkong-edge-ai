"""
Inference result domain model.

Represents the output of the AI inference stage.
"""

from dataclasses import dataclass
from datetime import datetime

from app.domain.enums import PlantHealthStatus


@dataclass(frozen=True, slots=True)
class InferenceResult:
    """
    Represents the result of AI inference.
    """

    prediction: PlantHealthStatus
    confidence: float
    model_version: str
    timestamp: datetime