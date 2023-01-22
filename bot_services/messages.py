from typing import List

from database import tables


def get_message_for_player_info(faceit_nickname: str, player: tables.Player) -> str:
    """Возвращает сообщение с общей статистикой"""
    message = f'{faceit_nickname} статистика:' \
               f'\nМатчей - {player.stats.matches_count}' \
               f'\nLVL - {player.faceit_lvl}' \
               f'\nELO - {player.faceit_elo}' \
               f'\nПобед - {player.stats.wins_count}' \
               f'\nWinrate - {player.stats.winrate}%' \
               f'\nСыграно раундов - {player.stats.rounds_count}' \
               f'\nВсего убийств - {player.stats.kills_count}' \
               f'\nУбийств в голову - {player.stats.hs_count}' \
               f'\nПроцент убийств в голову - {player.stats.avg_hs_percent}%' \
               f'\nКоличество эйсов - {player.stats.aces}' \
               f'\nQuadro kills - {player.stats.quadro_kills}' \
               f'\nTriple kills - {player.stats.triple_kills}' \
               f'\nDouble kills - {player.stats.double_kills}' \
               f'\nОдиночных убийств - {player.stats.single_kills}' \
               f'\nКоличество смертей - {player.stats.deaths_count}' \
               f'\nПолучено MVP в раундах - {player.stats.mvps}' \
               f'\n\nСредние показатели:' \
               f'\nK/D - {player.stats.avg_kd}' \
               f'\nСреднее количество убийств - {player.stats.avg_kills}' \
               f'\nУбийств за раунд - {round(player.stats.avg_kpr, 2)}' \
               f'\nСмертей за раунд - {round(1 - player.stats.avg_spr, 2)}'
    return message


def get_text_for_player_matches_handler(faceit_nickname, matches: List[tables.Match]) -> str:
    """Возвращает сообщение со статистикой в 20 матчах"""
    message = f'Матчи {faceit_nickname}:'
    for count, match in enumerate(matches):
        sub_text = f'\n{count + 1}. {match.map} | Rating 1.0: {match.rating_1} | K/D: {match.kd} | Убийств: {match.kills} | Смертей: {match.deaths} | ' \
                   f'Эйсов: {match.aces} | Quadro kills: {match.quadro_kills} | Triple kills: {match.triple_kills} | ' \
                   f'Double kills: {match.double_kills} | HS: {match.hs_percent}% | MVP: {match.mvps}'
        message += sub_text
        if count != 19:
            message += '\n'
    return message


def get_message_for_best_hs_players(players: List[tables.PlayerStats]) -> str:
    """Возвращает 10 лучших игроков по avg_hs"""
    message = f'<b>Игроки с лучшим hs:</b>'
    for count, player in enumerate(players):
        sub_text = f'\n{count + 1}. {player.player.faceit_nickname} - <b>{player.avg_hs_percent}%</b>'
        message += sub_text
    return message

