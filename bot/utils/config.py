"""Модуль для настройки бота.

Этот модуль содержит конфигурационные параметры и настройки, используемые
ботом. Включает переменные окружения для токена бота и URL, а также
настройки для логирования.
"""
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
NGROK_URL = os.getenv('NGROK_URL')
HTTP_OK = 200
