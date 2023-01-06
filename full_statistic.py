import json
from typing import List, Dict

from urls import send_request, create_urls
from parse_data import collect_player_info, is_wingman_mode, collect_all_matches_stats, parse_required_stats, \
    parse_required_player_info
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
            data = f.read().split('\n')
    except Exception as e:
        print(f'Ошибка при чтении данных из файлов ({e})')
        data = []
    return data


def get_last_matches_stats(faceit_id, request_matches_count: int = 20):
    """Получает статистику за последние n матчей"""
    matches_ids = []

    if request_matches_count > 100:
        for i in range(request_matches_count // 100 + 1):
            url = f'/players/{faceit_id}/history?game=csgo&limit=100'
            matches = [match['match_id'] for match in send_request(url + f'&offset={i * 100}')['items']
                       if not is_wingman_mode(match)]

            if i == request_matches_count // 100:
                matches = matches[:request_matches_count % 100]

            matches_ids.extend(matches)
    else:
        url = f'/players/{faceit_id}/history?game=csgo&limit={request_matches_count}'
        matches_ids.extend(match['match_id'] for match in send_request(url)['items'] if not is_wingman_mode(match))

    print(f'Собирается информация за последние {request_matches_count} матчей')
    parsed_player_data = {}
    urls = create_urls(faceit_id)

    # сбор общей статистики
    parsed_player_data['stats'] = parse_required_stats(send_request(urls[1][0]))
    # сбор статистики матчей
    parsed_player_data['matches'] = collect_all_matches_stats(matches_ids,
                                                              faceit_id,
                                                              parsed_player_data['stats'])
    parsed_player_data['player'] = parse_required_player_info(send_request(urls[0][0]))

    write_player_info_in_file(parsed_player_data, 'players_last_matches')


def get_avg_stats():
    data = {'avg_kpr': [],
            'avg_spr': [],
            'avg_rmk': []}
    for player_nickname in read_players_nickname_from_file():
        data['avg_kpr'].append(parse_required_stats(send_request(f'/players/{get_faciet_id(player_nickname)}/stats/csgo'))['avg_kpr'])
        data['avg_spr'].append(parse_required_stats(send_request(f'/players/{get_faciet_id(player_nickname)}/stats/csgo'))['avg_spr'])
        data['avg_rmk'].append(parse_required_stats(send_request(f'/players/{get_faciet_id(player_nickname)}/stats/csgo'))['avg_rmk'])
    data['avg_kpr'] = sum(data['avg_kpr']) / len(data['avg_kpr'])
    data['avg_spr'] = sum(data['avg_spr']) / len(data['avg_spr'])
    data['avg_rmk'] = sum(data['avg_rmk']) / len(data['avg_rmk'])
    with open('avg_stats/avg_stats.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # get_avg_stats()
    for nickname in read_players_nickname_from_file():
        print(f'Обрабатывается игрок {nickname}')
        faciet_id = get_faciet_id(nickname)
        if faciet_id:
            player_info = collect_player_info(create_urls(faciet_id), player_id=faciet_id)
            write_player_info_in_file(player_info, directory=PLAYERS_FULL_STATISTIC_DIR)
