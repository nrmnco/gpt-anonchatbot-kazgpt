import asyncio

import logging

from aiogram.types import BotCommand

from handlers import setup_message_routers
from callbacks import setup_callbacks_routers

from database.models import async_main

from src import dp, bot

async def main() -> None:
    
    await async_main()
    bot_commands = [
        BotCommand(command="/start", description="Start"),
        BotCommand(command="/stop_chatting", description="stop_chatting"),
        BotCommand(command="/next", description="next"),
        BotCommand(command="/profile", description="profile"),
        BotCommand(command="/add_friend", description="add_friend"),
        BotCommand(command="/write_to_friend", description="write_to_friend"),
        BotCommand(command="/users_online", description="users_online")
    ]
    await bot.set_my_commands(bot_commands)

    message_routers = setup_message_routers()
    callback_routers = setup_callbacks_routers()
    dp.include_router(message_routers)
    dp.include_router(callback_routers)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # try:
    #     asyncio.run(main())
    # except:
    #     print("exit")
    asyncio.run(main())