from aiogram import types
from gino import Gino
from gino.schema import GinoSchemaVisitor
from sqlalchemy import (Column, Integer, BigInteger, String, Sequence)
from sqlalchemy import sql

from config import db_pass, db_user, host

db = Gino()


class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    user_id = Column(BigInteger)
    full_name = Column(String(100))
    username = Column(String(50))
    win_score = Column(Integer)
    lose_score = Column(Integer)
    query: sql.Select


class DBCommands:

    async def get_user(self, user_id) -> User:
        user = await User.query.where(User.user_id == user_id).gino.first()
        return user

    async def add_new_user(self) -> User:
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = User()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        new_user.win_score = 0
        new_user.lose_score = 0
        await new_user.create()
        return new_user

    async def count_users(self) -> int:
        total = await db.func.count(User.id).gino.scalar()
        return total

    async def show_score(self) -> str:
        user = types.User.get_current()
        current_user = await self.get_user(user.id)
        win = await current_user.win_score
        lose = await current_user.lose_score
        score = f'Ваш счёт: {win}:{lose}\n' \
                f'Процент побед: {round(win/win+lose*100)}%'
        return score

    async def add_win(self):
        user = types.User.get_current()
        current_user = await self.get_user(user.id)
        current_user.win_score += 1

    async def add_lose(self):
        user = types.User.get_current()
        current_user = await self.get_user(user.id)
        current_user.lose_score += 1


async def create_db():
    await db.set_bind(f'postgresql://{db_user}:{db_pass}@{host}/gino')
    db.gino: GinoSchemaVisitor
    await db.gino.drop_all()
    await db.gino.create_all()