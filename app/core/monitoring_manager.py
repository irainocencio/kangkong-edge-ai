"""
Monitoring manager.

Coordinates one complete monitoring cycle.
"""

from app.utils.logger import logger


class MonitoringManager:
    """
    Coordinates the monitoring workflow.
    """

    def __init__(
            self, 
            camera_service,
            sensor_service,
            validation_service,
            preprocessing_service,
            inference_service,
            decision_service,   
            storage_service,   
            dashboard_service,
            alert_service, 
    ):
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

    def run_cycle(self):
        """
        Execute one monitoring cycle.
        """

        logger.info("----- Monitoring Cycle Started -----")

        self.camera.capture()
        self.sensor.read()
        self.validation.validate()
        self.preprocessing.process()
        self.inference.predict()
        self.decision.evaluate()
        self.storage.save()
        self.dashboard.update()
        self.alert.check()

        logger.info("----- Monitoring Cycle Complete -----")