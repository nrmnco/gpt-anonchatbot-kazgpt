import asyncio

import logging

from src.handlers import setup_message_routers
from src.callbacks import setup_callbacks_routers

from src.database.models import async_main

from src.bot import dp, bot

async def main() -> None:
    
    await async_main()

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