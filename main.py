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
            # write_player_info_in_file(player_info, directory=PLAYERS_FULL_STATISTIC_DIR)
            # get_last_matches_stats(faciet_id, 135)
    return players_info


def add_to_db():

    with Session() as session:
        player1 = tables.Player(
            faceit_id='067ad9f2-e96d-444a-9dd9-3de2813b0e26',
            faceit_nickname='nk_st1ck',
            steam_nickname='NK|st1ck',
            avatar="https://assets.faceit-cdn.net/avatars/067ad9f2-e96d-444a-9dd9-3de2813b0e26_1607622252515.jpg",
            country="ru"
        )

        session.add(player1)
        session.commit()

        player = session.query(tables.Player).filter_by(id=1).first()
        stats1 = tables.PlayerStats(matches_count=457, wins_count=230, winrate=50, rounds_count=12456, avg_kd=1.43,
            avg_kills=26, hs_percent=72, kills_count=8319, death_count=6784, single_kills=4420, double_kills=1243,
            triple_kills=385, quadro_kills=153, aces=3, mvps=830, avg_kpr=0.6673886883273165,
            avg_spr=0.35026073004412356, avg_rmk=1.1150421179302046, player_id=player.id)
        session.add(stats1)
        session.commit()

        match1 = tables.Match(
            match_id="1-635dd872-2e65-4acc-b054-73b3821e0823",
            map="de_dust2",
            rounds=34,
            kills=21,
            deaths=25,
            kd=0.84,
            kr=0.84,
            sr=0.2647058823529412,
            single_kills=11,
            double_kills=3,
            triple_kills=0,
            quadro_kills=1,
            aces=0,
            rating_1=0.92,
            mvps=3,
            hs_count=9,
            hs_percent=49,
            player_id=player.id
        )
        match2 = tables.Match(match_id="1-635dd872-2e65-4acc-b054-73b3821e0379", map="de_inferno", rounds=30, kills=22,
                            deaths=19, kd=1.17, kr=0.94, sr=0.3947058823529412, single_kills=12, double_kills=3, triple_kills=0,
                            quadro_kills=1, aces=0, rating_1=1.05, mvps=5, hs_count=10, hs_percent=60, player_id=player.id)
        match3 = tables.Match(match_id="1-635dd872-2e65-4acc-b054-73b3821e0356", map="de_mirage", rounds=28, kills=20,
                              deaths=15, kd=1.20, kr=0.94, sr=0.3447058823529412, single_kills=12, double_kills=3,
                              triple_kills=0, quadro_kills=1, aces=0, rating_1=1.05, mvps=5, hs_count=10, hs_percent=60,
                              player_id=player.id)
        session.add(match1)
        session.add(match2)
        session.add(match3)
        session.commit()


if __name__ == '__main__':
    create_db()
    full_statistic = get_full_statistic()
    for player in full_statistic:
        add_to_database(player)
