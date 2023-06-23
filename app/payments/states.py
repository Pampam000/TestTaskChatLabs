from aiogram.dispatcher.filters.state import State, StatesGroup


class PaymentStateGroup(StatesGroup):
    choose_amount = State()
    pay = State()