
from aiogram.fsm.state import State, StatesGroup


class MainState(StatesGroup):
    start = State()
    registration = State()
    nickname = State()
    searching = State()
    change_bio = State()
    profile = State()
    permission_to_connect = State()
    connect_to_friend = State()
    delete_friend = State()