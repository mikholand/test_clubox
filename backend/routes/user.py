"""Маршруты для работы с пользователями."""
from core.constants import HTTP_NOT_FOUND
from db.crud import (
    create_or_update_user,
    get_user_by_id,
    update_user_birthdate,
)
from fastapi import APIRouter, HTTPException
from schemas.user import BirthdateData, UserData

router = APIRouter()


@router.post('/user_data/')
async def receive_user_data(user_data: UserData) -> dict:
    """Принимает данные пользователя и создает или обновляет пользователя.

    Args:
        user_data (UserData): Данные пользователя для создания или обновления.

    Returns:
        dict: Результат операции создания или обновления пользователя.
    """
    return await create_or_update_user(user_data=user_data)


@router.get('/user_data/{user_id}')
async def get_user_data(user_id: int) -> dict:
    """Получает данные пользователя по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        dict: Данные пользователя, если пользователь найден, иначе выбрасывает HTTPException с ошибкой 404.

    Raises:
        HTTPException: Если пользователь не найден.
    """
    user = await get_user_by_id(user_id=user_id)
    if user:
        return user
    raise HTTPException(status_code=HTTP_NOT_FOUND, detail='User not found')


@router.post('/save_birthdate/')
async def save_birthdate(birthdate_data: BirthdateData) -> dict:
    """Сохраняет дату рождения пользователя.

    Args:
        birthdate_data (BirthdateData): Данные о дате рождения пользователя.

    Returns:
        dict: Результат операции обновления даты рождения. Если пользователь не найден, выбрасывается HTTPException с ошибкой 404.

    Raises:
        HTTPException: Если пользователь не найден.
    """
    response = await update_user_birthdate(birthdate_data.user_id, birthdate_data.birthdate)
    if response.get('error') == 'User not found':
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail='User not found')
    return response
