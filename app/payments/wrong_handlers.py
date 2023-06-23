from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, Message

from app.logger import logger
from . import keyboards, utils
from .states import PaymentStateGroup


async def wrong_choose_amount_content_type(message: Message):
    logger.debug(f'{message.from_user.username} did not press button while '
                 f'choosing amount of product')
    keyboard: InlineKeyboardMarkup = keyboards.get_keyboard()
    await message.answer('Пожалуйста, выберите количество покупаемоего товара',
                         reply_markup=keyboard)


async def wrong_payment_content_type(message: Message, state: FSMContext):
    logger.debug(f'{message.from_user.username} did not pay for product')
    await message.answer('Пожалуйста оплатите товар или отмените действие')
    async with state.proxy() as data:
        await utils.send_invoice(user_id=message.from_user.id,
                                 count=data['count'])


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=wrong_choose_amount_content_type,
                                content_types='any',
                                state=PaymentStateGroup.choose_amount)
    dp.register_message_handler(callback=wrong_payment_content_type,
                                content_types='any',
                                state=PaymentStateGroup.pay)
