from aiogram.types import Message
from create_bot import bot, Dispatcher
from keyboards.markup_user import *
from data.data import connector


async def start_user_process(message:Message):
    await bot.send_message(message.from_user.id, 'Welcome to our news bot', reply_markup=user_markup.menu())
    connector.insert_users(id_chat=message.from_user.id, username=message.from_user.username, status='USER')

def register_handler_start_user_process(dp: Dispatcher):
    dp.register_message_handler(start_user_process, commands='start')
    dp.register_message_handler(start_user_process, text='/')