from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.context import FSMContext

from middlewares.check_subscription import CheckSubscription
from states import MainState
from keyboards.reply import main_kb, reg_kb

import database.requests as rq

router = Router()
router.message.middleware(CheckSubscription())

@router.message(CommandStart())
async def start(message: Message) -> None:
    if await rq.check_user(message.from_user.id):
        await message.answer(text="Привет! Кнопка Профиля еще не работает\nНачинай общение командой /search или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)
    else:
        await message.answer(text="Привет! \nЗарегайся написав /reg или нажав на кнопку 'Зарегистрироваться' ниже", reply_markup=reg_kb)

@router.message(or_f(Command('reg'), F.text == "Зарегистрироваться"))
async def reg_one(message: Message, state: FSMContext) -> None:
    await state.set_state(MainState.registration)
    await message.answer(text="Напиши себе био (без личной информации)")

@router.message(MainState.registration)
async def reg_two(message: Message, state: FSMContext) -> None:
    await state.update_data(bio=message.text)
    data = await state.get_data()
    await rq.set_user(message.from_user.id, data["bio"])
    await state.clear()
    await message.answer(text="Начинай общение командой /search или нажав на кнопку '☕ Искать собеседника' ниже", reply_markup=main_kb)
