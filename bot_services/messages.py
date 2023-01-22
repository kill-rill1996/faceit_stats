from typing import List, Dict

from database import tables


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
               f'\nПроцент убийств в голову - <b>{player.stats.avg_hs_percent}%</b>' \
               f'\nКоличество эйсов - <b>{player.stats.aces}</b>' \
               f'\nQuadro kills - <b>{player.stats.quadro_kills}</b>' \
               f'\nTriple kills - <b>{player.stats.triple_kills}</b>' \
               f'\nDouble kills - <b>{player.stats.double_kills}</b>' \
               f'\nОдиночных убийств - <b>{player.stats.single_kills}</b>' \
               f'\nКоличество смертей - <b>{player.stats.deaths_count}</b>' \
               f'\nКоличество MVP - <b>{player.stats.mvps}</b> ⭐️' \
               f'\n\n<b>Средние показатели:</b>' \
               f'{get_emojies_string(kd=player.stats.avg_kd)}' \
               f'{get_emojies_string(avg_kills=player.stats.avg_kills)}' \
               f'\nУбийств за раунд - <b>{round(player.stats.avg_kpr, 2)}</b>' \
               f'\nСмертей за раунд - <b>{round(1 - player.stats.avg_spr, 2)}</b>'
    return message


def get_text_for_player_matches_handler(faceit_nickname: str, matches: List[tables.Match]) -> str:
    """Возвращает сообщение со статистикой в 10 матчах"""
    message = f'<b>Матчи {faceit_nickname}:</b>'
    for count, match in enumerate(matches):
        sub_text = f'\n<b>{count + 1}.</b> {match.map} | Rating 1.0: {match.rating_1} | K/D: {match.kd} | Убийств: {match.kills} | Смертей: {match.deaths} | ' \
                   f'Эйсов: {match.aces} | Quadro kills: {match.quadro_kills} | Triple kills: {match.triple_kills} | ' \
                   f'Double kills: {match.double_kills} | HS: {match.hs_percent}% | MVP: {match.mvps}'
        message += sub_text
        if count != 9:
            message += '\n'
    return message


def get_msg_for_stats_last_n_matches(data: Dict, matches_count: int, faceit_nickname: str) -> str:
    """Возвращает сообщение со статистикой за последние n матчей"""
    message = f'<b>Статистика {faceit_nickname} за последние {matches_count} матчей:</b>'
    message += f'{get_emojies_string(kd=data["kd"])}' \
               f'{get_emojies_string(rating=data["avg_rating_1"])}' \
               f'{get_emojies_string(avg_kills=data["avg_kills"])}' \
               f'\nСреднее количество смертей - <b>{data["avg_deaths"]}</b>' \
               f'\nКоличество эйсов - <b>{data["aces"]}</b>' \
               f'\nQuadro kills - <b>{data["quadro_kills"]}</b>' \
               f'\nTriple kills - <b>{data["triple_kills"]}</b>' \
               f'\nDouble kills - <b>{data["double_kills"]}</b>' \
               f'\nКоличество убийств в голову - <b>{data["hs_count"]}</b>' \
               f'\nПроцент убийств в голову - <b>{data["hs_percent"]}%</b>' \
               f'\nКоличество MVP - <b>{data["mvps"]}</b> ⭐️'
    return message


def get_emojies_string(kd: float = None, rating: float = None, avg_kills: float = None) -> str:
    if kd:
        message = f'\nK/D - <b>{kd}</b> '
        if kd <= 1.0:
            message += '❌'
        elif 1.0 < kd < 1.20:
            message += '✅'
        elif kd >= 1.20:
            message += '🔥'
    elif rating:
        message = f'\nРейтинг 1.0 - <b>{rating}</b> '
        if rating <= 1.0:
            message += '❌'
        elif 1.0 < rating < 1.15:
            message += '✅'
        elif rating >= 1.15:
            message += '🔥'
    elif avg_kills:
        message = f'\nСреднее количество убийств - <b>{avg_kills}</b> '
        if avg_kills <= 16.0:
            message += '❌'
        elif 16.0 < avg_kills < 21.0:
            message += '✅'
        elif avg_kills >= 21:
            message += '🔥'
    else:
        message = ''
    return message


