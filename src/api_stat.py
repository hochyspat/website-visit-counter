import re
from src.api_manager import ApiManager


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

def is_valid_date(date: str) -> bool:
    """Валидация даты"""
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", date))


def is_valid_month(month: str) -> bool:
    """Валидация месяца"""
    return bool(re.fullmatch(r"\d{4}-\d{2}", month))


def is_valid_year(year: str) -> bool:
    """Валидация года"""
    return bool(re.fullmatch(r"\d{4}", year))


def is_valid_ip(ip: str) -> bool:
    """Валидация ip"""
    return bool(re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", ip))


def main() -> None:
    """
    Меню для выбора статистики.
    """
    log_file = "../visits.txt"
    api = ApiManager(log_file)
    
    print("Статистики посещений")
    print("1. Все посещения")
    print("2. Уникальные посещения по IP")

    while True:
        stat_type = input("Выберите тип статистики (1/2): ").strip()
        if stat_type in {"1", "2"}:
            break
        print("Ошибка: введите 1 или 2.")

    ip = ""
    if stat_type == "2":
        while True:
            ip = input("Введите IP-адрес: ").strip()
            if is_valid_ip(ip):
                break
            print("Ошибка: введите корректный IP-адрес (например, 192.168.1.1).")

    print("\nВыберите период:")
    print("1. За день")
    print("2. За месяц")
    print("3. За год")
    print("4. За всё время")

    while True:
        period = input("Введите номер периода (1/2/3/4): ").strip()
        if period in {"1", "2", "3", "4"}:
            break
        print("Ошибка: введите число от 1 до 4.")

    result = ""

    if period == "1":
        while True:
            day = input("Введите день (в формате YYYY-MM-DD): ").strip()
            if is_valid_date(day):
                break
            print("Ошибка: неверный формат. Пример: 2024-04-25")
        result = (
            f"Посещений за день ({day}): {api.api_visits_day(day)}"
            if stat_type == "1"
            else f"Уникальных посещений за день ({day}) по IP {ip}: {api.api_uniq_visits_day(ip, day)}"
        )

    elif period == "2":
        while True:
            month = input("Введите месяц (в формате YYYY-MM): ").strip()
            if is_valid_month(month):
                break
            print("Ошибка: неверный формат. Пример: 2024-04")
        month_regex = build_month_regex(month)
        result = (
            f"Посещений за месяц ({month}): {api.api_visits_month(month_regex)}"
            if stat_type == "1"
            else f"Уникальных посещений за месяц ({month}) по IP {ip}: "
            f"{api.api_uniq_visits_month(ip, month_regex)}"
        )

    elif period == "3":
        while True:
            year = input("Введите год (в формате YYYY): ").strip()
            if is_valid_year(year):
                break
            print("Ошибка: неверный формат. Пример: 2024")
        year_regex = build_year_regex(year)
        result = (
            f"Посещений за год ({year}): {api.api_visits_year(year_regex)}"
            if stat_type == "1"
            else f"Уникальных посещений за год ({year}) по IP {ip}: {api.api_uniq_visits_year(ip, year_regex)}"
        )

    elif period == "4":
        result = (
            f"Общее количество посещений: {api.api_visits_all()}"
            if stat_type == "1"
            else f"Всего уникальных посещений по IP {ip}: {api.api_uniq_visits_all(ip)}"
        )

    with open("../stats.txt", "w", encoding="utf-8") as f:
        f.write(result + "\n")

    print("Результат записан в файл stats.txt")


if __name__ == "__main__":
    main()
