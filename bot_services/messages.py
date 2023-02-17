import datetime
from typing import List, Dict, Union

from database import tables


def get_greeting_message():
    message = "Это Telegram-бот для получения статистики с faceit.com.\n" \
              "Здесь можно получить подробную статистику об игроке по его никнейму faceit, а также cравнить показатели с другими игроками"
    return message


def get_message_for_player_main_info(player: tables.Player) -> str:
    """Возвращает сообщение с основной информацией об игроке"""
    message = f'<b>{player.faceit_nickname}</b>' \
                   f'\nLVL - {player.faceit_lvl}' \
                   f'\nELO - {player.faceit_elo}' \
                   f'\nМатчей - {player.stats.matches_count}' \
                   f'\nWinrate - {player.stats.winrate}%'
    if player.country == 'ru':
        message += f'\nСтрана - 🇷🇺'
    return message


def get_message_for_player_info(faceit_nickname: str, player: tables.Player) -> str:
    """Возвращает сообщение с общей статистикой"""
    message = f'<b>Статистика {faceit_nickname}:</b>' \
               f'\nМатчи - <b>{player.stats.matches_count}</b>' \
               f'\nLVL - <b>{player.faceit_lvl}</b>' \
               f'\nELO - <b>{player.faceit_elo}</b>' \
               f'\nПобед - <b>{player.stats.wins_count}</b>' \
               f'\nWinrate - <b>{player.stats.winrate}%</b>' \
               f'\nСыграно раундов - <b>{player.stats.rounds_count}</b>' \
               f'\nВсего убийств - <b>{player.stats.kills_count}</b>' \
               f'\nУбийств в голову - <b>{player.stats.hs_count}</b>' \
               f'{get_emoji_string_new(player.stats.avg_hs_percent, 45, 50, "Процент убийств в голову - <b>{0}%</b> ")}' \
               f'\nКоличество эйсов - <b>{player.stats.aces}</b>' \
               f'\nQuadro kills - <b>{player.stats.quadro_kills}</b>' \
               f'\nTriple kills - <b>{player.stats.triple_kills}</b>' \
               f'\nDouble kills - <b>{player.stats.double_kills}</b>' \
               f'\nОдиночных убийств - <b>{player.stats.single_kills}</b>' \
               f'\nКоличество смертей - <b>{player.stats.deaths_count}</b>' \
               f'\nКоличество MVP - <b>{player.stats.mvps}</b> ⭐️' \
               f'\n\n<b>Средние показатели:</b>' \
               f'{get_emoji_string_new(player.stats.rating_1, 1.05, 1.10, "Рейтинг 1.0 - <b>{0}</b>")}'\
               f'{get_emoji_string_new(player.stats.avg_kd, 1.0, 1.20, "K/D - <b>{0}</b> ")}' \
               f'{get_emoji_string_new(player.stats.avg_kills, 16, 21, "Среднее количество убийств - <b>{0}</b> ")}' \
               f'\nУбийств за раунд - <b>{round(player.stats.avg_kpr, 2)}</b>' \
               f'\nСмертей за раунд - <b>{round(1 - player.stats.avg_spr, 2)}</b>'
    return message


def get_text_for_player_matches_handler(faceit_nickname: str, matches: List[tables.Match]) -> str:
    """Возвращает сообщение со статистикой в 20 матчах"""
    message = f'<b>Матчи {faceit_nickname}:</b>'
    for count, match in enumerate(matches):
        sub_text = f'\n<b>{datetime.datetime.fromtimestamp(match.started_at).strftime("%H:%M %d.%m.%Y")}</b>' \
                    f'\n<b>{count + 1}.</b> <b>{match.map}</b> {match.score} {match.result} | Rating 1.0: {match.rating_1} | K/D: {match.kd} | Убийств: {match.kills} | Смертей: {match.deaths} | ' \
                   f'Эйсов: {match.aces} | Quadro kills: {match.quadro_kills} | Triple kills: {match.triple_kills} | ' \
                   f'Double kills: {match.double_kills} | HS: {match.hs_percent}% | MVP: {match.mvps}'
        message += sub_text.replace('True', '✅').replace('False', '❌') + '\n'
    return message


def get_message_for_best_elo_players(players: List[tables.Player]) -> str:
    """Возвращает 10 лучших игроков по кол-ву faciet elo"""
    message = f'<b>Игроки с наибольшим elo:</b>'
    for count, player in enumerate(players):
        sub_text = f'\n{count + 1}. {player.faceit_nickname} - <b>{player.faceit_elo}</b>'
        message += sub_text
    return message


def create_message_for_best_players_in_category(title: str, high: Union[int, float], low: Union[int, float],
                                                players: List[tables.PlayerStats], category: str) -> str:
    """Возвращает сообщение с 10 лучшими игроками в указанной категории"""
    message = title
    for count, player in enumerate(players):
        faceit_nickname = player.player.faceit_nickname
        stat = player.__dict__[category]
        sub_text = f'\n{count + 1}. {faceit_nickname} - <b>{stat}</b>'
        if stat > high:
            emoji = ' 🔥'
        elif low <= stat <= high:
            emoji = ' ✅'
        else:
            emoji = ' ❌'
        message += (sub_text + emoji)
    return message


