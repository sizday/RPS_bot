from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database
from config import admin_id
from load_all import dp, bot

db = database.DBCommands()


@dp.message_handler(user_id=admin_id, commands=["count"])
async def count_user(message: types.Message):
    chat_id = message.from_user.id
    count_users = await db.count_users()
    text = f'В базе {count_users} пользователей'
    await bot.send_message(chat_id, text)
