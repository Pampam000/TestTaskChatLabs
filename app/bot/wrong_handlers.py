from aiogram import Dispatcher
from aiogram.types import Message

from app.logger import logger


async def unexpected_message(message: Message):
    logger.debug(f'user: {message.from_user.username} sent message '
                 'without choosing an option')
    await message.answer(
        'Выберите опцию для дальнейшего взаимодействия с ботом')


async def wrong_content_type(message: Message):
    logger.debug(f'user: {message.from_user.username} sent not a text msg')
    await message.answer("Пожалуйста, введите текст")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=unexpected_message,
                                state=None, content_types='any')
    dp.register_message_handler(callback=wrong_content_type,
                                state='*', content_types='any')
