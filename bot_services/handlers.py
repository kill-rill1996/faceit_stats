import requests
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
import os

from full_statistic import read_players_nickname_from_file, get_full_stats_for_player
from bot_services.keyboards import cancel_keyboard, main_keyboard, create_players_inline_keyboard, \
    create_players_stats_inline_keyboard, cancel_inline_keyboard, create_back_inline_keyboard
from database.services import get_all_players_nickname_from_db, add_to_database, get_player_info_from_db, \
    get_player_matches_from_db
from bot_services.bot_init import bot


class FSMStart(StatesGroup):
    nickname = State()


async def greeting(message: types.Message):
    await FSMStart.nickname.set()
    await message.answer('Для получения статистики введите nickname faceit.', reply_markup=cancel_keyboard)


async def get_nickname_faceit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname_faceit'] = message.text

    async with state.proxy() as data:
        if data['nickname_faceit'] not in get_all_players_nickname_from_db():
            await message.answer('Идет сбор статистики, подождите...📈')
            player_full_stat = get_full_stats_for_player(data['nickname_faceit'])
            add_to_database(player_full_stat)
            # with open(f'{PLAYERS_LIST}', 'a') as f:
            #     f.write(f'\n{data["nickname_faceit"]}')
            await message.answer('Ваш nickname добавлен в базу данных.', reply_markup=main_keyboard)
        else:
            await message.answer('Ваш nickname уже был добавлен в базу.', reply_markup=main_keyboard)

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ок', reply_markup=main_keyboard)


async def all_players_handler(message: types.Message):
    all_nicknames = get_all_players_nickname_from_db()
    await message.answer('Список игроков', reply_markup=create_players_inline_keyboard(all_nicknames))


def get_player_avatar_path(player):
    if os.path.exists(f'players_avatars/{player.faceit_nickname}.jpeg'):
        return f'players_avatars/{player.faceit_nickname}.jpeg'
    else:
        if player.avatar:
            response = requests.get(player.avatar)
            with open(f'players_avatars/{player.faceit_nickname}.jpeg', 'wb') as fd:
                fd.write(response.content)
            # await save_avatar(player.avatar, player.faceit_nickname)
            return f'players_avatars/{player.faceit_nickname}.jpeg'
        else:
            return 'players_avatars/default.png'


async def player_handler(callback: types.CallbackQuery):
    """Вывод основной статистики и клавиатуры меню у конкретного игрока. Callback.data - <faceit_nickname>"""
    print(callback.data)
    faceit_nickname = callback.data.split('$&*')[1]
    print(faceit_nickname)
    player = get_player_info_from_db(faceit_nickname)
    player_avatar_path = get_player_avatar_path(player)
    text_message = f'{player.faceit_nickname}' \
                   f'\nLVL - {player.faceit_lvl}' \
                   f'\nELO - {player.faceit_elo}' \
                   f'\nМатчей - {player.stats.matches_count}' \
                   f'\nWinrate - {player.stats.winrate}%'
    await bot.send_photo(callback.message.chat.id,
                         photo=InputFile(player_avatar_path),
                         caption=text_message,
                         reply_markup=create_players_stats_inline_keyboard(faceit_nickname))
    await callback.answer()


async def player_info_handler(callback: types.CallbackQuery):
    """Вывод полной статистики и клавиатуры меню у конкретного игрока. Callback.data - <info$&*nickname>"""
    faceit_nickname = callback.data.split('$&*')[1]
    player = get_player_info_from_db(faceit_nickname)
    text_message = f'{faceit_nickname} статистика:' \
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
    await bot.send_message(callback.message.chat.id,
                           text=text_message,
                           reply_markup=create_back_inline_keyboard(faceit_nickname))
    await callback.answer()


async def player_matches_handler(callback: types.CallbackQuery):
    """Вывод матчей игрока и клавиатуры меню у конкретного игрока. Callback.data - <matches$&*nickname>"""
    faceit_nickname = callback.data.split('$&*')[1]
    matches = get_player_matches_from_db(faceit_nickname)
    text_message = f'Матчи {faceit_nickname}:'
    for count, match in enumerate(matches):
        sub_text = f'\n{count + 1}. {match.map} | Rating 1.0: {match.rating_1} | K/D: {match.kd} | Убийств: {match.kills} | Смертей: {match.deaths} | ' \
                   f'Эйсов: {match.aces} | Quadro kills: {match.quadro_kills} | Triple kills: {match.triple_kills} | ' \
                   f'Double kills: {match.double_kills} | HS: {match.hs_percent}% | MVP: {match.mvps}'
        text_message += sub_text
        if count != 19:
            text_message += '\n'

    await bot.send_message(callback.message.chat.id, text=text_message,
                           reply_markup=create_back_inline_keyboard(faceit_nickname))
    await callback.answer()


class FSMMatches(StatesGroup):
    matches_count = State()


async def player_last_stats(callback: types.CallbackQuery):
    """Вывод статистики за последние n матчей. Callback.data - <last_stats$&*nickname>"""
    await FSMMatches.matches_count.set()
    msg = await callback.message.answer('Для получения статистики введите количество матчей.', reply_markup=cancel_inline_keyboard)
    # запись в класс для последующего удаления
    FSMMatches.message = msg


async def last_n_matches_message_handler(request: types.Message | types.CallbackQuery, state: FSMContext):
    """Вывод определенного количества матчей по количеству из сообщения"""
    if type(request) == types.Message:
        try:
            int(request.text)
            await FSMMatches.message.delete()
            await request.answer(f'Ваше сообщение {request.text}')
        except ValueError:
            await request.reply('Необходимо ввести число')
            return

    elif type(request) == types.CallbackQuery:
        await request.message.delete()
        await bot.send_message(request.message.chat.id, f'Callback data - {request.data}')
        await request.answer()

    await state.finish()


async def cancel_last_n_matches(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.message.answer('Ок', reply_markup=main_keyboard)


async def empty(message: types.Message):
    await message.answer('Такой команды нет.')
    await message.delete()


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cancel_handler, commands=['отмена'], state="*")
    dispatcher.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dispatcher.register_message_handler(greeting, commands=['start'], state=None)
    dispatcher.register_message_handler(get_nickname_faceit, state=FSMStart.nickname)

    # Список всех игроков
    dispatcher.register_message_handler(all_players_handler, Text(equals='Список игроков', ignore_case=True))

    # получение информации по определенному количеству матчей
    dispatcher.register_callback_query_handler(cancel_last_n_matches,
                                               lambda callback: callback.data == 'cancel',
                                               state=FSMMatches.matches_count)
    dispatcher.register_message_handler(last_n_matches_message_handler, state=FSMMatches.matches_count)
    dispatcher.register_callback_query_handler(last_n_matches_message_handler,
                                               lambda callback: callback.data.split('_')[0] == 'matchescount',
                                               state=FSMMatches.matches_count)

    # хэндлеры в профиле игрока
    dispatcher.register_callback_query_handler(player_info_handler,
                                               lambda callback: callback.data.split('$&*')[0] == 'info')
    dispatcher.register_callback_query_handler(player_matches_handler,
                                               lambda callback: callback.data.split('$&*')[0] == 'matches')
    dispatcher.register_callback_query_handler(player_last_stats,
                                               lambda callback: callback.data.split('$&*')[0] == 'last_stats', state=None)

    # хэгдлер для перехода к одному игроку
    dispatcher.register_callback_query_handler(player_handler, lambda callback: callback.data.split('$&*')[1] in get_all_players_nickname_from_db())

    # незарегистрированные команды
    dispatcher.register_message_handler(empty)


