"""
Preprocessing result domain model.

Represents the output of the image preprocessing stage.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PreprocessingResult:
    """
    Represents the result of image preprocessing.
    """

    processed_image_path: Path
    metadata: dict[str, str]