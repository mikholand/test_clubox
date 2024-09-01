"""Модуль для управления соединением с базой данных."""
from contextlib import asynccontextmanager

from core.config import settings
from fastapi import FastAPI
from tortoise import Tortoise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Контекстный менеджер для инициализации и закрытия соединений с базой данных.

    Args:
        app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        None: Управляет ресурсами для схем базы данных.
    """
    config = {
        'connections': {'default': settings.database_url},
        'apps': {'models': {'models': ['models.user'], 'default_connection': 'default'}},
        'use_tz': False,
        'timezone': 'UTC',
    }
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas()
    try:
        yield
    finally:
        await Tortoise.close_connections()
