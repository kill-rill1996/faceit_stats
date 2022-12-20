import json
from typing import Dict, List, Any
from datetime import datetime, timedelta

from full_statistic import read_players_nickname_from_file, get_faciet_id, write_player_info_in_file
from parse_data import is_wingman_mode, parse_required_stats, collect_all_matches_stats, parse_required_player_info
from urls import send_request, create_urls
from config import PLAYERS_FULL_STATISTIC_DIR, PLAYERS_NEW_STATS_DIR, CHECK_UPDATE_PERIOD


def read_player_info_from_file(nickname_faceit: str, directory: str = PLAYERS_FULL_STATISTIC_DIR) -> Dict:
    """Получение общей статистики игрока из json файла"""
    stats = []
    try:
        with open(f'{directory}/{nickname_faceit}.json', 'r') as file:
            stats = json.loads(file.read())
    except Exception as e:
        print(f'Не получилось прочитать данные из файла players_info/{nickname_faceit}.json')
        print(f'Ошибка: {e}')
    return stats


def get_matches_count_from_faceit(player_faceit_id: str) -> int:
    """Получение количества матчей с faceit для определенного игрока"""
    data = send_request(f'/players/{player_faceit_id}/stats/csgo')
    return int(data['lifetime']['Matches'])


def get_matches_count_from_json(nickname_faceit) -> int | bool:
    """Получение количества матчей с faceit для определенного игрока"""
    stats = read_player_info_from_file(nickname_faceit)
    if stats:
        return int(stats['stats']['matches_count'])
    return False


def check_matches_count(player_faceit_id: str, nickname_faceit: str) -> bool:
    """Проверяет изменилось ли количество матчей"""
    matches_count_from_json = get_matches_count_from_json(nickname_faceit)
    matches_count_from_faceit = get_matches_count_from_faceit(player_faceit_id)
    if not matches_count_from_json:
        return False
    return matches_count_from_faceit > matches_count_from_json


def get_unix_time_lower_bound_of_query(period: int = CHECK_UPDATE_PERIOD) -> int:
    """Возвращает дату с котрой нужно начать проверку в формате timestamp в
    зависимости от выбранного периода проверки"""
    now = datetime.now()
    lower_bound_of_query = now - timedelta(days=period)
    lower_bound_of_query_timestamp = int(round(lower_bound_of_query.timestamp()))
    return lower_bound_of_query_timestamp


def get_new_matches_ids(player_faceit_id: str) -> List[str]:
    """Получает list[id] новых матчей за указанный период"""
    start_date = get_unix_time_lower_bound_of_query()
    url = f'/players/{player_faceit_id}/history?game=csgo&from={start_date}'
    return [match['match_id'] for match in send_request(url)['items'] if not is_wingman_mode(match)]


def get_new_stats(player_faceit_id: str) -> Dict[str, Any]:
    print('Собирается новая информация')
    parsed_player_data = {}
    urls = create_urls(player_faceit_id)

    # сбор новой общей статистики
    parsed_player_data['stats'] = parse_required_stats(send_request(urls[1][0]))
    # сбор статистики новых матчей
    parsed_player_data['matches'] = collect_all_matches_stats(get_new_matches_ids(player_faceit_id),
                                                              player_faceit_id,
                                                              parsed_player_data['stats'])
    parsed_player_data['player'] = parse_required_player_info(send_request(urls[0][0]))
    return parsed_player_data


def main():
    for nickname_faceit in read_players_nickname_from_file():
        print(f'Проверяется игрок {nickname_faceit}')
        player_faceit_id = get_faciet_id(nickname_faceit)
        if check_matches_count(player_faceit_id, nickname_faceit):
            new_stats = get_new_stats(player_faceit_id)
            write_player_info_in_file(new_stats, directory=PLAYERS_NEW_STATS_DIR)
        else:
            print('Нет новых матчей')


if __name__ == '__main__':
    main()
