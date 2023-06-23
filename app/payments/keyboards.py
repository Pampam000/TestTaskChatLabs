from aiogram.types import InlineKeyboardMarkup

from app.bot.keyboards import create_inline_keyboard
from app.config import PAYMENT_INLINE_BUTTONS


def get_keyboard() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = create_inline_keyboard(
        buttons=PAYMENT_INLINE_BUTTONS)
    return keyboard
