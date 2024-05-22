from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.database.requests import get_interlocutor_id, add_friend, get_friends
from src.keyboards.reply import add_friend_kb
from src.keyboards.builders import friends_list
from src.states import MainState

router = Router()

@router.message(Command("add_friend"))
async def manage_friends(message: Message):
    friends_object = await get_friends(message.from_user.id)
    await message.answer("Заявка на добавление в друзья отправлена пользователю. Ждемс . . .")
    if friends_object:
        if len(friends_object.friends) <= 5:
            interlocutor = await get_interlocutor_id(message.from_user.id)
            await message.bot.send_message(chat_id=interlocutor,
                                           text="Пользователь хочет добавить Вас в друзья",
                                           reply_markup=add_friend_kb)
        else:
            await message.answer("Достигнут лимит друзей (5 пользователей). Чтобы добавить данного пользователя сначала удалите одного из имеющихся контактов через /delete_friend")
    else:
        interlocutor = await get_interlocutor_id(message.from_user.id)
        await message.bot.send_message(chat_id=interlocutor,
                                       text="Пользователь хочет добавить Вас в друзья",
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
    await message.answer("С кем вы хотите пообщаться?", reply_markup= await friends_list(message.from_user.id))
    await state.set_state(MainState.permission_to_connect)
    await state.update_data(id=message.from_user.id)

@router.message(Command("delete_friend"))
async def delete_friend(message: Message, state: FSMContext):
    await message.answer("Кого вы хотите удалить?", reply_markup= await friends_list(message.from_user.id))
    await state.set_state(MainState.delete_friend)


