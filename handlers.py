import random

from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from load_all import bot, dp, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_LOSE = "SELECT count_loss FROM users WHERE chat_id = $1"
    CHECK_WIN = "SELECT count_win FROM users WHERE chat_id = $1"

    async def add_new_user(self):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_lose(self):
        command = self.CHECK_LOSE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_win(self):
        command = self.CHECK_WIN
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await db.add_new_user()
    count_users = await db.count_users()

    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    win = await db.check_win()
    lose = await db.check_lose()
    text += f"""
    Сейчас в базе {count_users} человек!
    Ваш счёт: {win}:{lose}.
    """
    # user_link = f"https://t.me/{bot_username}?start={id}"
    await bot.send_message(chat_id, text)
