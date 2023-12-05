import json
from typing import Dict, List, Any, Union
from datetime import datetime, timedelta

from parse_data import is_wingman_mode, parse_required_stats, collect_all_matches_stats, parse_required_player_info
from urls import send_request, create_urls
from config import PLAYERS_FULL_STATISTIC_DIR, PLAYERS_NEW_STATS_DIR, CHECK_UPDATE_PERIOD
from database.database import Session
from database.services import add_to_db_matches, add_to_db_player_info, add_to_db_player_stats, update_rating, \
    get_all_players_from_db, get_player_mathces_id_from_db
from database import tables
from config import LOG_DIRECTORY


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
    data = send_request(f'/players/{player_faceit_id}/stats/cs2')
    return int(data['lifetime']['Matches'])


def get_matches_count_from_json(nickname_faceit) -> Union[int, bool]:
    """Получение количества матчей с faceit для определенного игрока"""
    stats = read_player_info_from_file(nickname_faceit)
    if stats:
        return int(stats['stats']['matches_count'])
    return False


def get_matches_count_from_db(faceit_id) -> int:
    with Session() as session:
        player = session.query(tables.Player).filter_by(faceit_id=faceit_id).first()
        matches_count = session.query(tables.PlayerStats).filter_by(player_id=player.id).first().matches_count
        return matches_count


def check_matches_count(player_faceit_id: str) -> bool:
    """Проверяет изменилось ли количество матчей"""
    matches_count_from_db = get_matches_count_from_db(player_faceit_id)
    matches_count_from_faceit = get_matches_count_from_faceit(player_faceit_id)
    return matches_count_from_faceit > matches_count_from_db


def get_unix_time_lower_bound_of_query(period: int = CHECK_UPDATE_PERIOD) -> int:
    """Возвращает дату с котрой нужно начать проверку в формате timestamp в
    зависимости от выбранного периода проверки"""
    now = datetime.now()
    lower_bound_of_query = now - timedelta(days=period)
    lower_bound_of_query_timestamp = int(round(lower_bound_of_query.timestamp()))
    return lower_bound_of_query_timestamp


def get_new_matches_ids(faceit_id: str) -> List[str]:
    """Получает list[id] новых матчей за указанный период"""
    # start_date = get_unix_time_lower_bound_of_query()
    url = f'/players/{faceit_id}/history?game=cs2'
    matches_ids_from_db = get_player_mathces_id_from_db(faceit_id)
    matches_ids_from_faceit = [match['match_id'] for match in send_request(url)['items'] if not is_wingman_mode(match)]
    return list(set(matches_ids_from_faceit) - set(matches_ids_from_db))


def get_new_stats(player_faceit_id: str) -> Dict[str, Any]:
    print('Собирается новая информация')
    parsed_player_data = {}
    urls = create_urls(player_faceit_id)

    # сбор новой общей статистики
    parsed_player_data['stats'] = parse_required_stats(send_request(urls[1][0]))
    # сбор статистики новых матчей
    parsed_player_data['matches'] = collect_all_matches_stats(get_new_matches_ids(player_faceit_id),
                                                              player_faceit_id,
                                                              )
    parsed_player_data['player'] = parse_required_player_info(send_request(urls[0][0]))
    return parsed_player_data


if __name__ == '__main__':
    for player in get_all_players_from_db():
        print(f'Проверяется игрок {player.faceit_nickname} - {player.faceit_id}')
        if check_matches_count(player.faceit_id):
            try:
                new_stats = get_new_stats(player.faceit_id)
                with Session() as session:
                    add_to_db_player_info(session, new_stats['player'], player.faceit_id, update=True)
                    add_to_db_player_stats(session, new_stats['stats'], player.faceit_id, update=True)
                    add_to_db_matches(session, new_stats['matches'], player.faceit_id)
                    update_rating(player.faceit_id)
            except Exception as e:
                with open(f'{LOG_DIRECTORY}log.txt', 'a') as f:
                    f.write(f'Error:\n{e}')
            # write_player_info_in_file(new_stats, directory=PLAYERS_NEW_STATS_DIR)
        else:
            print('Нет новых матчей')
    with open(f'{LOG_DIRECTORY}log.txt', 'a') as f:
        f.write(f'Последне обновление {datetime.now()}\n')

