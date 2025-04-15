from api_manager import ApiManager


def build_month_regex(month: str) -> str:
    """
    Преобразует строку месяца в регулярное выражение.

    Аргументы:
        month (str): Месяц в формате 'YYYY-MM'.

    Возвращает:
        str: Регулярное выражение для фильтрации дат по месяцу.
    """
    return rf"{month}-\d{{2}}"


def build_year_regex(year: str) -> str:
    """
    Преобразует строку года в регулярное выражение.

    Аргументы:
        year (str): Год в формате 'YYYY'.

    Возвращает:
        str: Регулярное выражение для фильтрации дат по году.
    """
    return rf"{year}-\d{{2}}-\d{{2}}"


def main():
    """
    - Получает ввод от пользователя: день, месяц, год, IP.
    - Преобразует введённые значения в регулярные выражения.
    - Вызывает методы из ApiManager для получения статистики.
    - Записывает все результаты в файл 'stats.txt'.
    """
    api = ApiManager()

    day = input("Введите день (в формате YYYY-MM-DD): ").strip()
    month_raw = input("Введите месяц (в формате YYYY-MM): ").strip()
    year_raw = input("Введите год (в формате YYYY): ").strip()
    ip = input("Введите IP-адрес: ").strip()

    month_regex = build_month_regex(month_raw)
    year_regex = build_year_regex(year_raw)

    stats = [
        f"Общее количество посещений: {api.api_visits_all()}",
        f"Посещений за день ({day}): {api.api_visits_day(day)}",
        f"Посещений за месяц ({month_raw}): {api.api_visits_month(month_regex)}",
        f"Посещений за год ({year_raw}): {api.api_visits_year(year_regex)}",
        f"Всего уникальных посещений по IP {ip}: {api.api_uniq_visits_all(ip)}",
        f"Уникальных за день ({day}) по IP {ip}: {api.api_uniq_visits_day(ip, day)}",
        f"Уникальных за месяц ({month_raw}) по IP {ip}: {api.api_uniq_visits_month(ip, month_regex)}",
        f"Уникальных за год ({year_raw}) по IP {ip}: {api.api_uniq_visits_year(ip, year_regex)}",
    ]

    with open("stats.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(stats))

    print("Все данные записаны в stats.txt")


if __name__ == "__main__":
    main()
