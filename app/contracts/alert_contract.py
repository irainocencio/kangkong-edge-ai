"""
Alert service contract.

Defines the interface for alert services.
"""

from abc import ABC, abstractmethod

from app.domain.monitoring_result import MonitoringResult


class AlertServiceContract(ABC):
    """
    Contract for alert services.
    """

    @abstractmethod
    def check(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Evaluate whether an alert should be sent.
        """
        raise NotImplementedError