"""Модуль для создания inline клавиатур."""
from typing import Optional

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from utils.config import NGROK_URL


def create_start_keyboard(profile_link: Optional[str] = None) -> InlineKeyboardMarkup:
    """Создание клавиатуры для пользователя.

    Args:
        profile_link (Optional[str]): Ссылка на профиль для кнопки, если она указана

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками
    """
    buttons = []

    # Добавление кнопки для создания профиля
    create_profile_button = InlineKeyboardButton(
        text='Создать свой профиль',
        web_app=WebAppInfo(url=NGROK_URL),
    )
    buttons.append([create_profile_button])

    # Добавление кнопки для просмотра чужого профиля, если указана ссылка
    if profile_link:
        view_profile_button = InlineKeyboardButton(
            text='Посмотреть чужой профиль',
            web_app=WebAppInfo(url=profile_link),
        )
        buttons.insert(0, [view_profile_button])

    return InlineKeyboardMarkup(inline_keyboard=buttons)
