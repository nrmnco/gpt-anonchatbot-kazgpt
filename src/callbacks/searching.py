from aiogram.types import CallbackQuery
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from database.requests import delete_from_queue
from states import MainState

router = Router()

@router.callback_query(F.data == "search_stop", MainState.searching)
async def search_stop(cb: CallbackQuery, state:FSMContext):
    await cb.answer('')
    await delete_from_queue(cb.from_user.id)
    await cb.message.answer(text="Поиск остановлен")
    await state.clear()
