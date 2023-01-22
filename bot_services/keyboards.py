from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


cancel_button = KeyboardButton('Отмена')
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(cancel_button)

players_button = KeyboardButton('Список игроков')
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(players_button)


def create_players_inline_keyboard(players: List) -> InlineKeyboardMarkup:
    """Для формирования динамической inline keyboard со списком всех игроков"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=player, callback_data=f'menu$&*{player}') for player in players]
    inline_keyboard.add(*buttons)
    return inline_keyboard


def create_players_stats_inline_keyboard(nickname: str) -> InlineKeyboardMarkup:
    """Для формирования динамической inline keyboard у конкретного игрока"""
    stats_button = InlineKeyboardButton(text='Полная статистика', callback_data=f'info$&*{nickname}')
    matches_button = InlineKeyboardButton(text='Последние 10 матчей', callback_data=f'matches$&*{nickname}')
    last_matches_stats_button = InlineKeyboardButton(text='Статистика за последние матчи', callback_data=f'last_stats$&*{nickname}')
    player_keyboard = InlineKeyboardMarkup(row_width=2)
    player_keyboard.add(stats_button, matches_button, last_matches_stats_button)
    return player_keyboard


cancel_inline_keyboard = InlineKeyboardMarkup(row_width=3)
ten_matches_inline_button = InlineKeyboardButton(text='10 матчей', callback_data='matchescount_10')
fif_matches_inline_button = InlineKeyboardButton(text='50 матчей', callback_data='matchescount_50')
hund_matches_inline_button = InlineKeyboardButton(text='100 матчей', callback_data='matchescount_100')
cancel_inline_button = InlineKeyboardButton(text='Отмена', callback_data='cancel')
cancel_inline_keyboard.add(ten_matches_inline_button, fif_matches_inline_button, hund_matches_inline_button, cancel_inline_button)


def create_back_inline_keyboard(nickname: str) -> InlineKeyboardMarkup:
    back_inline_keyboard = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text='<<Назад', callback_data=f'menu$&*{nickname}')
    back_inline_keyboard.add(back_button)
    return back_inline_keyboard
