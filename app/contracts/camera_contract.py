"""
Camera service contract.

Defines the interface for image capture services.
"""

from abc import ABC, abstractmethod

from app.domain.captured_image import CapturedImage


class CameraServiceContract(ABC):
    """
    Contract for camera services.
    """

    @abstractmethod
    def capture(self) -> CapturedImage:
        """
        Capture an image.

        Returns:
            CapturedImage: The captured image.
        """
        raise NotImplementedError