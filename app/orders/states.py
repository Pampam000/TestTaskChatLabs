from aiogram.dispatcher.filters.state import State, StatesGroup


class OrderStateGroup(StatesGroup):
    business_name = State()
    platform_name = State()
    min_price = State()
    max_price = State()
    phone = State()
