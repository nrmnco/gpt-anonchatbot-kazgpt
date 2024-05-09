import asyncio

import logging

from handlers import setup_message_routers
from callbacks import setup_callbacks_routers

from database.models import async_main

from bot import dp, bot

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