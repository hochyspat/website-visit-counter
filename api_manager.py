import re

from load_manager import LoadManager


class ApiManager:
    """
    Класс для получения статистики посещений.
    """

    def __init__(self, log_file_name: str) -> None:
        self._load_manager = LoadManager(log_file_name)

    def api_visits_filter_by_date(self, date: str) -> int:
        """
        Фильтрует все посещения по дате.
        Принимает аргументы:
            date (str): Регулярное выражение для сравнения даты.
        Возвращает:
            int: Количество совпадений.
        """
        logs = self._load_manager.load_logs()

        pattern = re.compile(date)
        matches = [t for t in logs if pattern.match(t[1])]

        return len(matches)

    def api_visits_day(self, day: str) -> int:
        """Возвращает количество посещений за день."""

        return self.api_visits_filter_by_date(day)

    def api_visits_month(self, month: str) -> int:
        """Возвращает количество посещений за месяц."""

        return self.api_visits_filter_by_date(month)

    def api_visits_year(self, year: str) -> int:
        """Возвращает количество посещений за год."""

        return self.api_visits_filter_by_date(year)

    def api_visits_all(self) -> int:
        """Возвращает общее количество посещений."""

        logs = self._load_manager.load_logs()
        return len(logs)

    def api_uniq_visits_filter(self, ip: str, date: str) -> int:
        """
        Фильтрует уникальные посещения по IP и дате.
            Принимает аргументы:
                ip (str): IP клиента,
                date (str): Дата.
            Возвращает:
                int: Количество уникальных совпадений.
        """
        logs = self._load_manager.load_logs()

        pattern_date = re.compile(date)
        pattern_ip = re.compile(ip)
        matches = [
            t for t in logs if pattern_date.match(t[1]) and pattern_ip.match(t[0])
        ]

        return len(matches)

    def api_uniq_visits_day(self, ip: str, day: str) -> int:
        """Возвращает количество уникальных посещений по IP за день."""

        return self.api_uniq_visits_filter(ip, day)

    def api_uniq_visits_month(self, ip: str, month: str) -> int:
        """Возвращает количество уникальных посещений по IP за месяц."""

        return self.api_uniq_visits_filter(ip, month)

    def api_uniq_visits_year(self, ip: str, year: str) -> int:
        """Возвращает количество уникальных посещений по IP за год."""

        return self.api_uniq_visits_filter(ip, year)

    def api_uniq_visits_all(self, ip: str, date: str = r"^\d{4}-\d{2}-\d{2}$") -> int:
        """Возвращает количество всех уникальных посещений по IP."""

        return self.api_uniq_visits_filter(ip, date)
