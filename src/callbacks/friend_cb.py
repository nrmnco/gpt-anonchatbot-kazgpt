from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from aiogram import Router, F
from aiogram.fsm.context import FSMContext

from src import dp
from src.database.requests import get_interlocutor_id, get_friends, is_in_session, add_to_queue, get_random_record, \
    get_bio, add_session
from src.handlers.chat_commands import stop_chatting
from src.keyboards.reply import permission_kb, search_kb
from src.states import MainState

router = Router()

@router.callback_query(F.data == "accept")
async def accept_friend(cb: CallbackQuery, state:FSMContext):
    await cb.answer('')
    interlocutor = await get_interlocutor_id(cb.from_user.id)
    await cb.message.answer("Придумайте ему никнейм")
    await cb.message.bot.send_message(chat_id=interlocutor,
                                   text="Придумайте ему никнейм")
    await state.set_state(MainState.nickname)
    await dp.fsm.get_context(cb.message.bot, user_id=interlocutor, chat_id=interlocutor).set_state(MainState.nickname)

@router.callback_query(F.data == "decline")
async def decline_friend(cb: CallbackQuery):
    interlocutor = await get_interlocutor_id(cb.from_user.id)
    await cb.answer('')
    await cb.message.answer("Вы отказали предложению о дружбе")
    await cb.message.bot.send_message(chat_id=interlocutor,
                                   text="Ваше предложение о дружбе отклонили")

@router.callback_query(MainState.permission_to_connect)
async def permission_to_connect(cb: CallbackQuery, state: FSMContext):
    await cb.answer('')
    data = await state.get_data()
    interlocutor_id = int(cb.data)
    friends = await get_friends(interlocutor_id)
    nickname = friends[str(data["id"])]
    await cb.message.bot.send_message(chat_id=interlocutor_id,text=f"{nickname} хочет общаться с вами", reply_markup=permission_kb)
    await state.clear()
    await dp.fsm.get_context(cb.message.bot, user_id=interlocutor_id, chat_id=interlocutor_id).storage.set_data(key=StorageKey(bot_id=cb.bot.id, chat_id=interlocutor_id, user_id=interlocutor_id), data=data)


@router.callback_query(F.data == "perm_accept")
async def create_friend_session(cb: CallbackQuery, state: FSMContext):
    print(cb.from_user.id)
    await cb.answer('')
    try:
        await stop_chatting(cb)
    except:
        pass

    data = await state.storage.get_data(key=StorageKey(bot_id=cb.bot.id, user_id=cb.from_user.id, chat_id=cb.from_user.id))
    interlocutor = data["id"]

    interlocutor_bio = await get_bio(interlocutor)
    user_bio = await get_bio(cb.from_user.id)
    await add_session(cb.from_user.id, interlocutor)
    await cb.message.answer(f"Собеседник найден 🌝\nВот его био: {interlocutor_bio}", reply_markup=ReplyKeyboardRemove())
    await cb.message.bot.send_message(chat_id=interlocutor, text=f"Собеседник найден 🌝\nВот его био: {user_bio}", reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await dp.fsm.get_context(cb.message.bot, user_id=interlocutor, chat_id=interlocutor).set_state(await state.clear())

@router.callback_query(F.data == "perm_decline")
async def denied_permission(cb: CallbackQuery, state: FSMContext):
    await cb.answer()
    interlocutor_id = await state.get_data()
    await cb.message.bot.send_message(chat_id=interlocutor_id["id"], text="Вам отказали в общении")
    await state.clear()