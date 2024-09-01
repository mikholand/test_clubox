"""Маршруты для работы с профилем."""
from datetime import datetime

from core.constants import HTTP_NOT_FOUND
from fastapi import APIRouter, HTTPException
from models.user import User, User_Pydantic
from tortoise.exceptions import DoesNotExist
from utils.calculate import calculate_time_until_next_birthday

router = APIRouter()


@router.get('/{user_id}')
async def get_profile(user_id: int) -> dict:
    """Получает профиль пользователя и рассчитывает время до следующего дня рождения.

    Args:
        user_id (int): Идентификатор пользователя.

    Returns:
        dict: Данные пользователя и время до следующего дня рождения.

    Raises:
        HTTPException: Если пользователь не найден.
    """
    try:
        user = await User_Pydantic.from_queryset_single(User.get(user_id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail='User not found')

    now = datetime.now()

    birthdate = user.birthdate.strftime('%Y-%m-%d')
    time_left_in_minutes = calculate_time_until_next_birthday(user.birthdate, now)

    return {
        'user': {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'photo': user.photo,
            'birthdate': birthdate,
        },
        'time_left': time_left_in_minutes,
    }
