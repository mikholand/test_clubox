"""Модуль с основными командами бота."""
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from utils.backend_client import send_user_data
from utils.config import logger
from utils.telegram import (
    create_response_with_keyboard,
    get_and_structure_user_data,
)

router = Router()


@router.message(Command(commands=['start', 'help']))
async def send_welcome_message(message: Message, command: CommandObject) -> None:
    """Приветственное сообщение.

    Args:
        message (Message): Сообщение от пользователя
        command (CommandObject): Объект команды

    Return:
        None
    """
    user_data = await get_and_structure_user_data(message)
    response = await send_user_data(user_data)
    if response:
        logger.info('response: {0}'.format(response))
    await create_response_with_keyboard(message, command.args)
