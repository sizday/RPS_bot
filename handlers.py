import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text, CommandStart
from keyboards import rps_menu, new_round_menu, answer_keyboard
from state import Game
import database
from load_all import bot, dp

db = database.DBCommands()


@dp.message_handler(CommandStart())
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    user = await db.add_new_user()
    text = f'Приветствую вас, {user.full_name}'
    await bot.send_message(chat_id, text)


@dp.message_handler(commands=["score"])
async def count_user(message: types.Message):
    chat_id = message.from_user.id
    text = await db.show_score()
    await bot.send_message(chat_id, text)


@dp.message_handler(Text(equals='No'))
async def end_game(message: Message):
    await bot.send_message(message.from_user.id, "Thanks for game")
    await message.edit_reply_markup()


@dp.message_handler(Text(equals='Yes'))
async def new_game(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "New game started!")
    await state.update_data(
        {"round_number": 1,
         "pc_score": 0,
         "player_score": 0,
         "pc_select": 0,
         "player_select": 0})
    await bot.send_message(message.from_user.id, "Enter for start new game", reply_markup=new_round_menu)
    await Game.entering.set()


@dp.message_handler(Command('game'), state=None)
async def start_game(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "ROCK PAPER SCISSORS")
    await bot.send_message(message.from_user.id, "Start game!")
    await state.update_data(
        {"round_number": 1,
         "pc_score": 0,
         "player_score": 0,
         "pc_select": 0,
         "player_select": 0})
    await bot.send_message(message.from_user.id, "Enter for start", reply_markup=new_round_menu)
    await Game.entering.set()


@dp.message_handler(state=Game.entering)
async def game(message: Message, state: FSMContext):
    names = ["rock", "paper", "scissors"]
    data = await state.get_data()
    round_number = data.get("round_number")
    pc_score = data.get("pc_score")
    player_score = data.get("player_score")
    if pc_score < 3 and player_score < 3:
        pc_select = (names[random.randint(0, len(names)-1)])
        await bot.send_message(message.from_user.id, f"Round №{round_number}")
        round_number += 1
        await bot.send_message(message.from_user.id, "Your choice", reply_markup=rps_menu)
        await state.update_data(
            {"round_number": round_number,
             "pc_select": pc_select})
        await Game.choosing.set()


@dp.message_handler(state=Game.choosing)
async def get_object(message: Message, state: FSMContext):
    data = await state.get_data()
    pc_score = data.get("pc_score")
    player_score = data.get("player_score")
    pc_select = data.get("pc_select")
    player_select = message.text.lower()
    if player_select != "rock" and player_select != "paper" and player_select != "scissors":
        player_select = "error"
    await bot.send_message(message.from_user.id, f"Your choice = {player_select}\nMy choice = {pc_select}")
    if player_select == "error":
        pc_score += 1
    elif (pc_select == "rock") and (player_select == "paper"):
        player_score += 1
    elif (pc_select == "rock") and (player_select == "scissors"):
        pc_score += 1
    elif (pc_select == "paper") and (player_select == "rock"):
        pc_score += 1
    elif (pc_select == "paper") and (player_select == "scissors"):
        player_score += 1
    elif (pc_select == "scissors") and (player_select == "paper"):
        pc_score += 1
    elif (pc_select == "scissors") and (player_select == "rock"):
        player_score += 1
    else:
        await bot.send_message(message.from_user.id, "Draw in this round")
    await bot.send_message(message.from_user.id, f"Current score: {player_score}:{pc_score}")
    if pc_score == 3 or player_score == 3:
        if pc_score == 3:
            await db.add_lose()
            await bot.send_message(message.from_user.id, "Game over. I'm win, but I love you very much")
        else:
            await db.add_win()
            await bot.send_message(message.from_user.id, "Game over. You are win. I know that you are best!!!")
        await bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
        await bot.send_message(message.from_user.id, "Do you want play again?", reply_markup=answer_keyboard)
        await state.reset_state()
    else:
        await bot.send_message(message.from_user.id, "Enter for continue", reply_markup=new_round_menu)
        await state.update_data(
            {"pc_score": pc_score,
             "player_score": player_score})
        await Game.entering.set()


@dp.message_handler(Text)
async def other_text(message: Message):
    if message.text.lower() == "hi":
        await bot.send_message(message.from_user.id, "Hello! I am TestBot. How can i help you?")
    elif message.text.lower() == "how are you?":
        await bot.send_message(message.from_user.id, "Плохо. Скинь смешняфку")
    elif message.text.lower() == "love":
        await bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')
    elif message.text.lower() == "bye":
        await bot.send_message(message.from_user.id, "I don't love you((")
    else:
        await bot.send_message(message.from_user.id, "Sorry, i dont understand you.")


@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: Message):
    await bot.send_message(message.from_user.id, "Смефно")
    print(message)


@dp.message_handler(content_types=['audio'])
async def send_sticker(message: Message):
    await bot.send_message(message.from_user.id, "Я тупой. Давай текст")
    print(message)
