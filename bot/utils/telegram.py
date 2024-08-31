"""Модуль с функциями для взаимодействия с пользователем."""
from typing import Optional

from aiogram.types import Message
from bot_instance import bot
from keyboards.inline import create_start_keyboard
from utils.backend_client import fetch_user_data
from utils.config import NGROK_URL, TOKEN, logger


async def create_response_with_keyboard(message: Message, command_arg: Optional[str] = None) -> None:
    """Создает ответ пользователю с клавиатурой.

    Args:
        message (Message): Сообщение от пользователя.
        command_arg (str, optional): Аргумент команды.
    """
    if command_arg:
        logger.info('command.args: {0}'.format(command_arg))

        user_data = await fetch_user_data(command_arg)

        if user_data and 'error' not in user_data:
            profile_link = '{0}/profile/{1}'.format(NGROK_URL, command_arg)
            keyboard = create_start_keyboard(profile_link=profile_link)
            await message.answer('Выберите действие для дальнейшего взаимодействия с ботом:', reply_markup=keyboard)
        else:
            await message.answer('Ошибка: Пользователь не найден или возникла ошибка при запросе данных.')
    else:
        keyboard = create_start_keyboard()
        await message.answer('Привет {0}!'.format(message.from_user.full_name), reply_markup=keyboard)


async def get_and_structure_user_data(message: Message) -> dict:
    """Получает и структурирует данные пользователя.

    Args:
        message (Message): Сообщение от пользователя.

    Returns:
        dict: Данные пользователя.
    """
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    photo_url = await get_user_photo_url(user_id)
    logger.info('photo_url: {0}'.format(photo_url))

    return {
        'user_id': user_id,
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'photo': photo_url,
    }


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
