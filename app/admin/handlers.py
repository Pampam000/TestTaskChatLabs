from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils.exceptions import ChatNotFound
from asyncpg import Record

from app.bot.create_bot import bot
from app.config import SEND_MESSAGE_BUTTON
from app.logger import logger
from app.users import crud as users_crud
from .states import MailingStateGroup


async def start_mailing(message: Message):
    logger.debug(f'{message.from_user.username} started mailing')
    user: Record = await users_crud.get_user_by_id(
        user_id=message.from_user.id)
    if user and user['is_admin']:
        logger.debug(f'{message.from_user.username} is admin')
        await message.answer("Введите сообщение для рассылки")
        await MailingStateGroup.start.set()
    else:
        logger.debug(f'{message.from_user.username} is not admin')
        await message.answer(
            'Выберите опцию для дальнейшего взаимодействия с ботом')


async def send_mailing(message: Message, state: FSMContext):
    logger.debug(f'{message.from_user.username} sending mailing')
    author_id = message.from_user.id
    users_in_mailing: list[Record] = await \
        users_crud.get_all_users_except_sender(user_id=author_id)

    bad_list = []
    for user in users_in_mailing:
        try:
            await bot.send_message(user['id'], message.text)
        except ChatNotFound:
            bad_list.append(f'@{user["username"]}')
    await message.answer("Сообщение отправлено")

    if bad_list:
        logger.debug(f'Список пользователей, удаливших бота: {bad_list}')
        await message.answer('Список пользователей, удаливших бота:\n'
                             f'{bad_list}')

    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(callback=start_mailing, state=None,
                                content_types='text',
                                text=SEND_MESSAGE_BUTTON)
    dp.register_message_handler(callback=send_mailing,
                                state=MailingStateGroup.start,
                                content_types='text')
