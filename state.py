from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    no_game = State()
    new_game = State()
    entering = State()
    choosing = State()
