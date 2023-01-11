from typing import Dict, List
from sqlalchemy.orm import Session as Sa_session

from . import tables
from .database import Session


def add_to_db_player_info(session: Sa_session, data: Dict, faceit_id: str, update=False) -> None:
    # обновление имеющейся записи в базе данных
    if update:
        player = session.query(tables.Player).filter_by(faceit_id=faceit_id).first()
        for k, v in data.items():
            setattr(player, k, v)
    # создание новой записи в базе данных
    else:
        player = tables.Player(**data)
        session.add(player)
    session.commit()


def add_to_db_player_stats(session: Sa_session, data: Dict, faceit_id: str, update=False) -> None:
    player = session.query(tables.Player).filter_by(faceit_id=faceit_id).first()
    if update:
        player_stats = session.query(tables.PlayerStats).filter_by(player_id=player.id).first()
        for k, v in data.items():
            setattr(player_stats, k, v)
    else:
        stats = tables.PlayerStats(**data)
        stats.player_id = player.id
        session.add(stats)

    session.commit()


def add_to_db_matches(session: Sa_session,  data: List[Dict], faceit_id: str) -> None:
    player = session.query(tables.Player).filter_by(faceit_id=faceit_id).first()
    for match in data:
        match = tables.Match(**match)
        match.player_id = player.id
        session.add(match)
    session.commit()


def add_to_database(data: Dict) -> None:
    with Session() as session:
        print('Запись в базу данных...')
        # запись в базу данных информации об аккаунте
        add_to_db_player_info(session, data['player'], data['player']['faceit_id'])
        # запись в базу данных статистики общей
        add_to_db_player_stats(session, data['stats'], data['player']['faceit_id'])
        # запись в базу данных матчей игрока
        add_to_db_matches(session, data['matches'], data['player']['faceit_id'])
    print('Данные записаны.')


def get_all_faceit_ids_from_db() -> List[str]:
    with Session() as session:
        faceit_ids = [player.faceit_id for player in session.query(tables.Player).all()]
    return faceit_ids


def get_all_players_nickname_from_db() -> List[str]:
    with Session() as session:
        faceit_nicknames = [player.faceit_nickname for player in session.query(tables.Player).all()]
    return faceit_nicknames



