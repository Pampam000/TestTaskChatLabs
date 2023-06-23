from aiogram.types import LabeledPrice

from app.bot.create_bot import bot
from app.config import U_KASSA_TOKEN, PRODUCT_NAME, PRODUCT_DESCRIPTION, \
    PRODUCT_PAYLOAD, PRODUCT_CURRENCY, PRODUCT_PRICE

price = LabeledPrice(label=PRODUCT_NAME, amount=PRODUCT_PRICE)


async def send_invoice(user_id: int, count: int):
    await bot.send_invoice(chat_id=user_id,
                           title=PRODUCT_NAME,
                           description=PRODUCT_DESCRIPTION,
                           payload=PRODUCT_PAYLOAD,
                           provider_token=U_KASSA_TOKEN,
                           currency=PRODUCT_CURRENCY,
                           prices=[price] * count)
