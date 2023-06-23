from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, PreCheckoutQuery, \
    ContentType, CallbackQuery
from asyncpg import Record

from app.bot.create_bot import bot
from app.config import BUY_PRODUCT_BUTTON, MY_BALANCE_BUTTON
from app.logger import logger
from app.users import crud as users_crud
from . import keyboards, utils
from .states import PaymentStateGroup


async def start_buying(message: Message):
    logger.debug(f'{message.from_user.username} start buying product')
    keyboard = keyboards.get_keyboard()
    await message.answer('Выберите количество', reply_markup=keyboard)
    await PaymentStateGroup.choose_amount.set()


async def choose_amount(callback: CallbackQuery, state: FSMContext):
    logger.debug(f'{callback.from_user.username} choose: {callback.data}')
    count = int(callback.data.split()[1])  # Купить 1 раз
    async with state.proxy() as data:
        data['count'] = count

    user_id = callback.from_user.id

    await utils.send_invoice(user_id=user_id, count=count)

    await PaymentStateGroup.pay.set()
    await callback.answer()


async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: Message, state: FSMContext):
    logger.debug(f'{message.from_user.username} payed successfully')
    async with state.proxy() as data:
        await users_crud.update_balance(user_id=message.from_user.id,
                                        balance=data['count'])
    await state.finish()


async def get_balance(message: Message):
    logger.debug(f'{message.from_user.username} wanna get balance')
    balance: Record = await users_crud.get_balance(
        user_id=message.from_user.id)
    await message.answer(f'Ваш баланс: {dict(balance)["balance"]} у.е.')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start_buying, state=None,
                                content_types='text', text=BUY_PRODUCT_BUTTON)
    dp.register_callback_query_handler(callback=choose_amount,
                                       state=PaymentStateGroup.choose_amount)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query,
                                           lambda query: True,
                                           state=PaymentStateGroup.pay)
    dp.register_message_handler(callback=process_successful_payment,
                                content_types=ContentType.SUCCESSFUL_PAYMENT,
                                state=PaymentStateGroup.pay)
    dp.register_message_handler(callback=get_balance,
                                content_types='text', text=MY_BALANCE_BUTTON,
                                state=None)
