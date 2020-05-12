from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import database
from config import admin_id
from load_all import dp, bot

db = database.DBCommands()


@dp.message_handler(commands=["count"])
async def count_user(message: types.Message):
    chat_id = message.from_user.id
    await bot.send_message(chat_id, isinstance(chat_id, int))
    await bot.send_message(chat_id, isinstance(admin_id, int))
    if message.from_user.id == admin_id:
        count_users = await db.count_users()
        text = f'В базе {count_users} пользователей'
        await bot.send_message(chat_id, text)
