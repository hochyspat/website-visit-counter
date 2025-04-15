class LoadManager:
    """
    Класс для чтения и записи логов посещений.
    """

    def __init__(self, log_file_name: str) -> None:
        self.log_file = log_file_name

    def save_log(self, client_ip: str, access_date: str) -> None:
        """
        Сохраняет IP и дату в файл.
        Принимает аргументы:
            client_ip (str): IP-адрес клиента.
            access_date (str): Дата в формате YYYY-MM-DD.
        """

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{client_ip} {access_date}\n")

    def load_logs(self) -> list[tuple[str, str]]:
        """
        Загружает все строки из файла логов.
        Возвращает:
            List[Tuple[str, str]]: Список кортежей (IP, дата).
        """

        with open(self.log_file, "r", encoding="utf-8") as f:
            line = f.readline()
            visits = []
            while line:
                client_ip, access_date = line.split(" ")
                visits.append((client_ip, access_date))
                line = f.readline()
        return visits
