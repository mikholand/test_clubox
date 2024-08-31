"""Инициализация экземпляра бота Telegram."""
from aiogram import Bot
from utils.config import TOKEN

bot = Bot(token=TOKEN)
