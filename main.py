import asyncio
import logging 
from aiogram import Bot, Dispatcher
from config import TOKEN
from app.client_handlers import router
from app.admin_handlers import router_admin
from app.database.models import async_main


async def main(): 
    await async_main()
    bot = Bot(token = TOKEN)
    dp = Dispatcher()
    dp.include_routers(router, router_admin)
    await dp.start_polling(bot)

if __name__ == '__main__': 
    logging.basicConfig(level = logging.INFO)
    try: 
        asyncio.run(main())
    except KeyboardInterrupt: 
        print('Exit')