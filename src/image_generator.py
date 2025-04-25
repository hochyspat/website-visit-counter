import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class ImageGenerator:
    """
    Класс для генерации изображения с текстом и встроенной картинкой.
    """

    def __init__(self) -> None:
        """
        Инициализация генератора изображения.
        Загружает шрифт и картинку.
        """
        self.font: ImageFont.FreeTypeFont = ImageFont.truetype("arial.ttf", 40)
        img_path: str = os.path.join(os.path.dirname(__file__), "hello.png")
        self.hello_image: Image.Image = Image.open(img_path).convert("RGBA")

    def generate_image(self, number: int) -> bytes:
        """
        Генерирует изображение, содержащее текст и встроенную картинку.
        Возвращает PNG-изображение в байтовом формате, готовое для передачи по сети.
        """
        text: str = f"Сайт посетили {number} раз(а)"

        temp_img: Image.Image = Image.new("RGB", (1, 1))
        draw: ImageDraw = ImageDraw.Draw(temp_img)
        bbox = draw.textbbox((0, 0), text, font=self.font)
        text_width: int = bbox[2] - bbox[0]
        text_height: int = bbox[3] - bbox[1]

        padding: int = 40
        spacing: int = 20

        hello_img: Image.Image = self.hello_image
        hello_width: int = hello_img.width
        hello_height: int = hello_img.height

        width: int = max(text_width, hello_width) + padding * 2
        total_height: int = text_height + spacing + hello_height + padding * 2

        img: Image.Image = Image.new("RGB", (width, total_height), "#e0f7fa")
        draw = ImageDraw.Draw(img)

        text_x: int = (width - text_width) // 2
        text_y: int = padding
        draw.text((text_x, text_y), text, font=self.font, fill="#004d40")

        hello_x: int = (width - hello_width) // 2
        hello_y: int = text_y + text_height + spacing
        img.paste(hello_img, (hello_x, hello_y), hello_img)

        buffer: BytesIO = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
