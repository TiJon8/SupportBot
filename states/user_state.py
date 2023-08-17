from aiogram.dispatcher.filters.state import StatesGroup, State


class UserStates(StatesGroup):
    writing_message = State()
    waiting_answer_from_support = State()