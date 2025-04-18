from datetime import datetime

from aiohttp import web

from api_manager import ApiManager
from load_manager import LoadManager


class VisitCounter:
    """
    Класс, обрабатывающий HTTP-запросы и считающий количество посещений.
    """

    def __init__(self) -> None:
        self.load_manager = LoadManager("visits.txt")
        self.api_manager = ApiManager("visits.txt")

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

        visits = self.api_manager.api_visits_all()
        visits += 1
        return web.Response(text=f"Сайт посетили {visits} раз(а)")
