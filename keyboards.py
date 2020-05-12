from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

rps_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Rock"),
            KeyboardButton(text="Paper"),
            KeyboardButton(text="Scissors")
        ],
    ],
    resize_keyboard=True
)

new_round_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="New round")
        ],
    ],
    resize_keyboard=True
)

answer_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Yes"),
            KeyboardButton(text="No")
        ],
    ],
    resize_keyboard=True
)

func_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/game"),
            KeyboardButton(text="/score")
        ],
    ],
    resize_keyboard=True
)
