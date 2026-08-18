"""Tests for monitoring decision rules."""

from datetime import datetime

from app.domain.enums import PlantHealthStatus
from app.domain.inference_result import InferenceResult
from app.services.decision_service import DecisionService


def test_high_confidence_deficiency_triggers_alert():
    inference = InferenceResult(
        prediction=PlantHealthStatus.POSSIBLE_NITROGEN_DEFICIENCY,
        confidence=0.95,
        model_version="test",
        timestamp=datetime.now(),
    )

    result = DecisionService().evaluate(inference)

    assert result.should_alert is True


def test_healthy_result_does_not_trigger_alert():
    inference = InferenceResult(
        prediction=PlantHealthStatus.HEALTHY,
        confidence=0.95,
        model_version="test",
        timestamp=datetime.now(),
    )

    result = DecisionService().evaluate(inference)

    assert result.should_alert is False
