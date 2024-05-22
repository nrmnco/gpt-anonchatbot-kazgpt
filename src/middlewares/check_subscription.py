from typing import Callable, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message

from src import bot


class CheckSubscription(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any]
    ) -> Any:
        statuses = ["creator", "administrator", "member"]
        try:
            result = await bot.get_chat_member(chat_id="@nukazgpt", user_id=event.from_user.id)
            print(result.status.value)
            if result.status.value in statuses:
                return await handler(event, data)
        except:
            await event.answer("Сначала Подпишись на @nukazgpt и попробуй заного.\n\n"
                               "☂️ New Your Times - Газета-канал о Нушниках")
            return
        await event.answer("Подпишись на @nukazgpt и попробуй заного")
        