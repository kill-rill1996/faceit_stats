from aiogram.dispatcher.filters.state import StatesGroup, State


class FSMStart(StatesGroup):
    nickname = State()


class FSMMatches(StatesGroup):
    matches_count = State()


class FSMCompare(StatesGroup):
    first_player = State()
    second_player = State()

