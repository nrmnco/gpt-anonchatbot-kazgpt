from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from src.database.requests import delete_from_queue

router = Router()

@router.callback_query(F.data == "search_stop")
async def search_stop(cb: CallbackQuery, state:FSMContext):
    await cb.answer('')
    await delete_from_queue(cb.from_user.id)
    await cb.message.answer(text="❌ Поиск остановлен")
    await state.clear()
