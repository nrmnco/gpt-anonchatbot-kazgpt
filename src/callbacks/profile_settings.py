from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from states import MainState
from keyboards.reply import main_kb

router = Router()

@router.callback_query(F.data == "change_bio", MainState.profile)
async def change_bio_cb(cb: CallbackQuery, state:FSMContext):
    await cb.answer('')
    await state.set_state(MainState.change_bio)
    await cb.message.answer("Напишите новое био")

@router.callback_query(F.data == "go_back", MainState.profile)
async def go_back(cb: CallbackQuery, state:FSMContext):
    await cb.answer('')
    await state.clear()
    await cb.message.answer("Начинай общение командой /search или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)

