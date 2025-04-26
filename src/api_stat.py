import re
from typing import Callable

from src.api_manager import ApiManager
from src.stat_period import StatPeriod
from src.stat_type import StatType


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


def stat_type_select() -> StatType:
    """Выбор типа статистики"""
    while True:
        stat_type: str = input("Выберите тип статистики (1/2): ").strip()
        if stat_type in (stat.value for stat in StatType):
            return StatType(stat_type)
        print("Ошибка: введите 1 или 2.")


def stat_period_select() -> StatPeriod:
    """Выбор периода для создания статистики"""
    while True:
        period: str = input("Введите номер периода (1/2/3/4): ").strip()
        if period in (stat.value for stat in StatPeriod):
            return StatPeriod(period)
        print("Ошибка: введите число от 1 до 4.")


def input_with_validation(
    prompt: str, validation_func: Callable[[str], bool], error_example: str
) -> str:
    """Метод для корректного ввода параметров"""
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(f"Ошибка: неверный формат. Пример: {error_example}")


def main() -> None:
    """
    Меню для выбора статистики.
    """
    log_file = "../visits.txt"
    api = ApiManager(log_file)

    print("Статистики посещений")
    print("1. Все посещения")
    print("2. Уникальные посещения по IP")
    stat_type = stat_type_select()

    ip = ""
    if stat_type == StatType.UNIQUE_VISITS:
        ip = input_with_validation("Введите IP-адрес: ", is_valid_ip, "192.168.1.1")

    print("\nВыберите период:")
    print("1. За день")
    print("2. За месяц")
    print("3. За год")
    print("4. За всё время")

    period = stat_period_select()

    input_settings: dict[
        StatPeriod,
        tuple[
            str,
            Callable[[str], bool],
            str,
            Callable[[str], int],
            Callable[[str, str], int],
        ],
    ] = {
        StatPeriod.DAY_STAT: (
            "Введите день (в формате YYYY-MM-DD): ",
            is_valid_date,
            "2024-04-25",
            api.api_visits_day,
            api.api_uniq_visits_day,
        ),
        StatPeriod.MONTH_STAT: (
            "Введите месяц (в формате YYYY-MM): ",
            is_valid_month,
            "2024-04",
            api.api_visits_month,
            api.api_uniq_visits_month,
        ),
        StatPeriod.YEAR_STAT: (
            "Введите год (в формате YYYY): ",
            is_valid_year,
            "2024",
            api.api_visits_year,
            api.api_uniq_visits_year,
        ),
    }

    match period:
        case StatPeriod.ALL_TIME_STAT:
            result = (
                f"Общее количество посещений: {api.api_visits_all()}"
                if stat_type == StatType.ALL_VISITS
                else f"Всего уникальных посещений по IP {ip}: {api.api_uniq_visits_all(ip)}"
            )
        case _:
            (
                prompt,
                validator,
                example,
                all_visits_func,
                uniq_visits_func,
            ) = input_settings[period]
            value = input_with_validation(prompt, validator, example)

            if period == StatPeriod.MONTH_STAT:
                value = build_month_regex(value)
            elif period == StatPeriod.YEAR_STAT:
                value = build_year_regex(value)

            result = (
                f"Посещений за период: {all_visits_func(value)}"
                if stat_type == StatType.ALL_VISITS
                else f"Уникальных посещений за период по IP {ip}: {uniq_visits_func(ip, value)}"
            )

    with open("../stats.txt", "w", encoding="utf-8") as f:
        f.write(result + "\n")

    print("Результат записан в файл stats.txt")


if __name__ == "__main__":
    main()
