from aiogram import Dispatcher
from aiogram.types import Message

from app.logger import logger
from . import keyboards
from .states import OrderStateGroup


async def wrong_business_content_type(message: Message):
    logger.debug(f'{message.from_user.username} did not press button while '
                 f'choosing business type')
    keyboard = await keyboards.get_keyboard_with_business_names()
    await message.answer('Пожалуйста, выберите вид вашего бизнеса',
                         reply_markup=keyboard)


async def wrong_platform_content_type(message: Message):
    logger.debug(f'{message.from_user.username} did not press button while '
                 f'choosing platform')
    keyboard = await keyboards.get_keyboard_with_platforms()
    await message.answer('Пожалуйста, выберите платформу для бота',
                         reply_markup=keyboard)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=wrong_business_content_type,
                                content_types='any',
                                state=OrderStateGroup.business_name)
    dp.register_message_handler(callback=wrong_platform_content_type,
                                content_types='any',
                                state=OrderStateGroup.platform_name)
