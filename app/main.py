import uvloop
from aiogram.utils import executor

from app.admin import handlers as admin_handlers
from app.bot import handlers
from app.bot import wrong_handlers
from app.bot.create_bot import dp, set_bot_commands
from app.orders import handlers as orders_handlers
from app.orders import wrong_handlers as wrong_orders_handlers
from app.payments import handlers as payments_handlers
from app.payments import wrong_handlers as wrong_payments_handlers

handlers.register_handlers(dp=dp)
orders_handlers.register_handlers(dp=dp)
payments_handlers.register_handlers(dp=dp)
admin_handlers.register_handlers(dp=dp)

wrong_payments_handlers.register_handlers(dp=dp)
wrong_orders_handlers.register_handlers(dp=dp)
wrong_handlers.register_handlers(dp=dp)


async def on_startup(_):
    await set_bot_commands()


if __name__ == '__main__':
    uvloop.install()
    executor.start_polling(dispatcher=dp, skip_updates=True,
                           on_startup=on_startup)
