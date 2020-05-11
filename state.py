from aiogram.dispatcher.filters.state import StatesGroup, State


class Game(StatesGroup):
    entering = State()
    choosing = State()
    new_game = State()
    no_game = State()
    yes_game = State()
