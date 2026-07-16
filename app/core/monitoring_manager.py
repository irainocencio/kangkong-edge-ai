"""
Monitoring manager.

Coordinates one complete monitoring cycle.
"""

from datetime import datetime

from app.contracts.alert_contract import AlertServiceContract
from app.contracts.camera_contract import CameraServiceContract
from app.contracts.dashboard_contract import DashboardServiceContract
from app.contracts.decision_contract import DecisionServiceContract
from app.contracts.inference_contract import InferenceServiceContract
from app.contracts.preprocessing_contract import PreprocessingServiceContract
from app.contracts.sensor_contract import SensorServiceContract
from app.contracts.storage_contract import StorageServiceContract
from app.contracts.validation_contract import ValidationServiceContract

from app.domain.monitoring_result import MonitoringResult

from app.utils.logger import logger


class MonitoringManager:
    """
    Coordinates the monitoring workflow.
    """

    def __init__(
        self,
        camera_service: CameraServiceContract,
        sensor_service: SensorServiceContract,
        validation_service: ValidationServiceContract,
        preprocessing_service: PreprocessingServiceContract,
        inference_service: InferenceServiceContract,
        decision_service: DecisionServiceContract,
        storage_service: StorageServiceContract,
        dashboard_service: DashboardServiceContract,
        alert_service: AlertServiceContract,
    ) -> None:
        """
        Initialize the monitoring manager.
        """

        self.camera = camera_service
        self.sensor = sensor_service
        self.validation = validation_service
        self.preprocessing = preprocessing_service
        self.inference = inference_service
        self.decision = decision_service
        self.storage = storage_service
        self.dashboard = dashboard_service
        self.alert = alert_service

    def run_cycle(self) -> None:
        """
        Execute one monitoring cycle.
        """

        logger.info("----- Monitoring Cycle Started -----")

        captured_image = self.camera.capture()

        sensor_reading = self.sensor.read()

        validation_result = self.validation.validate(
            captured_image,
            sensor_reading,
        )

        preprocessing_result = self.preprocessing.process(
            captured_image,
        )

        inference_result = self.inference.predict(
            preprocessing_result,
        )

        decision_result = self.decision.evaluate(
            inference_result,
        )

        monitoring_result = MonitoringResult(
            captured_image=captured_image,
            sensor_reading=sensor_reading,
            validation=validation_result,
            preprocessing=preprocessing_result,
            inference=inference_result,
            decision=decision_result,
            completed_at=datetime.now(),
        )

        self.storage.save(monitoring_result)

        self.dashboard.update(monitoring_result)

        self.alert.check(monitoring_result)

        logger.info("----- Monitoring Cycle Complete -----")