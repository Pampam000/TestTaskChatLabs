from aiogram.types import InlineKeyboardMarkup
from asyncpg import Record

from app.bot.keyboards import create_inline_keyboard
from app.business import crud as business_crud
from app.platforms import crud as platform_crud


async def get_keyboard_with_business_names() -> InlineKeyboardMarkup:
    all_business_names: list[Record] = await \
        business_crud.get_all_business_names()
    all_business_names = [dict(x)['name'] for x in
                          all_business_names]
    keyboard: InlineKeyboardMarkup = create_inline_keyboard(
        buttons=all_business_names)
    return keyboard


async def get_keyboard_with_platforms() -> InlineKeyboardMarkup:
    all_platforms: list[Record] = await \
        platform_crud.get_all_platform_names()
    all_platforms = [dict(x)['name'] for x in
                     all_platforms]
    keyboard: InlineKeyboardMarkup = create_inline_keyboard(
        buttons=all_platforms)
    return keyboard
