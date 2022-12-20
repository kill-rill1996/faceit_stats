import json
from typing import List, Dict

from urls import send_request, create_urls
from parse_data import collect_player_info
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
        with open(f'{directory}/{data["player"]["nickname_faceit"]}.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f'Произошла ошибка при записи игрока {data["player"]["nickname_faceit"]} в файл')
        print(e)
        return False


def read_players_nickname_from_file(file_name: str = PLAYERS_LIST) -> List[str]:
    """Получает перечень игроков из указанного файла"""
    try:
        with open(f'{file_name}', 'r') as f:
            data = f.read().split('\n')
    except Exception as e:
        print(f'Ошибка при чтении данных из файлов ({e})')
        data = []
    return data


def main():
    for nickname in read_players_nickname_from_file():
        print(f'Обрабатывается игрок {nickname}')
        faciet_id = get_faciet_id(nickname)
        if faciet_id:
            player_info = collect_player_info(create_urls(faciet_id), player_id=faciet_id)
            write_player_info_in_file(player_info, directory=PLAYERS_FULL_STATISTIC_DIR)


if __name__ == '__main__':
    main()