import json
from typing import List, Dict

from urls import send_request, create_urls
from parse_data import collect_player_info, parse_required_stats, parse_required_player_info
from config import PLAYERS_LIST, PLAYERS_FULL_STATISTIC_DIR
from custom_exceptions import PlayerInfoException


def get_faciet_id(nickname: str) -> str:
    """return faceit id by player nickname"""
    try:
        player_info = send_request(f'/players?nickname={nickname}')
        if 'errors' in player_info.keys():
            raise PlayerInfoException(nickname, player_info['errors'])
        return player_info['player_id']
    except PlayerInfoException as e:
        print(e.message)


def write_player_info_in_file(data: Dict, directory: str) -> bool:
    """Записывает полную статистику игрока в json файл в формате nickname.json"""
    try:
        with open(f'{directory}/{data["player"]["faceit_nickname"]}.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f'Произошла ошибка при записи игрока {data["player"]["faceit_nickname"]} в файл')
        print(e)
        return False


def read_players_nickname_from_file(file_name: str = PLAYERS_LIST) -> List[str]:
    """Получает перечень игроков из указанного файла"""
    try:
        with open(f'{file_name}', 'r') as f:
            data = f.read().strip().split('\n')
    except Exception as e:
        print(f'Ошибка при чтении данных из файлов ({e})')
        data = []
    return data


def get_avg_stats():
    data = {'avg_kpr': [],
            'avg_spr': [],
            'avg_rmk': []}
    for count, player_faceit_id in enumerate(read_players_nickname_from_file(file_name='players_for_avg3.txt')):
        print(f'Обрабатывается игрок {count}')
        try:
            data['avg_kpr'].append(parse_required_stats(send_request(f'/players/{player_faceit_id}/stats/cs2'))['avg_kpr'])
            data['avg_spr'].append(parse_required_stats(send_request(f'/players/{player_faceit_id}/stats/cs2'))['avg_spr'])
            data['avg_rmk'].append(parse_required_stats(send_request(f'/players/{player_faceit_id}/stats/cs2'))['avg_rmk'])
        except:
            continue
    data['avg_kpr'] = sum(data['avg_kpr']) / len(data['avg_kpr'])
    data['avg_spr'] = sum(data['avg_spr']) / len(data['avg_spr'])
    data['avg_rmk'] = sum(data['avg_rmk']) / len(data['avg_rmk'])
    with open('avg_stats.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_full_stats_for_player(nickname: str) -> Dict:
    faciet_id = get_faciet_id(nickname)
    if faciet_id:
        player_info = collect_player_info(create_urls(faciet_id), player_id=faciet_id)
        return player_info


if __name__ == '__main__':
    players_info = []
    for nickname in read_players_nickname_from_file():
        try:
            print(f'Обрабатывается игрок {nickname}')
            player_info = get_full_stats_for_player(nickname)

            if player_info:
                players_info.append(player_info)
        except:
            pass
    for player in players_info:
        write_player_info_in_file(player, directory='players_info')
