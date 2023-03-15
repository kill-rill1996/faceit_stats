from database.services import delete_player_from_db


def main():
    players = ["nk_st1ck2", "Get_elOy"]
    if players:
        for player in players:
            try:
                delete_player_from_db(player)
                print(f"Пользователь {player} удален")
            except Exception as e:
                print(e)
    else:
        print('Список пользователей для удаления пуст')


if __name__ == '__main__':
    main()