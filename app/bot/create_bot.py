from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.types import BotCommand

from app.config import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN, timeout=5)
storage: MemoryStorage = MemoryStorage()
dp: Dispatcher = Dispatcher(bot=bot, storage=storage)


async def set_bot_commands():
    await dp.bot.set_my_commands([
        BotCommand("start", "(Пере)запустить бота"),
        BotCommand("help", 'Получить справку и выйти на главную')
    ])
