"""Модели данных для работы с пользователями."""
from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserData(BaseModel):
    """Модель данных пользователя для получения и создания.

    Attributes:
        user_id (int): Идентификатор пользователя.
        first_name (str): Имя пользователя.
        last_name (Optional[str]): Фамилия пользователя.
        username (Optional[str]): Имя пользователя в Telegram.
        photo (Optional[str]): URL фотографии профиля.
    """

    user_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo: Optional[str] = None


class BirthdateData(BaseModel):
    """Модель данных для сохранения даты рождения пользователя.

    Attributes:
        user_id (int): Идентификатор пользователя.
        birthdate (date): Дата рождения пользователя.
    """

    user_id: int
    birthdate: date
