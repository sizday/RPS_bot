from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

answer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Rock", callback_data="yes"),
            InlineKeyboardButton(text="Paper", callback_data="no"),
        ],
    ]
)
