"""Модуль для расчетов."""
from datetime import datetime


def calculate_time_until_next_birthday(birthdate: datetime, now: datetime) -> float:
    """Рассчитывает время до следующего дня рождения.

    Args:
        birthdate (datetime): Дата рождения пользователя.
        now (datetime): Текущая дата и время.

    Returns:
        float: Время до следующего дня рождения в минутах.
    """
    next_birthday = datetime(now.year, birthdate.month, birthdate.day)

    if next_birthday < now:
        next_birthday = datetime(now.year + 1, birthdate.month, birthdate.day)

    time_diff = next_birthday - now
    return time_diff.total_seconds() // 60
