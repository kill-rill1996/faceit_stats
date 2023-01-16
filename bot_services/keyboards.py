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
    buttons = [InlineKeyboardButton(text=player, callback_data=player) for player in players]
    inline_keyboard.add(*buttons)
    return inline_keyboard


def create_players_stats_inline_keyboard(nickname: str) -> InlineKeyboardMarkup:
    """Для формирования динамической inline keyboard у конкретного игрока"""
    stats_button = InlineKeyboardButton(text='Статистика', callback_data=f'info_{nickname}')
    matches_button = InlineKeyboardButton(text='Матчи', callback_data=f'matches_{nickname}')
    last_matches_stats_button = InlineKeyboardButton(text='За последние 20 матчей', callback_data=f'lastmatches_{nickname}')
    player_keyboard = InlineKeyboardMarkup(row_width=2)
    player_keyboard.add(stats_button, matches_button, last_matches_stats_button)
    return player_keyboard



