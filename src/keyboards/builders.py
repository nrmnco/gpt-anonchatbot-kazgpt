from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from src.database.requests import get_friends
async def friends_list(tg_id):
    keyboard = InlineKeyboardBuilder()
    friends = (await get_friends(tg_id)).friends
    for id in friends:
        keyboard.add(InlineKeyboardButton(text=friends[id], callback_data=id))
    return keyboard.adjust(2).as_markup()
