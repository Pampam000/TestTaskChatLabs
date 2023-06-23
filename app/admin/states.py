from aiogram.dispatcher.filters.state import State, StatesGroup


class MailingStateGroup(StatesGroup):
    start = State()
