"""
Storage service contract.

Defines the interface for data storage services.
"""

from abc import ABC, abstractmethod

from app.domain.monitoring_result import MonitoringResult


class StorageServiceContract(ABC):
    """
    Contract for storage services.
    """

    @abstractmethod
    def save(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Save a monitoring result.
        """
        raise NotImplementedError