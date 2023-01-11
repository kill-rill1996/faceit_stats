from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List

cancel_button = KeyboardButton('Отмена')
players_button = KeyboardButton('Список игроков')


cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(cancel_button)

main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(players_button)


def create_players_inline_keyboard(players: List) -> InlineKeyboardMarkup:
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=player, callback_data=player) for player in players]
    inline_keyboard.add(*buttons)
    return inline_keyboard


