from typing import List, Dict

from full_statistic import read_players_nickname_from_file, get_faciet_id, write_player_info_in_file, \
    get_last_matches_stats
from urls import create_urls
from parse_data import collect_player_info
from config import PLAYERS_FULL_STATISTIC_DIR
from database.database import create_db, Session
from database.service import add_to_database
from database import tables


def get_full_statistic() -> List[Dict]:
    players_info = []
    for nickname in read_players_nickname_from_file():
        print(f'Обрабатывается игрок {nickname}')
        faciet_id = get_faciet_id(nickname)
        if faciet_id:
            player_info = collect_player_info(create_urls(faciet_id), player_id=faciet_id)
            players_info.append(player_info)
    return players_info


if __name__ == '__main__':
    create_db()
    full_statistic = get_full_statistic()
    for player in full_statistic:
        add_to_database(player)
