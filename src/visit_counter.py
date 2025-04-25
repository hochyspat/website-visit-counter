from datetime import datetime

from aiohttp import web

from src.api_manager import ApiManager
from src.image_generator import ImageGenerator
from src.load_manager import LoadManager


class VisitCounter:
    """
    Класс, обрабатывающий HTTP-запросы и считающий количество посещений.
    """

    def __init__(self) -> None:
        self.load_manager = LoadManager("../visits.txt")
        self.api_manager = ApiManager("../visits.txt")
        self.image_generator = ImageGenerator()

    def save_log(self, client_ip: str | None, access_date: str) -> None:
        """
        Сохраняет лог посещения.
        Принимает аргументы:
            client_ip (str): IP-адрес клиента.
            access_date (str): Дата в формате YYYY-MM-DD.
        """

        if client_ip is not None:
            self.load_manager.save_log(client_ip, access_date)

    async def handle(self, request: web.Request) -> web.Response:
        """
        Обрабатывает входящий HTTP-запрос и возвращает количество посещений.
        Принимает аргументы:
            request (web.Request): HTTP-запрос.
        Возвращает:
            web.Response: HTTP-ответ с количеством посещений.
        """

        client_ip = request.remote
        access_date = datetime.now().strftime("%Y-%m-%d")

        self.save_log(client_ip, access_date)

        html = """
        <html>
        <head>
            <style>
                body {
                    background-color: #ffffff;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: sans-serif;
                }
            </style>
        </head>
        <body>
            <img src="/image" alt="Visit Image">
        </body>
        </html>
        """
        return web.Response(text=html, content_type="text/html")

    async def handle_image(self, request: web.Request) -> web.Response:
        """
        Обрабатывает HTTP-запрос и возвращает PNG-изображение с числом посещений.
        Возвращает web.Response: HTTP-ответ с изображением в формате PNG.
        """
        visits: int = self.api_manager.api_visits_all()
        image_bytes: bytes = self.image_generator.generate_image(visits)

        return web.Response(body=image_bytes, content_type="image/png")
