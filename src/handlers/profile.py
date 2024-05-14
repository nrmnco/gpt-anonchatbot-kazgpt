from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, or_f
from aiogram.fsm.context import FSMContext

from src.states import MainState
from src.keyboards.reply import profile_kb, main_kb
from src.database.requests import get_bio, update_bio

router = Router()

@router.message(or_f(Command('profile'), F.text == "🍪 Профиль"))
async def profile(message: Message, state: FSMContext) -> None:
    await state.set_state(MainState.profile)
    bio = await get_bio(message.from_user.id)
    await message.answer(f"Ваш био: {bio}\nВыберите что хотите сделать", reply_markup=profile_kb)

@router.message(MainState.change_bio)
async def change_bio(message: Message, state: FSMContext) -> None:
    await update_bio(message.from_user.id, message.text)
    await state.clear()
    await message.answer("Био изменен\nНачинай общение командой /next в меню слева  или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)

