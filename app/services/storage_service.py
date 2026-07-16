"""
Storage service.

Responsible for persisting monitoring results.
"""

from app.contracts.storage_contract import StorageServiceContract
from app.domain.monitoring_result import MonitoringResult
from app.utils.logger import logger


class StorageService(StorageServiceContract):
    """
    Handles persistence of monitoring results.
    """

    def save(
        self,
        monitoring_result: MonitoringResult,
    ) -> None:
        """
        Save a monitoring result.

        Placeholder implementation.
        """

        logger.info("7. Saving monitoring result...")