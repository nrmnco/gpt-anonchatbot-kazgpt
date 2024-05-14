from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext

from src.database.requests import get_interlocutor_id, add_friend, get_friends
from src.keyboards.reply import add_friend_kb, permission_kb
from src.keyboards.builders import friends_list
from src.states import MainState

router = Router()

@router.message(Command("add_friend"))
async def manage_friends(message: Message):
    interlocutor = await get_interlocutor_id(message.from_user.id)
    await message.bot.send_message(chat_id=interlocutor,
                                   text="Вас хотят добавить в друзья",
                                   reply_markup=add_friend_kb)

@router.message(MainState.nickname)
async def adding_friend(message: Message, state: FSMContext):
    nickname = message.text
    interlocutor = await get_interlocutor_id(message.from_user.id)
    await add_friend(message.from_user.id, interlocutor, nickname)
    await message.answer("Друг добавлен")
    await state.clear()

@router.message(Command("write_to_friend"))
async def connect_with_friend(message: Message, state: FSMContext):
    friends = await get_friends(message.from_user.id)
    await message.answer("С кем вы хотите пообщаться?", reply_markup= await friends_list(message.from_user.id))
    await state.set_state(MainState.permission_to_connect)
    await state.update_data(id=message.from_user.id)



