"""
Validation result domain model.

Represents the outcome of validating monitoring data.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """
    Represents the outcome of the validation process.
    """

    is_valid: bool
    errors: tuple[str, ...]