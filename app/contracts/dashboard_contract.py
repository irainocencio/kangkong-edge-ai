"""
Dashboard service contract.

Defines the interface for dashboard services.
"""

from abc import ABC, abstractmethod

from app.domain.monitoring_result import MonitoringResult


class DashboardServiceContract(ABC):
    """
    Contract for dashboard services.
    """

    @abstractmethod
    def update(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Update the dashboard using a monitoring result.
        """
        raise NotImplementedError