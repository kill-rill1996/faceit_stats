from database.services import add_to_database
from full_statistic import read_players_nickname_from_file
from database.database import create_db
from update_stats import read_player_info_from_file


def main():
    # get_avg_stats()
    create_db()
    players_info = []
    for nickname in read_players_nickname_from_file():
        print(f'Обрабатывается игрок {nickname}')

        player_info = read_player_info_from_file(nickname)

        if player_info:
            players_info.append(player_info)
    for player in players_info:
        add_to_database(player)


if __name__ == '__main__':
    main()