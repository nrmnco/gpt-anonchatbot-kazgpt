from aiogram import Router, F
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext

from src import bot
from src.middlewares.check_subscription import CheckSubscription
from src.states import MainState
from src.keyboards.reply import main_kb, reg_kb

import src.database.requests as rq

router = Router()
router.message.middleware(CheckSubscription())

@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    if await rq.check_user(message.from_user.id):
        await message.answer(text="Начинай общение командой /next в меню слева или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)
    else:
        await message.answer(text="Привет! Напиши про себя небольшое био. Он будет отображаться твоим собеседникам 🖖")
        await state.set_state(MainState.registration)


@router.message(MainState.registration)
async def reg_two(message: Message, state: FSMContext) -> None:
    await state.update_data(bio=message.text)
    data = await state.get_data()
    await rq.set_user(message.from_user.id, data["bio"])
    await state.clear()
    await message.answer(text="Начинай общение командой /next в меню слева или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)
