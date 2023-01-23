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
    """Возвращает сообщение со статистикой в 20 матчах"""
    message = f'<b>Матчи {faceit_nickname}:</b>'
    for count, match in enumerate(matches):
        sub_text = f'\n<b>{count + 1}.</b> <b>{match.map}</b> {match.score} {match.result} | Rating 1.0: {match.rating_1} | K/D: {match.kd} | Убийств: {match.kills} | Смертей: {match.deaths} | ' \
                   f'Эйсов: {match.aces} | Quadro kills: {match.quadro_kills} | Triple kills: {match.triple_kills} | ' \
                   f'Double kills: {match.double_kills} | HS: {match.hs_percent}% | MVP: {match.mvps}'
        message += sub_text.replace('True', '✅').replace('False', '❌')
        if count != 9:
            message += '\n'
    return message


def get_message_for_best_hs_players(players: List[tables.PlayerStats]) -> str:
    """Возвращает 10 лучших игроков по avg_hs"""
    message = f'<b>Игроки с лучшим hs:</b>'
    for count, player in enumerate(players):
        sub_text = f'\n{count + 1}. {player.player.faceit_nickname} - <b>{player.avg_hs_percent}%</b>'
        message += sub_text
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
               f'\n{get_emojies_string(hs_percent=data["hs_percent"])}' \
               f'\nКоличество MVP - <b>{data["mvps"]}</b> ⭐️'
    return message


