from enum import Enum


class PlantHealthStatus(Enum):
    """Possible plant health classifications."""

    HEALTHY = "Healthy"
    POSSIBLE_NITROGEN_DEFICIENCY = "Possible Nitrogen Deficiency"
    UNKNOWN = "Unknown"


class DecisionStatus(Enum):
    """Possible monitoring decisions."""

    CONTINUE_MONITORING = "Continue Monitoring"
    STORE_ONLY = "Store Only"
    TRIGGER_ALERT = "Trigger Alert"


class AlertLevel(Enum):
    """Alert severity."""

    INFO = "Info"
    WARNING = "Warning"
    CRITICAL = "Critical"