"""
Bootstrap module.

Responsible for constructing and wiring the application's
core components before execution.
"""

from app.config.settings import ApplicationSettings, settings

from app.core.application import Application
from app.core.lifecycle import Lifecycle
from app.core.monitoring_manager import MonitoringManager
from app.core.scheduler import Scheduler

from app.hardware.contracts.hardware_provider_contract import (
    HardwareProviderContract,
)
from app.hardware.hardware_provider import HardwareProvider

from app.services.alert_service import AlertService
from app.services.camera_service import CameraService
from app.services.dashboard_service import DashboardService
from app.services.decision_service import DecisionService
from app.services.inference_service import InferenceService
from app.services.preprocessing_service import PreprocessingService
from app.services.sensor_service import SensorService
from app.services.storage_service import StorageService
from app.services.validation_service import ValidationService


class Bootstrap:
    """
    Builds and initializes the application's dependencies.
    """

    def __init__(self) -> None:
        """
        Initialize the bootstrap process.
        """

        self._settings: ApplicationSettings = settings

    # ==================================================
    # Infrastructure
    # ==================================================

    def _build_lifecycle(self) -> Lifecycle:
        """
        Create the application lifecycle manager.
        """

        return Lifecycle()

    # ==================================================
    # Hardware
    # ==================================================

    def _build_hardware_provider(
        self,
    ) -> HardwareProviderContract:
        """
        Create the hardware provider.
        """

        return HardwareProvider()

    # ==================================================
    # Services
    # ==================================================

    def _build_camera_service(
        self,
        hardware_provider: HardwareProviderContract,
    ) -> CameraService:
        """
        Create the camera service.
        """

        return CameraService(
            hardware=hardware_provider.camera(),
        )

    def _build_sensor_service(
            self,
            hardware_provider: HardwareProviderContract,
        ) -> SensorService:
        """
        Create the sensor service.
        """

        return SensorService(
            hardware=hardware_provider.sensor(),
        )

    def _build_validation_service(self) -> ValidationService:
        """
        Create the validation service.
        """

        return ValidationService()

    def _build_preprocessing_service(self) -> PreprocessingService:
        """
        Create the preprocessing service.
        """

        return PreprocessingService()

    def _build_inference_service(self) -> InferenceService:
        """
        Create the inference service.
        """

        return InferenceService()

    def _build_decision_service(self) -> DecisionService:
        """
        Create the decision service.
        """

        return DecisionService()

    def _build_storage_service(self) -> StorageService:
        """
        Create the storage service.
        """

        return StorageService()

    def _build_dashboard_service(self) -> DashboardService:
        """
        Create the dashboard service.
        """

        return DashboardService()

    def _build_alert_service(self) -> AlertService:
        """
        Create the alert service.
        """

        return AlertService()

    # ==================================================
    # Core Components
    # ==================================================

    def _build_monitoring_manager(
        self,
        camera_service: CameraService,
        sensor_service: SensorService,
        validation_service: ValidationService,
        preprocessing_service: PreprocessingService,
        inference_service: InferenceService,
        decision_service: DecisionService,
        storage_service: StorageService,
        dashboard_service: DashboardService,
        alert_service: AlertService,
    ) -> MonitoringManager:
        """
        Create the monitoring manager.
        """

        return MonitoringManager(
            camera_service=camera_service,
            sensor_service=sensor_service,
            validation_service=validation_service,
            preprocessing_service=preprocessing_service,
            inference_service=inference_service,
            decision_service=decision_service,
            storage_service=storage_service,
            dashboard_service=dashboard_service,
            alert_service=alert_service,
        )

    def _build_scheduler(
        self,
        monitoring_manager: MonitoringManager,
    ) -> Scheduler:
        """
        Create the scheduler.
        """

        return Scheduler(
            monitoring_manager=monitoring_manager,
        )

    def _build_application(
        self,
        lifecycle: Lifecycle,
        scheduler: Scheduler,
    ) -> Application:
        """
        Create the application.
        """

        return Application(
            lifecycle=lifecycle,
            scheduler=scheduler,
        )

    # ==================================================
    # Composition Root
    # ==================================================

    def build(self) -> Application:
        """
        Build and wire all application components.
        """

        # Infrastructure
        lifecycle = self._build_lifecycle()

        # Hardware
        hardware_provider = self._build_hardware_provider()

        # Services
        camera_service = self._build_camera_service(
            hardware_provider=hardware_provider,
        )

        sensor_service = self._build_sensor_service(
            hardware_provider=hardware_provider,
        )

        validation_service = self._build_validation_service()

        preprocessing_service = self._build_preprocessing_service()

        inference_service = self._build_inference_service()

        decision_service = self._build_decision_service()

        storage_service = self._build_storage_service()

        dashboard_service = self._build_dashboard_service()

        alert_service = self._build_alert_service()

        # Core Components
        monitoring_manager = self._build_monitoring_manager(
            camera_service=camera_service,
            sensor_service=sensor_service,
            validation_service=validation_service,
            preprocessing_service=preprocessing_service,
            inference_service=inference_service,
            decision_service=decision_service,
            storage_service=storage_service,
            dashboard_service=dashboard_service,
            alert_service=alert_service,
        )

        scheduler = self._build_scheduler(
            monitoring_manager=monitoring_manager,
        )

        application = self._build_application(
            lifecycle=lifecycle,
            scheduler=scheduler,
        )

        return application