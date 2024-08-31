"""
Модуль для выполнения HTTP-запросов к API.

Этот модуль предоставляет функции для отправки данных пользователя на бекенд
и получения их из него с использованием библиотеки aiohttp. Также он включает
контекстный менеджер для работы с aiohttp-сессией.
"""
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import aiohttp
from utils.config import HTTP_OK, NGROK_URL, logger


@asynccontextmanager
async def get_session():
    """Контекст менеджер для создания aiohttp сессии."""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()


async def send_user_data(user_data: dict) -> Optional[str]:
    """Отправка данных пользователя на бекенд для сохранения в БД.

    Args:
        user_data (dict): Словарь с информацией о пользователе

    Returns:
        Optional[str]: Текст ответа сервера в случае успешного выполнения запроса, иначе None
    """
    async with get_session() as session:
        try:
            async with session.post('{0}/api/user_data'.format(NGROK_URL), json=user_data) as response:
                response_text = await response.text()
                if response.status == HTTP_OK:
                    return response_text
                logger.error('Ошибка при отправке данных: {0} {1}'.format(response.status, response_text))
                return None
        except aiohttp.ClientError as error:
            logger.error('Ошибка соединения с сервером: {0}'.format(error))
            return None


async def fetch_user_data(user_id: str) -> Optional[Dict[str, Any]]:
    """Получение данных пользователя из бекенда по его идентификатору.

    Args:
        user_id (str): Идентификатор пользователя

    Returns:
        Optional[Dict[str, Any]]: Словарь с данными пользователя в случае успешного выполнения запроса, иначе None
    """
    async with get_session() as session:
        try:
            async with session.get('{0}/api/user_data/{1}'.format(NGROK_URL, user_id)) as response:
                if response.status == HTTP_OK:
                    return await response.json()
                logger.error('Ошибка при получении данных пользователя: {0}'.format(response.status))
                return None
        except aiohttp.ClientError as error:
            logger.error('Ошибка соединения с сервером: {0}'.format(error))
            return None
