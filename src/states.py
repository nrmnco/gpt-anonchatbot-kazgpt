
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    start = State()
    registration = State()
    chatting = State()
    searching = State()
    change_bio = State()
    profile = State()