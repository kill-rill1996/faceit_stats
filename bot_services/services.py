import os
import requests
from typing import List, Dict


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

