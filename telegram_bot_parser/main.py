from aiogram.utils import executor
from create_bot import dp
import asyncio
from handlers import *
from threading_rn.thread_news import check_process


start_user.register_handler_start_user_process(dp)

async def on_startup(dp):
    await dp.start_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check_process())
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)