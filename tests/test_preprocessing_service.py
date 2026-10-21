
"""Tests for image preprocessing."""

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np
import pytest

from app.domain.captured_image import CapturedImage
from app.services.preprocessing_service import PreprocessingService


def test_process_resizes_and_saves_image(tmp_path):
    """Processing should resize the image and return its output metadata."""
    captured_path = tmp_path / "captured.png"
    captured_path.write_bytes(b"mock image")

    processed_directory = tmp_path / "processed"
    fake_image = np.zeros((100, 100, 3), dtype=np.uint8)
    resized_image = np.zeros((480, 640, 3), dtype=np.uint8)

    mock_settings = SimpleNamespace(
        storage=SimpleNamespace(
            processed_images_directory=processed_directory,
        ),
        camera=SimpleNamespace(
            width=640,
            height=480,
            image_format="png",
        ),
    )

    with (
        patch(
            "app.services.preprocessing_service.settings",
            mock_settings,
        ),
        patch(
            "app.services.preprocessing_service.cv2.imread",
            return_value=fake_image,
        ),
        patch(
            "app.services.preprocessing_service.cv2.resize",
            return_value=resized_image,
        ) as resize_mock,
        patch(
            "app.services.preprocessing_service.cv2.imwrite",
            return_value=True,
        ) as write_mock,
    ):
        result = PreprocessingService().process(
            CapturedImage(
                path=captured_path,
                timestamp=datetime.now(),
                width=100,
                height=100,
            )
        )

    expected_path = processed_directory / captured_path.name

    resize_mock.assert_called_once_with(fake_image, (640, 480))
    write_mock.assert_called_once_with(str(expected_path), resized_image)

    assert result.processed_image_path == expected_path
    assert result.metadata == {
        "width": "640",
        "height": "480",
        "format": "png",
    }


def test_process_raises_when_image_cannot_be_loaded(tmp_path):
    """Processing should reject an unreadable input image."""
    captured_path = tmp_path / "captured.png"
    captured_path.write_bytes(b"invalid image data")

    mock_settings = SimpleNamespace(
        storage=SimpleNamespace(
            processed_images_directory=tmp_path / "processed",
        ),
    )

    with (
        patch(
            "app.services.preprocessing_service.settings",
            mock_settings,
        ),
        patch(
            "app.services.preprocessing_service.cv2.imread",
            return_value=None,
        ),
    ):
        with pytest.raises(ValueError, match="Unable to load image"):
            PreprocessingService().process(
                CapturedImage(
                    path=captured_path,
                    timestamp=datetime.now(),
                    width=100,
                    height=100,
                )
            )


def test_process_raises_when_saving_fails(tmp_path):
    """Processing should not report success if OpenCV fails to save."""
    captured_path = tmp_path / "captured.png"
    captured_path.write_bytes(b"mock image")

    processed_directory = tmp_path / "processed"
    fake_image = np.zeros((100, 100, 3), dtype=np.uint8)
    resized_image = np.zeros((480, 640, 3), dtype=np.uint8)

    mock_settings = SimpleNamespace(
        storage=SimpleNamespace(
            processed_images_directory=processed_directory,
        ),
        camera=SimpleNamespace(
            width=640,
            height=480,
            image_format="png",
        ),
    )

    with (
        patch(
            "app.services.preprocessing_service.settings",
            mock_settings,
        ),
        patch(
            "app.services.preprocessing_service.cv2.imread",
            return_value=fake_image,
        ),
        patch(
            "app.services.preprocessing_service.cv2.resize",
            return_value=resized_image,
        ),
        patch(
            "app.services.preprocessing_service.cv2.imwrite",
            return_value=False,
        ),
    ):
        with pytest.raises(
            OSError,
            match="Unable to save processed image",
        ):
            PreprocessingService().process(
                CapturedImage(
                    path=captured_path,
                    timestamp=datetime.now(),
                    width=100,
                    height=100,
                )
            )
