from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command, or_f, StateFilter
from aiogram.fsm.context import FSMContext

from src import dp
from src.keyboards.reply import main_kb, search_kb
from src.database.requests import add_session, get_random_record, add_to_queue, get_interlocutor_id, delete_session, get_bio, is_in_session

router = Router()


@router.message(or_f(Command("search"), F.text == "☕ Искать собеседника"))
async def search_interlocutor(message: Message, state: FSMContext) -> None:
    if await is_in_session(message.from_user.id):
        await message.answer("У тебя уже есть собеседник!!")
    else:
        await message.answer("Ищем собеседника . . .", reply_markup=search_kb)
        await add_to_queue(message.from_user.id)
        interlocutor = await get_random_record(message.from_user.id)
        if interlocutor:
            interlocutor_bio = await get_bio(interlocutor.user_tg_id)
            user_bio = await get_bio(message.from_user.id)
            await add_session(message.from_user.id, interlocutor.user_tg_id)
            await message.answer(f"Собеседник найден 🌝\nВот его био: {interlocutor_bio}", reply_markup=ReplyKeyboardRemove())
            await message.bot.send_message(chat_id=interlocutor.user_tg_id, text=f"Собеседник найден 🌝\nВот его био: {user_bio}", reply_markup=ReplyKeyboardRemove())
            await state.clear()
            await dp.fsm.get_context(message.bot, user_id=interlocutor.user_tg_id, chat_id=interlocutor.user_tg_id).clear()


@router.message(or_f(Command("stop_chatting"), F.text == "❌ Покинуть Чат"))
async def stop_chatting(message: Message):
    interlocutor = await get_interlocutor_id(message.from_user.id)
    await message.answer(text="❌ Диалог закончен", reply_markup=main_kb)
    await message.bot.send_message(chat_id=interlocutor, text="❌ Диалог закончен", reply_markup=main_kb)
    await delete_session(message.from_user.id)
    await dp.fsm.get_context(message.bot, user_id=interlocutor, chat_id=interlocutor).clear()
    await dp.fsm.get_context(message.bot, user_id=message.from_user.id, chat_id=message.from_user.id).clear()

@router.message(or_f(Command("next"), F.text == "🔎 Следующий чат"))
async def next_chatting(message: Message, state: FSMContext):
    try:
        await stop_chatting(message)
    except:
        pass
    if await is_in_session(message.from_user.id):
        await message.answer("У тебя уже есть собеседник!!")
    else:
        await message.answer("Ищем собеседника . . .", reply_markup=search_kb)
        await add_to_queue(message.from_user.id)
        interlocutor = await get_random_record(message.from_user.id)
        if interlocutor:
            interlocutor_bio = await get_bio(interlocutor.user_tg_id)
            user_bio = await get_bio(message.from_user.id)
            await add_session(message.from_user.id, interlocutor.user_tg_id)
            await message.answer(f"Собеседник найден 🌝\nВот его био: {interlocutor_bio}", reply_markup=ReplyKeyboardRemove())
            await message.bot.send_message(chat_id=interlocutor.user_tg_id, text=f"Собеседник найден 🌝\nВот его био: {user_bio}", reply_markup=ReplyKeyboardRemove())
            await state.clear()
            await dp.fsm.get_context(message.bot, user_id=interlocutor.user_tg_id, chat_id=interlocutor.user_tg_id).set_state(await state.clear())




