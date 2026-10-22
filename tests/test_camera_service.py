"""Tests for the camera service."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import Mock, patch

import cv2
import numpy as np

from app.services.camera_service import CameraService


def test_capture_reports_actual_image_dimensions(tmp_path):
    """CapturedImage metadata should match the saved image dimensions."""
    raw_images_directory = tmp_path / "raw"
    image_width = 2592
    image_height = 1944
    fake_image = np.zeros((image_height, image_width, 3), dtype=np.uint8)

    mock_settings = SimpleNamespace(
        storage=SimpleNamespace(
            raw_images_directory=raw_images_directory,
        ),
        camera=SimpleNamespace(
            width=640,
            height=480,
        ),
    )

    hardware = Mock()

    def save_fake_image(output_path):
        assert cv2.imwrite(str(output_path), fake_image)

    hardware.capture_image.side_effect = save_fake_image

    with patch(
        "app.services.camera_service.settings",
        mock_settings,
    ):
        captured_image = CameraService(hardware).capture()

    actual_image = cv2.imread(str(captured_image.path))

    assert actual_image is not None
    assert captured_image.width == image_width
    assert captured_image.height == image_height
    assert actual_image.shape[:2] == (image_height, image_width)
