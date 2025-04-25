from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from src.image_generator import ImageGenerator


@pytest.fixture
def mock_hello_image() -> Image.Image:
    return Image.new("RGBA", (100, 100), color=(255, 0, 0, 255))


@patch("src.image_generator.ImageDraw.Draw")
@patch("src.image_generator.ImageFont.truetype")
@patch("src.image_generator.Image.open")
def test_generate_image(
    mock_open: MagicMock,
    mock_truetype: MagicMock,
    mock_draw_class: MagicMock,
    mock_hello_image: Image.Image,
) -> None:
    mock_truetype.return_value = MagicMock()
    mock_open.return_value = mock_hello_image

    mock_draw_instance = MagicMock()
    mock_draw_instance.textbbox.return_value = (0, 0, 200, 50)
    mock_draw_class.return_value = mock_draw_instance

    generator = ImageGenerator()

    result_bytes = generator.generate_image(5)

    assert isinstance(result_bytes, bytes)
    assert len(result_bytes) > 0
    assert result_bytes[:8] == b"\x89PNG\r\n\x1a\n"

    mock_truetype.assert_called_once_with("arial.ttf", 40)
    mock_open.assert_called_once()
    mock_draw_class.assert_called()
    mock_draw_instance.textbbox.assert_called()
