"""
Captured image domain model.

Represents an image captured during a monitoring cycle.
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CapturedImage:
    """
    Represents an image captured by the monitoring system.
    """

    path: Path
    timestamp: datetime
    width: int
    height: int