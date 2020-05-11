from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

rps_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Rock"),
            InlineKeyboardButton(text="Paper"),
            InlineKeyboardButton(text="Scissors")
        ],
    ],
    resize_keyboard=True
)

new_round_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="New round")
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
    ],
    resize_keyboard=True
)
