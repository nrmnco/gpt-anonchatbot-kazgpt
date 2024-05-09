from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

from bot import dp
from states import MainState
from keyboards.reply import main_kb, search_kb, chatting_kb
from database.requests import add_session, get_random_record, add_to_queue, get_interlocutor_id, delete_session, get_bio

router = Router()


@router.message(or_f(Command("search"), F.text == "☕ Искать собеседника"))
async def search_interlocutor(message: Message, state: FSMContext) -> None:
    await state.set_state(MainState.searching)

    await message.answer("Ищем собеседника", reply_markup=search_kb)
    await add_to_queue(message.from_user.id)
    interlocutor = await get_random_record(message.from_user.id)
    if interlocutor:
        interlocutor_bio = await get_bio(interlocutor.user_tg_id)
        user_bio = await get_bio(message.from_user.id)
        await add_session(message.from_user.id, interlocutor.user_tg_id)
        await message.answer(f"Собеседник найден\nЕго био: {interlocutor_bio}", reply_markup=chatting_kb)
        await message.bot.send_message(chat_id=interlocutor.user_tg_id, text=f"Собеседник найден\nЕго био: {user_bio}", reply_markup=chatting_kb)
        await state.set_state(MainState.chatting)
        await dp.fsm.get_context(message.bot, user_id=interlocutor.user_tg_id, chat_id=interlocutor.user_tg_id).set_state(MainState.chatting)
        

@router.message(MainState.searching)
async def search_error(message: Message):
    await message.answer("Вы уже находитесь в поиске собеседника", reply_markup=search_kb)

@router.message(Command("stop_chatting"), MainState.chatting)
async def stop_chatting(message: Message):
    interlocutor = await get_interlocutor_id(message.from_user.id)
    await message.answer(text="Диалог закончен", reply_markup=main_kb)
    await message.bot.send_message(chat_id=interlocutor, text="Диалог закончен", reply_markup=main_kb)
    await delete_session(message.from_user.id)
    await dp.fsm.get_context(message.bot, user_id=interlocutor, chat_id=interlocutor).clear()
    await dp.fsm.get_context(message.bot, user_id=message.from_user.id, chat_id=message.from_user.id).clear()

@dp.message(MainState.chatting, Command("next"))
async def next_chatting(message: Message, state: FSMContext):
    await stop_chatting(message)

    await state.set_state(MainState.searching)
    await message.answer("Ищем собеседника", reply_markup=search_kb)
    await add_to_queue(message.from_user.id)
    interlocutor = await get_random_record(message.from_user.id)
    if interlocutor:
        await add_session(message.from_user.id, interlocutor.user_tg_id)
        await message.answer("Собеседник найден", reply_markup=chatting_kb)
        await message.bot.send_message(chat_id=interlocutor.user_tg_id, text="Собеседник найден", reply_markup=chatting_kb)
        await state.set_state(MainState.chatting)
        await dp.fsm.get_context(message.bot, user_id=interlocutor.user_tg_id, chat_id=interlocutor.user_tg_id).set_state(MainState.chatting)
        