def get_message_for_compare(stat1: tables.Player, stat2: tables.Player) -> str:
    message = f'Сравнение <b>{stat1.faceit_nickname}</b> и <b>{stat2.faceit_nickname}</b>\n'
    # Матчи
    if stat1.stats.matches_count > stat2.stats.matches_count:
        message += f'\n<b>Матчи:</b> ✅ {stat1.stats.matches_count} - {stat2.stats.matches_count} ❌'
    else:
        message += f'\n<b>Матчи:</b> ❌ {stat1.stats.matches_count} - {stat2.stats.matches_count} ✅'
    # Ело
    if stat1.faceit_elo > stat2.faceit_elo:
        message += f'\n<b>ELO:</b> ✅ {stat1.faceit_elo} - {stat2.faceit_elo} ❌'
    else:
        message += f'\n<b>ELO:</b> ❌ {stat1.faceit_elo} - {stat2.faceit_elo} ✅'
    # LVL
    if stat1.faceit_lvl > stat2.faceit_lvl:
        message += f'\n<b>LVL:</b> ✅ {stat1.faceit_lvl} - {stat2.faceit_lvl} ❌'
    elif stat1.faceit_lvl < stat2.faceit_lvl:
        message += f'\n<b>LVL:</b> ❌ {stat1.faceit_lvl} - {stat2.faceit_lvl} ✅'
    else:
        message += f'\n<b>LVL:</b> {stat1.faceit_lvl} - {stat2.faceit_lvl}'
    # Побед
    if stat1.stats.wins_count > stat2.stats.wins_count:
        message += f'\n<b>Побед:</b> ✅ {stat1.stats.wins_count} - {stat2.stats.wins_count} ❌'
    else:
        message += f'\n<b>Побед:</b> ❌ {stat1.stats.wins_count} - {stat2.stats.wins_count} ✅'
    # Winrate
    if stat1.stats.winrate > stat2.stats.winrate:
        message += f'\n<b>Winrate:</b> ✅ {stat1.stats.winrate}% - {stat2.stats.winrate}% ❌'
    else:
        message += f'\n<b>Winrate:</b> ❌ {stat1.stats.winrate}% - {stat2.stats.winrate}% ✅'
    # K/D
    if stat1.stats.avg_kd > stat2.stats.avg_kd:
        message += f'\n<b>Средний K/D:</b> ✅ {stat1.stats.avg_kd} - {stat2.stats.avg_kd} ❌'
    else:
        message += f'\n<b>Средний K/D:</b> ❌ {stat1.stats.avg_kd} - {stat2.stats.avg_kd} ✅'
    # Убийств
    if stat1.stats.kills_count > stat2.stats.kills_count:
        message += f'\n<b>Всего убийств:</b> ✅ {stat1.stats.kills_count} - {stat2.stats.kills_count} ❌'
    else:
        message += f'\n<b>Всего убийств:</b> ❌ {stat1.stats.kills_count} - {stat2.stats.kills_count} ✅'
    # HS%
    if stat1.stats.avg_hs_percent > stat2.stats.avg_hs_percent:
        message += f'\n<b>Процент HS:</b> ✅ {stat1.stats.avg_hs_percent}% - {stat2.stats.avg_hs_percent}% ❌'
    elif stat1.stats.avg_hs_percent < stat2.stats.avg_hs_percent:
        message += f'\n<b>Процент HS:</b> ❌ {stat1.stats.avg_hs_percent}% - {stat2.stats.avg_hs_percent}% ✅'
    else:
        message += f'\n<b>Процент HS:</b> {stat1.stats.avg_hs_percent}% - {stat2.stats.avg_hs_percent}%'
    # Aces
    if stat1.stats.aces > stat2.stats.aces:
        message += f'\n<b>Количество эйсов:</b> ✅ {stat1.stats.aces} - {stat2.stats.aces} ❌'
    else:
        message += f'\n<b>Количество эйсов:</b> ❌ {stat1.stats.aces} - {stat2.stats.aces} ✅'
    # Quadro kills
    if stat1.stats.quadro_kills > stat2.stats.quadro_kills:
        message += f'\n<b>Quadro kills:</b> ✅ {stat1.stats.quadro_kills} - {stat2.stats.quadro_kills} ❌'
    else:
        message += f'\n<b>Quadro kills:</b> ❌ {stat1.stats.quadro_kills} - {stat2.stats.quadro_kills} ✅'
    # Triple kills
    if stat1.stats.quadro_kills > stat2.stats.quadro_kills:
        message += f'\n<b>Triple kills:</b> ✅ {stat1.stats.triple_kills} - {stat2.stats.triple_kills} ❌'
    else:
        message += f'\n<b>Triple kills:</b> ❌ {stat1.stats.triple_kills} - {stat2.stats.triple_kills} ✅'
    # Double kills
    if stat1.stats.quadro_kills > stat2.stats.quadro_kills:
        message += f'\n<b>Double kills:</b> ✅ {stat1.stats.double_kills} - {stat2.stats.double_kills} ❌'
    else:
        message += f'\n<b>Double kills:</b> ❌ {stat1.stats.double_kills} - {stat2.stats.double_kills} ✅'
    # Deaths
    if stat1.stats.quadro_kills < stat2.stats.quadro_kills:
        message += f'\n<b>Смертей:</b> ✅ {stat1.stats.deaths_count} - {stat2.stats.deaths_count} ❌'
    else:
        message += f'\n<b>Смертей:</b> ❌ {stat1.stats.deaths_count} - {stat2.stats.deaths_count} ✅'
    # MVPs
    if stat1.stats.quadro_kills > stat2.stats.quadro_kills:
        message += f'\n<b>Количество MVP:</b> ✅ {stat1.stats.mvps} - {stat2.stats.mvps} ❌'
    else:
        message += f'\n<b>Количество MVP:</b> ❌ {stat1.stats.mvps} - {stat2.stats.mvps} ✅'
    # AVG Kills
    if stat1.stats.avg_kills > stat2.stats.avg_kills:
        message += f'\n<b>Среднее кол-во убийств:</b> ✅ {stat1.stats.avg_kills} - {stat2.stats.avg_kills} ❌'
    elif stat1.stats.avg_kills < stat2.stats.avg_kills:
        message += f'\n<b>Среднее кол-во убийств:</b> ❌ {stat1.stats.avg_kills} - {stat2.stats.avg_kills} ✅'
    else:
        message += f'\n<b>Среднее кол-во убийств:</b> {stat1.stats.avg_kills} - {stat2.stats.avg_kills}'
    return message


def get_emojies_string(kd: float = None, rating: float = None, avg_kills: float = None, hs_percent: int = None) -> str:
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
    elif hs_percent:
        message = f'Процент убийств в голову - <b>{hs_percent}%</b>'
        if hs_percent < 45:
            message += '❌'
        elif 45 <= hs_percent <= 50:
            message += '✅'
        elif hs_percent > 50:
            message += '🔥'
    else:
        message = ''
    return message