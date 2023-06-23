from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardButton, InlineKeyboardMarkup

from app.config import MAIN_BUTTONS, ADMIN_BUTTONS


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for button in MAIN_BUTTONS:
        keyboard.insert(KeyboardButton(text=button))

    return keyboard


def create_main_admin_keyboard() -> ReplyKeyboardMarkup:
    keyboard = get_main_keyboard()
    for button in ADMIN_BUTTONS:
        keyboard.insert(KeyboardButton(text=button))
    return keyboard


def create_inline_keyboard(buttons: list[str]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    for button in buttons:
        keyboard.add(InlineKeyboardButton(text=button,
                                          callback_data=button))
    return keyboard


main_keyboard = get_main_keyboard()

main_admin_keyboard = create_main_admin_keyboard()
