import os
import requests
from typing import List, Dict

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot_services.keyboards import main_keyboard
from database.services import get_all_players_nickname_from_db, add_to_database
from full_statistic import get_full_stats_for_player


def get_stats_for_n_matches(matches_data: List[Dict]) -> Dict:
    player_stat = {
        'avg_deaths': round(sum([match['deaths'] for match in matches_data]) / len(matches_data), 2),
        'avg_kills': round(sum([match['kills'] for match in matches_data]) / len(matches_data), 2),
        'kd': round(sum([match['kills'] for match in matches_data]) / sum([match['deaths'] for match in matches_data]), 2),
        'avg_rating_1': round(sum([match['rating_1'] for match in matches_data]) / len(matches_data), 2),
        'mvps': sum([match['mvps'] for match in matches_data]),
        'hs_count': sum([match['hs_count'] for match in matches_data]),
        'hs_percent': int(round(sum([match['hs_count'] for match in matches_data]) / sum([match['kills'] for match in matches_data]), 2) * 100),
        'aces': sum([match['aces'] for match in matches_data]),
        'quadro_kills': sum([match['quadro_kills'] for match in matches_data]),
        'triple_kills': sum([match['triple_kills'] for match in matches_data]),
        'double_kills': sum([match['double_kills'] for match in matches_data]),
    }
    return player_stat


def get_player_avatar_path(player):
    if os.path.exists(f'players_avatars/{player.faceit_nickname}.jpeg'):
        return f'players_avatars/{player.faceit_nickname}.jpeg'
    else:
        if player.avatar:
            response = requests.get(player.avatar)
            with open(f'players_avatars/{player.faceit_nickname}.jpeg', 'wb') as fd:
                fd.write(response.content)
            return f'players_avatars/{player.faceit_nickname}.jpeg'
        else:
            return 'players_avatars/default.png'


async def get_nickname_faceit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname_faceit'] = message.text

    async with state.proxy() as data:
        if data['nickname_faceit'] not in get_all_players_nickname_from_db():
            await message.answer('Идет сбор статистики, подождите...📈')
            player_full_stat = get_full_stats_for_player(data['nickname_faceit'])
            add_to_database(player_full_stat)
            # with open(f'{PLAYERS_LIST}', 'a') as f:
            #     f.write(f'\n{data["nickname_faceit"]}')
            await message.answer('Ваш nickname добавлен в базу данных.', reply_markup=main_keyboard)
        else:
            await message.answer('Ваш nickname уже был добавлен в базу.', reply_markup=main_keyboard)

    await state.finish()