from typing import Dict, List
from sqlalchemy.orm import Session as Sa_session

from . import tables
from .database import Session


def add_to_db_player_info(session: Sa_session, data: Dict) -> None:
    player = tables.Player(**data)
    session.add(player)
    session.commit()


def add_to_db_player_stats(session: Sa_session, data: Dict, faceit_id: str) -> None:
    player = session.query(tables.Player).filter_by(faceit_id=faceit_id).first()
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
        add_to_db_player_info(session, data['player'])
        add_to_db_player_stats(session, data['stats'], data['player']['faceit_id'])
        add_to_db_matches(session, data['matches'], data['player']['faceit_id'])
    print('Данные записаны.')

