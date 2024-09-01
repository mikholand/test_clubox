"""Модуль моделей для приложения."""
from core.constants import (
    MAX_LENGTH_FIRST_NAME,
    MAX_LENGTH_LAST_NAME,
    MAX_LENGTH_PHOTO,
    MAX_LENGTH_USERNAME,
)
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class User(models.Model):
    """Модель пользователя.

    Атрибуты:
        user_id (int): Идентификатор пользователя.
        first_name (str): Имя пользователя.
        last_name (str, optional): Фамилия пользователя.
        username (str, optional): Имя пользователя в Telegram.
        photo (str, optional): URL фотографии профиля.
        birthdate (date, optional): Дата рождения пользователя.
    """

    user_id = fields.BigIntField(pk=True, unique=True)
    first_name = fields.CharField(max_length=MAX_LENGTH_FIRST_NAME)
    last_name = fields.CharField(max_length=MAX_LENGTH_LAST_NAME, null=True)
    username = fields.CharField(max_length=MAX_LENGTH_USERNAME, null=True)
    photo = fields.CharField(max_length=MAX_LENGTH_PHOTO, null=True)
    birthdate = fields.DateField(null=True)

    class Meta:
        """Meta информация для модели User."""

        table = 'users'


User_Pydantic = pydantic_model_creator(User, name='User')
