import json
from typing import Dict

from full_statistic import read_players_nickname_from_file, get_faciet_id
from urls import send_request


def read_player_info_from_file(nickname_faceit: str) -> Dict:
    """Получение общей статистики игрока из json файла"""
    try:
        with open(f'players_info/{nickname_faceit}.json', 'r') as file:
            stats = json.loads(file.read())
            return stats
    except Exception as e:
        print(f'Не получилось прочитать данные из файла players_info/{nickname_faceit}.json')
        print(f'Ошибка: {e}')


def get_matches_count_from_faceit(nickname_faceit: str) -> int:
    """Получение количества матчей с faceit для определенного игрока"""
    faceit_id = get_faciet_id(nickname_faceit)
    data = send_request(f'/players/{faceit_id}/stats/csgo')
    return int(data['lifetime']['Matches'])


def get_matches_count_from_json(nickname_faceit) -> int:
    """Получение количества матчей с faceit для определенного игрока"""
    stats = read_player_info_from_file(nickname_faceit)
    return int(stats['stats']['matches_count'])


def check_matches_count(nickname_faceit: str) -> bool:
    """Проверяет изменилось ли количество матчей"""
    return get_matches_count_from_faceit(nickname_faceit) > get_matches_count_from_json(nickname_faceit)


# TODO
def get_new_matches():
    pass


def main():
    for nickname_faceit in read_players_nickname_from_file():
        if check_matches_count(nickname_faceit):
            pass

