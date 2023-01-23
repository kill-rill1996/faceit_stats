from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from typing import List


def create_cancel_keyboard() -> ReplyKeyboardMarkup:
    cancel_button = KeyboardButton('Отмена')
    cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    cancel_keyboard.add(cancel_button)
    return cancel_keyboard


def create_main_keyboard() -> ReplyKeyboardMarkup:
    players_button = KeyboardButton('📃 Список игроков')
    add_player_button = KeyboardButton('➕ Добавить нового игрока')
    compare_player_button = KeyboardButton('📊 Сравнить игроков')
    best_players_button = KeyboardButton('🔝 Лучшие игроки')
    main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    main_keyboard.add(players_button, add_player_button, compare_player_button, best_players_button)
    return main_keyboard


def create_players_inline_keyboard(players: List, best_players: bool = True) -> InlineKeyboardMarkup:
    """Для формирования динамической inline keyboard со списком всех игроков"""
    inline_keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(text=player, callback_data=f'menu$&*{player}') for player in players]
    inline_keyboard.add(*buttons)
    if best_players:
        best_players_button = InlineKeyboardButton(text='Лучшие игроки', callback_data=f'best_players$&*')
        inline_keyboard.add(best_players_button)
    return inline_keyboard


def create_players_stats_inline_keyboard(nickname: str) -> InlineKeyboardMarkup:
    """Для формирования динамической inline keyboard у конкретного игрока"""
    stats_button = InlineKeyboardButton(text='Полная статистика', callback_data=f'info$&*{nickname}')
    matches_button = InlineKeyboardButton(text='Последние 20 матчей', callback_data=f'matches$&*{nickname}')
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


def create_best_players_inline_keyboard() -> InlineKeyboardMarkup:
    best_plyaers_categories_keyboard = InlineKeyboardMarkup(row_width=2)
    category_1 = InlineKeyboardButton(text='Rating 1.0', callback_data='best$&*rating')
    category_2 = InlineKeyboardButton(text='Headshots', callback_data='best$&*hs')
    category_3 = InlineKeyboardButton(text='K/D', callback_data='best$&*kd')
    category_4 = InlineKeyboardButton(text='Aces', callback_data='best$&*aces')
    category_5 = InlineKeyboardButton(text='ELO', callback_data='best$&*elo')
    category_6 = InlineKeyboardButton(text='AVG Kills', callback_data='best$&*avg_kills')
    cancel_button_best_players = InlineKeyboardButton(text='<<Назад', callback_data='best$&*cancel')
    best_plyaers_categories_keyboard.add(category_1, category_2, category_3, category_4,
                                         category_5, category_6, cancel_button_best_players)
    return best_plyaers_categories_keyboard