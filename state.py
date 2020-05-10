from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    round = State()
    entering = State()
    choosing = State()