from typing import Dict, Any, List, Tuple

import config
from urls import send_request


def parse_required_player_info(data: Dict) -> Dict[str, Any]:
    """Собирает основную информацию об аккаунте"""

    parsed_data = {
        'faceit_id': data['player_id'],
        'faceit_nickname': data['nickname'],
        'steam_nickname': data['games']['cs2']['game_player_name'],
        'avatar': data['avatar'],
        'country': data['country'],
        'faceit_lvl': data['games']['cs2']['skill_level'],
        'faceit_elo': data['games']['cs2']['faceit_elo']
    }
    return parsed_data


def parse_required_stats(data: Dict) -> Dict[str, Any]:
    """Собирает общую информацию о статистике игрока в csgo"""

    rounds_count = sum([int(segment['stats']['Rounds']) for segment in data['segments']])
    kills_count = sum([int(segment['stats']['Kills']) for segment in data['segments']])
    headshots_count = sum([int(segment['stats']['Headshots']) for segment in data['segments']])
    deaths_count = sum([int(segment['stats']['Deaths']) for segment in data['segments']])
    aces = sum([int(segment['stats']['Penta Kills']) for segment in data['segments']])
    quadro_kills = sum([int(segment['stats']['Quadro Kills']) for segment in data['segments']])
    triple_kills = sum([int(segment['stats']['Triple Kills']) for segment in data['segments']])
    double_kills = round((kills_count - aces * 5 - quadro_kills * 4 - triple_kills * 3) * 0.18)
    single_kills = kills_count - aces * 5 - quadro_kills * 4 - triple_kills * 3 - double_kills * 2
    mvps = sum([int(segment['stats']['MVPs']) for segment in data['segments']])
    avg_kpr = kills_count / rounds_count
    avg_spr = (rounds_count - deaths_count) / rounds_count
    avg_rmk = (single_kills + double_kills * 4 + triple_kills * 9 + quadro_kills * 16 + aces * 25) / rounds_count

    parsed_data = {
        'avg_kd': float(data['lifetime']['Average K/D Ratio']),
        'matches_count': int(data['lifetime']['Matches']),
        'rounds_count': rounds_count,
        'avg_hs_percent': int(data['lifetime']["Average Headshots %"]),
        'wins_count': int(data['lifetime']["Wins"]),
        'hs_count': headshots_count,
        'winrate': int(data['lifetime']["Win Rate %"]),
        'kills_count': kills_count,
        'deaths_count': deaths_count,
        'aces': aces,
        'quadro_kills': quadro_kills,
        'triple_kills': triple_kills,
        'double_kills': double_kills,
        'single_kills': single_kills,
        'mvps': mvps,
        'avg_kpr': avg_kpr,
        'avg_spr': avg_spr,
        'avg_rmk': avg_rmk,
        'avg_kills': round(kills_count / int(data['lifetime']['Matches']))
    }
    return parsed_data


def calculate_rating_1_per_match(match_stats: Dict) -> float:
    """Рассчитывает рейтинг 1.0 за карту"""

    kill_rating = match_stats['kills'] / match_stats['rounds'] / config.AVG_KPR
    survival_rating = (match_stats['rounds'] - match_stats['deaths']) / match_stats['rounds'] / config.AVG_SPR
    rmk_rating = (match_stats['single_kills'] + match_stats['double_kills'] * 4 + match_stats['triple_kills'] * 9 +
                 match_stats['quadro_kills'] * 16 + match_stats['aces'] * 25) / match_stats['rounds'] / config.AVG_RMK
    rating_1 = round((kill_rating + 0.7 * survival_rating + rmk_rating) / 2.7, 2)

    return rating_1


def get_match_winner(data: Dict, player_id: str) -> bool:
    """Возвращает победу игрока - True или поражение - False"""
    winner_id = data['rounds'][0]['round_stats']['Winner']
    team1 = [player['player_id'] for player in data['rounds'][0]['teams'][0]['players']]
    if data['rounds'][0]['teams'][0]['team_id'] == winner_id:
        if player_id in team1:
            return True
        return False
    else:
        if player_id not in team1:
            return True
        return False


