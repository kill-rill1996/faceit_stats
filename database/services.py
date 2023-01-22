from typing import Dict, List
from sqlalchemy.orm import Session as Sa_session, joinedload

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


def get_player_info_from_db(nickname: str) -> tables.Player:
    try:
        with Session() as session:
            player_info = session.query(tables.Player).filter_by(faceit_nickname=nickname)\
                .options(joinedload(tables.Player.stats)).first()
        return player_info
    except Exception as e:
        print(e)


def get_player_matches_from_db(nickname: str, count: int = 20) -> List[tables.Match]:
    try:
        with Session() as session:
            player_with_matches = session.query(tables.Player).filter_by(faceit_nickname=nickname)\
                .options(joinedload(tables.Player.matches)).first()
            return player_with_matches.matches[:count]
    except Exception as e:
        print(e)


def get_players_stats_from_db(order_by: str = None, limit_count: int = None) -> List[tables.PlayerStats]:
    """Get players full stats from db"""
    with Session() as session:
        if order_by == 'hs':
            players_stats = session.query(tables.PlayerStats).order_by(tables.PlayerStats.avg_hs_percent.desc()).limit(limit_count)
        else:
            players_stats = session.query(tables.PlayerStats).all()
        return players_stats

