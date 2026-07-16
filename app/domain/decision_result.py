"""
Decision result domain model.

Represents the business decision after AI inference.
"""

from dataclasses import dataclass

from app.domain.enums import PlantHealthStatus


@dataclass(frozen=True, slots=True)
class DecisionResult:
    """
    Represents the evaluated monitoring decision.
    """

    health_status: PlantHealthStatus
    should_alert: bool
    reason: str