def get_player_stats_in_match(data: Dict, player_id: str) -> Dict[str, Any]:
    """Собирает статистику переданного игрока за один матч"""

    match_stats = {}
    for player in data['rounds'][0]['teams'][0]['players'] + data['rounds'][0]['teams'][1]['players']:
        if player['player_id'] == player_id:
            match_stats = {
                'result': get_match_winner(data, player_id),
                'score': data['rounds'][0]['round_stats']['Score'],
                'aces': int(player['player_stats']["Penta Kills"]),
                'quadro_kills': int(player['player_stats']["Quadro Kills"]),
                'triple_kills': int(player['player_stats']["Triple Kills"]),
                'kr': float(player['player_stats']['K/R Ratio']),
                'sr': (int(data['rounds'][0]['round_stats']['Rounds']) - int(
                    player['player_stats']['Deaths']))
                                 / int(data['rounds'][0]['round_stats']['Rounds']),
                'kills': int(player['player_stats']['Kills']),
                'deaths': int(player['player_stats']['Deaths']) if int(player['player_stats']['Deaths']) != 0 else 1,
                'rounds': int(data['rounds'][0]['round_stats']['Rounds']),
                'hs_percent': int(player['player_stats']["Headshots %"]),
                'hs_count': int(player['player_stats']["Headshots"]),
                'mvps': int(player['player_stats']["MVPs"])
            }

            match_stats['kd'] = round(int(player['player_stats']['Kills']) / match_stats['deaths'], 2)

            match_stats['double_kills'] = round((match_stats['kills'] -
                                                  match_stats['aces'] * 5 -
                                                  match_stats['quadro_kills'] * 4 -
                                                  match_stats['triple_kills'] * 3) * 0.18
                                                 )
            match_stats['single_kills'] = match_stats['kills'] - match_stats['aces'] * 5 - \
                                           match_stats['quadro_kills'] * 4 - \
                                           match_stats['triple_kills'] * 3 -\
                                           match_stats['double_kills'] * 2

            match_stats['rating_1'] = calculate_rating_1_per_match(match_stats)
    return match_stats


def parse_matches_data(data: Dict, player_id: str, number: int) -> Dict[str, Any]:
    """Собирает общую информацию за один матч"""

    print(f'Обрабатывается матч № {number + 1}... id {data["rounds"][0]["match_id"]}')
    parsed_data = {
        'match_id': data['rounds'][0]['match_id'],
        'map': data['rounds'][0]['round_stats']['Map'],
        # add unix time date match
        'started_at': send_request(f'/matches/{data["rounds"][0]["match_id"]}')['started_at']
    }

    player_stats_in_match = get_player_stats_in_match(data, player_id)
    if player_stats_in_match:
        for key, value in player_stats_in_match.items():
            parsed_data[key] = value
        return parsed_data


def calculate_avg_rating_1(matches_stats: List[Dict]):
    """Рассчитывается средний рейтинг 1.0 игрока за все матчи"""
    return round(sum([match['rating_1'] for match in matches_stats]) / len(matches_stats), 2)


def is_wingman_mode(match) -> bool:
    """Проверяет являлся ли матч 'напарниками'"""
    return True if match['game_mode'] == 'Wingman' else False


def collect_all_matches_stats(matches_ids: List[str], player_faceit_id: str,) -> List[Dict]:
    """Собирает статистику по каждому матчу и рассчитывает для него рейтинг 1.0 (с учетом всей статистии игрока.
    Возвращает [{}, {}, {}...]
    """
    matches_stats = []
    # формирование необходимых данных из всех матчей
    for number, match_id in enumerate(matches_ids):
        match_data = parse_matches_data(send_request(f'/matches/{match_id}/stats'),
                                        player_faceit_id,
                                        number)
        # проверка на наличие данных полученных из матча
        if match_data:
            matches_stats.append(match_data)
    return matches_stats


def collect_player_info(urls: List[Tuple], player_id: str) -> Dict:
    parsed_player_data = {}

    for url in urls:

        # статистика за все время
        if url[1] == 'csgo_stats':
            print('Обрабатывается общая статистика')
            parsed_player_data['stats'] = parse_required_stats(send_request(url[0]))

        # история матчей
        elif url[1] == 'match_history':
            # получение id всех матчей
            matches_ids = []

            if parsed_player_data['stats']['matches_count'] >= 1100:
                range_idx = 10
            else:
                range_idx = parsed_player_data['stats']['matches_count'] // 100 + 1

            for i in range(range_idx):
                matches_ids.extend(match['match_id'] for match in send_request(url[0] + f'&offset={i * 100}')['items']
                                   if not is_wingman_mode(match))
            # получение статистики по каждому матчу
            parsed_player_data['matches'] = collect_all_matches_stats(matches_ids, player_id)

        # информация об faceit аккаунте
        else:
            print('Обрабатывается информация об аккаунте')
            parsed_player_data['player'] = parse_required_player_info(send_request(url[0]))

    parsed_player_data['stats']['rating_1'] = calculate_avg_rating_1(parsed_player_data['matches'])
    return parsed_player_data
