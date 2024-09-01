"""Модуль с CRUD операциями."""
from datetime import date

from core.config import logger
from models.user import User


async def create_or_update_user(user_data: dict) -> dict:
    """Обрабатывает получение данных пользователя и создаёт пользователя, если он не существует.

    Args:
        user_data (dict): Данные пользователя для создания или обновления:
            - user_id: идентификатор пользователя
            - first_name: имя пользователя
            - last_name: фамилия пользователя
            - username: имя пользователя
            - photo: фото пользователя

    Returns:
        dict: Сообщение о результате операции.
    """
    user, created = await User.get_or_create(
        user_id=user_data.user_id,
        defaults={
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'username': user_data.username,
            'photo': user_data.photo,
        },
    )
    if created:
        logger.info('User {0} created'.format(user_data.user_id))
        return {'message': 'User created'}
    return {'message': 'User already created'}


async def get_user_by_id(user_id: int) -> dict:
    """Получает данные пользователя по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        dict: Данные пользователя или сообщение об ошибке, если пользователь не найден.
    """
    user = await User.get_or_none(user_id=user_id)
    if user:
        return {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'photo': user.photo,
            'birthdate': user.birthdate,
        }
    return {'error': 'User not found'}


async def update_user_birthdate(user_id: int, birthdate: date) -> dict:
    """Сохраняет дату рождения пользователя по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя.
        birthdate (date): Дата рождения пользователя.

    Returns:
        dict: Сообщение о результате операции.
    """
    try:
        user = await User.get(user_id=user_id)
    except Exception as error:
        return {'error': 'User not found'}
    user.birthdate = birthdate
    await user.save()
    return {'message': 'Birthdate updated successfully'}
