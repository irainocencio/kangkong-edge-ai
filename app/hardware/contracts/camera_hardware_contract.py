"""
Camera hardware contract.

Defines the interface for camera hardware implementations.
"""

from abc import ABC, abstractmethod
from pathlib import Path


class CameraHardwareContract(ABC):
    """
    Contract for camera hardware implementations.
    """

    @abstractmethod
    def capture_image(
        self,
        output_path: Path,
    ) -> None:
        """
        Capture an image and save it to the specified path.
        """
        raise NotImplementedError