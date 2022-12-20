import json
from typing import List, Dict

from urls import send_request, create_urls
from parse_data import collect_player_info
from config import PLAYERS_LIST


def get_faciet_id(nickname: str) -> str:
    """return faceit id by player nickname"""
    player_info = send_request(f'/players?nickname={nickname}')
    return player_info['player_id']


def write_player_info_in_file(data: Dict) -> bool:
    """Записывает полную статистику игрока в json файл в формате nickname.json"""
    try:
        with open(f'players_info/{data["player"]["nickname_faceit"]}.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except:
        print(f'Произошла ошибка при записи игрока {data["player"]["nickname_faceit"]} в файл')
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
        # добавить функцию которая будет делать запрос на кол-во матчей игрока и дальше запускать алгоритм при неолбходимости
        player_info = collect_player_info(create_urls(faciet_id), player_id=faciet_id)
        write_player_info_in_file(player_info)


if __name__ == '__main__':
    main()