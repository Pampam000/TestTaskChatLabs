import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.utils.exceptions import ChatNotFound
from asyncpg import Record

from app.bot.create_bot import bot
from app.config import TIME_BEFORE_ORDER_NOTIFICATION_IN_SECONDS, \
    SEND_REQUEST_BUTTON
from app.logger import logger
from app.users import crud as users_crud
from . import crud, validators, keyboards
from .states import OrderStateGroup


async def start_making_order(message: Message, state: FSMContext):
    logger.debug(f'user: {message.from_user.username} start making an order')
    keyboard: InlineKeyboardMarkup = await \
        keyboards.get_keyboard_with_business_names()
    await message.answer("Какое направление вашего бизнеса?",
                         reply_markup=keyboard)
    await OrderStateGroup.business_name.set()

    task = asyncio.create_task(send_notification(state=state))

    async with state.proxy() as data:
        data['task'] = task.get_name()


async def choose_business(callback: CallbackQuery, state: FSMContext):
    logger.debug(f'user: {callback.from_user.username} choose business: '
                 f'{callback.data}')
    async with state.proxy() as data:
        data['business_name'] = callback.data

    keyboard: InlineKeyboardMarkup = \
        await keyboards.get_keyboard_with_platforms()
    await callback.message.answer(
        text='На какой платформе вы хотите разработать чат-бот?',
        reply_markup=keyboard)
    await OrderStateGroup.platform_name.set()

    await callback.answer()


async def choose_platform(callback: CallbackQuery, state: FSMContext):
    logger.debug(f'user: {callback.from_user.username} '
                 f'choose platform: {callback.data}')
    async with state.proxy() as data:
        data['platform_name'] = callback.data

    await OrderStateGroup.min_price.set()
    await callback.message.answer('Укажите минимальный бюджет в рублях\n'
                                  'Пример1: 5 000\n'
                                  'Пример2: 20000')
    await callback.answer()


async def set_min_price(message: Message, state: FSMContext):
    text = message.text

    try:
        logger.debug(f'{message.from_user.username} trying to set '
                     f'min price = {text}')
        validators.check_price(price=text)
    except ValueError as e:
        logger.debug(f'{message.from_user.username} get value error: {e}')
        await message.answer(e)
    else:
        logger.debug(f'{message.from_user.username} successfully '
                     f'set min price = {text}')
        async with state.proxy() as data:
            data['min_price'] = int(text)
        await message.answer('Укажите максимальный бюджет')
        await OrderStateGroup.max_price.set()


async def set_max_price(message: Message, state: FSMContext):
    text = message.text
    async with state.proxy() as data:
        try:
            logger.debug(f'{message.from_user.username} trying to set '
                         f'max price = {text}')
            validators.check_price(price=text, min_price=data['min_price'])
        except ValueError as e:
            logger.debug(f'{message.from_user.username} get value error: {e}')
            await message.answer(e)
        else:
            logger.debug(f'{message.from_user.username} successfully '
                         f'set max price = {text}')

            data['max_price'] = int(text)
            await message.answer('Укажите ваш номер телефона')
            await OrderStateGroup.phone.set()


async def set_phone(message: Message, state: FSMContext):
    phone = message.text

    try:
        logger.debug(
            f'{message.from_user.username} trying to set phone = {phone}')
        validators.check_phone(phone=phone)
    except ValueError as e:
        logger.debug(f'{message.from_user.username} get value error: {e}')
        await message.answer(e)
    else:
        logger.debug(f'{message.from_user.username} successfully set '
                     f'phone = {phone}')
        async with state.proxy() as data:
            data['phone'] = phone
            data['user_id'] = message.from_user.id

        for task in asyncio.all_tasks():
            if task.get_name() == data['task']:
                task.cancel()
                break

        data = data.as_dict()
        data.pop('task')

        await crud.insert_order(list_of_args=data.values())

        admins: list[Record] = await users_crud.get_admins()
        for admin in admins:
            try:
                await bot.send_message(
                    admin['id'],
                    'Новая заявка: \n'
                    f'Направление бизнеса: {data["business_name"]}\n'
                    f'Платформа: {data["platform_name"]}\n'
                    f'Бюджет: от {data["min_price"]} до {data["max_price"]}\n'
                    f'Телефон: {data["phone"]}')
            except ChatNotFound:
                logger.debug(f'{dict(admin)["username"]} is not a bot user')
                # await message.answer('except')
        await message.answer('Ваша заявка отправлена администратору')
        await state.finish()


async def send_notification(state: FSMContext):
    await asyncio.sleep(TIME_BEFORE_ORDER_NOTIFICATION_IN_SECONDS)

    current_state = await state.get_state()
    if current_state:
        logger.debug(f'{state.user} got notification')
        await bot.send_message(state.user, 'Ты забыл заполнить заявку!')
        asyncio.create_task(send_notification(state))


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start_making_order,
                                text=SEND_REQUEST_BUTTON,
                                content_types='text', state=None)
    dp.register_callback_query_handler(callback=choose_business,
                                       state=OrderStateGroup.business_name)
    dp.register_callback_query_handler(callback=choose_platform,
                                       state=OrderStateGroup.platform_name)
    dp.register_message_handler(callback=set_min_price, content_types='text',
                                state=OrderStateGroup.min_price)
    dp.register_message_handler(callback=set_max_price, content_types='text',
                                state=OrderStateGroup.max_price)
    dp.register_message_handler(callback=set_phone, content_types='text',
                                state=OrderStateGroup.phone)
