"""Основной модуль для запуска Telegram бота."""
import asyncio

from aiogram import Dispatcher
from bot_instance import bot
from handlers.main_commands import router as main_router


async def main_commands():
    """Настраивает и запускает Telegram бота."""
    dp = Dispatcher()

    dp.include_router(main_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main_commands())
