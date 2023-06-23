from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ParseMode
from asyncpg import Record

from app.config import HELLO_MESSAGE, ADMIN_HELLO_MESSAGE
from app.logger import logger
from app.users import crud as users_crud
from .keyboards import main_admin_keyboard, main_keyboard


async def start(message: Message, state: FSMContext):
    if state.get_state():
        await state.finish()

    from_user = message.from_user
    username = from_user.username
    logger.debug(f'{username} started bot')

    user: Record = await users_crud.get_user_by_id(user_id=from_user.id)

    msg = HELLO_MESSAGE
    reply_markup = main_keyboard

    if user:
        logger.debug(f'user: {username} found in db, '
                     f'is_admin={user["is_admin"]}')
        if user['is_admin']:
            msg += ADMIN_HELLO_MESSAGE
            reply_markup = main_admin_keyboard

    else:
        logger.debug(f'user: {username} not found in db')
        await users_crud.insert_user(user_id=from_user.id,
                                     username=from_user.username)
    await message.answer(text=msg,
                         reply_markup=reply_markup,
                         parse_mode=ParseMode.MARKDOWN)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start", 'help'], state='*')
