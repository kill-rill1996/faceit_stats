import requests
from typing import Dict, Any, List, Tuple

from config import DOMEN, HEADERS


def send_request(url: str, domen: str = DOMEN, headers: dict = HEADERS) -> Dict[str, Any]:
    """Отправляет запросы на сервер и возвращает информацию в json формате"""
    return requests.get(domen + url, headers=headers).json()


def create_urls(faciet_id: str, game: str = 'csgo') -> List[Tuple]:
    """return list of urls with an explanation in the format [(url, explain)]"""

    urls = [(f'/players/{faciet_id}', 'acc_info'),
            (f'/players/{faciet_id}/stats/{game}', 'csgo_stats'),
            (f'/players/{faciet_id}/history?game=csgo&limit=100', 'match_history'),
            ]
    return urls
