"""Бекенд для работы Telegram Mini App."""
import logging
import os
from contextlib import asynccontextmanager
from datetime import date, datetime
from typing import AsyncGenerator, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import User
from pydantic import BaseModel
from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
HTTP_NOT_FOUND = 404


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Контекстный менеджер для инициализации и закрытия соединений с базой данных.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        None: Управляет ресурсами для схем базы данных.
    """
    config = {
        'connections': {
            'default': DATABASE_URL,
        },
        'apps': {
            'models': {
                'models': ['models'],
                'default_connection': 'default',
            },
        },
        'use_tz': False,
        'timezone': 'UTC',
    }

    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()

    try:
        yield
    finally:
        await Tortoise.close_connections()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


User_Pydantic = pydantic_model_creator(User, name='User')


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


# Эндпоинт для получения данных о пользователе
@app.post('/user_data/')
async def receive_user_data(user_data: UserData) -> dict:
    """Обрабатывает получение данных пользователя и создаёт пользователя, если он не существует.

    Args:
        user_data (UserData): Данные пользователя для создания или обновления.

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


@app.get('/user_data/{user_id}')
async def get_user_data(user_id: int) -> dict:
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
    logger.info('User {0} created'.format(user_id))
    return {'error': 'User not found'}


@app.post('/save_birthdate/')
async def save_birthdate(birthdate_data: BirthdateData) -> dict:
    """Сохраняет дату рождения пользователя по его идентификатору.

    Args:
        birthdate_data (BirthdateData): Данные о дате рождения пользователя.

    Returns:
        dict: Сообщение о результате операции.
    """
    user = await User.get(user_id=birthdate_data.user_id)
    try:
        user.birthdate = birthdate_data.birthdate
        await user.save()
        return {'message': 'Birthdate updated successfully'}
    except Exception as error:
        return {'message': 'User created successfully'}


@app.get('/profile/{user_id}')
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
        now = datetime.now()
        today = now.date()

        try:
            birthdate = user.birthdate.strftime('%Y-%m-%d')
            next_birthday = datetime(today.year, user.birthdate.month, user.birthdate.day)

            if next_birthday < now:
                next_birthday = datetime(today.year + 1, user.birthdate.month, user.birthdate.day)

            time_diff = next_birthday - now
            time_left_in_minutes = time_diff.total_seconds() // 60

        except Exception as error:
            birthdate = 0
            time_left_in_minutes = 0

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
    except DoesNotExist:
        raise HTTPException(status_code=HTTP_NOT_FOUND, detail='User not found')
