from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    entering = State()
    choosing = State()
