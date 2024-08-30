"""Бот для запуска Telegram Mini App."""
import logging
import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')
HTTP_OK = 200
bot = Bot(token=TOKEN)
dp = Dispatcher()


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


async def get_user_photo_url(user_id: int) -> Optional[str]:
    """Получение URL фотографии профиля пользователя.

    Args:
        user_id (int): Идентификатор пользователя

    Returns:
        Optional[str]: URL фотографии профиля, если она есть, иначе None
    """
    try:
        photos = await bot.get_user_profile_photos(user_id)
        if photos.total_count > 0:
            photo_id = photos.photos[0][0].file_id
            photo_file = await bot.get_file(photo_id)
            return 'https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, photo_file.file_path)
    except Exception as error:
        logger.error('Ошибка получения фотографии пользователя: {0}'.format(error))

    return None


def create_keyboard(profile_link: Optional[str] = None) -> InlineKeyboardMarkup:
    """Создание клавиатуры для пользователя.

    Args:
        profile_link (Optional[str]): Ссылка на профиль для кнопки, если она указана

    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками
    """
    buttons = [
        [InlineKeyboardButton(text='Создать свой профиль', web_app=WebAppInfo(url=NGROK_URL))],
    ]
    if profile_link:
        buttons.insert(0, [InlineKeyboardButton(text='Посмотреть чужой профиль', web_app=WebAppInfo(url=profile_link))])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: Message, command: CommandObject) -> None:
    """Приветственное сообщение.

    Args:
        message (Message): Сообщение от пользователя
        command (CommandObject): Объект команды

    Return:
        None
    """
    text = 'Привет {0}!'.format(message.from_user.full_name)
    command_arg = command.args

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    file_url = await get_user_photo_url(user_id)

    user_data = {
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'photo': file_url,
    }

    response = await send_user_data(user_data)
    if response:
        logger.info('response: {0}'.format(response))

    if command_arg:
        logger.info('command.args: {0}'.format(command_arg))

        user_data = await fetch_user_data(command_arg)

        if user_data and 'error' not in user_data:
            profile_link = '{0}/profile/{1}'.format(NGROK_URL, command_arg)
            keyboard = create_keyboard(profile_link=profile_link)
            await message.answer('Выберите действие для дальнейшего взаимодействия с ботом:', reply_markup=keyboard)
        else:
            await message.answer('Ошибка: Пользователь не найден или возникла ошибка при запросе данных.')
    else:
        keyboard = create_keyboard()
        await message.answer(text, reply_markup=keyboard)


if __name__ == '__main__':
    dp.run_polling(bot)
