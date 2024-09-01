"""Модуль для конфигурации бэкенда и настройки логирования."""
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings:
    """Настройки конфигурации приложения.

    Атрибуты:
        database_url (str): URL базы данных, полученный из переменной окружения DATABASE_URL.
    """

    def __init__(self):
        """Инициализирует настройки конфигурации."""
        self.database_url: str = os.getenv('DATABASE_URL')


settings = Settings()
