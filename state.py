from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    pregame = State()
    entering = State()
    choosing = State()