def get_msg_for_stats_last_n_matches(data: Dict, matches_count: int, faceit_nickname: str) -> str:
    """Возвращает сообщение со статистикой за последние n матчей"""
    message = f'<b>Статистика {faceit_nickname} за последние {matches_count} матчей:</b>'
    message += f'{get_emoji_string_new(data["kd"], 1.0, 1.20, "K/D - <b>{0}</b> ")}' \
               f'{get_emoji_string_new(data["avg_rating_1"], 1.0, 1.15, "Рейтинг 1.0 - <b>{0}</b> ")}' \
               f'{get_emoji_string_new(data["avg_kills"], 16, 21, "Среднее количество убийств - <b>{0}</b> ")}' \
               f'\nСреднее количество смертей - <b>{data["avg_deaths"]}</b>' \
               f'\nКоличество эйсов - <b>{data["aces"]}</b>' \
               f'\nQuadro kills - <b>{data["quadro_kills"]}</b>' \
               f'\nTriple kills - <b>{data["triple_kills"]}</b>' \
               f'\nDouble kills - <b>{data["double_kills"]}</b>' \
               f'\nКоличество убийств - <b>{data["kills"]}</b>' \
               f'\nКоличество убийств в голову - <b>{data["hs_count"]}</b>' \
               f'{get_emoji_string_new(data["hs_percent"], 45, 50, "Процент убийств в голову - <b>{0}%</b> ")}' \
               f'\nКоличество MVP - <b>{data["mvps"]}</b> ⭐️'
    return message


def get_message_for_compare(stat1: tables.Player, stat2: tables.Player) -> str:
    """Возвращает сообщение со сравнением игроков"""
    message = f'Сравнение <b>{stat1.faceit_nickname}</b> и <b>{stat2.faceit_nickname}</b>\n'
    rows = [(stat1.stats.matches_count, stat2.stats.matches_count, '\n<b>Матчи:</b> {2} {0} - {1} {3}',),
                       (stat1.faceit_elo, stat2.faceit_elo, '\n<b>ELO:</b> {2} {0} - {1} {3}',),
                       (stat1.faceit_lvl, stat2.faceit_lvl,  '\n<b>LVL:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.wins_count, stat2.stats.wins_count, '\n<b>Побед:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.winrate, stat2.stats.winrate, '\n<b>Winrate:</b> {2} {0}% - {1}% {3}',),
                       (stat1.stats.rating_1, stat2.stats.rating_1, '\n<b>Рейтинг 1.0: :</b> {2} {0} - {1} {3}',),
                       (stat1.stats.avg_kd, stat2.stats.avg_kd, '\n<b>Средний K/D:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.kills_count, stat2.stats.kills_count,  '\n<b>Всего убийств:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.avg_hs_percent, stat2.stats.avg_hs_percent, '\n<b>Процент HS:</b> {2} {0}% - {1}% {3}',),
                       (stat1.stats.aces, stat2.stats.aces, '\n<b>Количество эйсов:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.quadro_kills, stat2.stats.quadro_kills, '\n<b>Quadro kills:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.triple_kills, stat2.stats.triple_kills, '\n<b>Triple kills:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.double_kills, stat2.stats.double_kills, '\n<b>Double kills:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.deaths_count, stat2.stats.deaths_count, '\n<b>Смертей:</b> {2} {0} - {1} {3}', 'reverse'),
                       (stat1.stats.mvps, stat2.stats.mvps, '\n<b>Количество MVP:</b> {2} {0} - {1} {3}',),
                       (stat1.stats.avg_kills, stat2.stats.avg_kills,  '\n<b>Среднее кол-во убийств:</b> {2} {0} - {1} {3}')]

    for row in rows:
        stat1 = row[0]
        stat2 = row[1]
        if len(row) > 3:
            if stat1 < stat2:
                message += row[2].format(stat1, stat2, '✅', '❌')
            elif stat1 > stat2:
                message += row[2].format(stat1, stat2, '❌', '✅')
            else:
                message += row[2].format(stat1, stat2, '', '')
        else:
            if stat1 > stat2:
                message += row[2].format(stat1, stat2, '✅', '❌')
            elif stat1 < stat2:
                message += row[2].format(stat1, stat2, '❌', '✅')
            else:
                message += row[2].format(stat1, stat2, '', '')
    return message


def get_emoji_string_new(parameter: Union[int, float], low: Union[int, float], high: Union[int, float], row: str) -> str:
    """Возвращает готовую строку для статистки за n матчей"""
    result = '\n' + row.format(parameter)
    if parameter >= high:
        return result + '🔥'
    elif low <= parameter < high:
        return result + '✅'
    return result + '❌'
