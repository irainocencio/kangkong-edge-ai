"""Tests for mock camera hardware."""

from app.hardware.mock.mock_camera_hardware import MockCameraHardware


def test_mock_camera_creates_non_empty_image(tmp_path):
    """The mock should produce input that passes image validation."""

    output_path = tmp_path / "captured.jpg"

    MockCameraHardware().capture_image(output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0
    assert output_path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
