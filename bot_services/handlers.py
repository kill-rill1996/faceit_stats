from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from typing import Union

from bot_services.keyboards import create_cancel_keyboard, create_players_inline_keyboard, \
    create_players_stats_inline_keyboard, cancel_inline_keyboard, create_back_inline_keyboard, \
    create_best_players_inline_keyboard, create_main_keyboard
from bot_services.messages import get_message_for_player_info, get_text_for_player_matches_handler, \
    get_message_for_player_main_info, get_msg_for_stats_last_n_matches, get_message_for_best_elo_players, \
    create_message_for_best_players_in_category, get_message_for_compare, get_greeting_message

from database.services import get_all_players_nickname_from_db, get_player_info_from_db, get_player_matches_from_db, \
    get_players_stats_from_db, add_to_database
from bot_services.bot_init import bot
from bot_services.services import get_stats_for_n_matches, get_player_avatar_path
from bot_services.fsm import FSMStart, FSMMatches, FSMCompare
from full_statistic import get_full_stats_for_player


async def greeting_handler(message: types.Message):
    await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHcfhj0XjUTKUDZv9-oDbNw4l9VMrSJgAC-xgAAoXwIEhZtNXC9grBQy0E')
    msg = get_greeting_message()
    await message.answer(msg, parse_mode='html', reply_markup=create_main_keyboard())


async def add_new_player_handler(message: types.Message):
    await FSMStart.nickname.set()
    await message.answer('Для добавления аккаунта в базу данных и ежедневного обновления '
                         'статистики введите 🔑<b>nickname faceit</b> (с учетом регистра)',
                         reply_markup=create_cancel_keyboard(),
                         parse_mode='html')


async def save_nickname_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname_faceit'] = message.text

    async with state.proxy() as data:
        if data['nickname_faceit'] not in get_all_players_nickname_from_db():
            await message.answer('Идет сбор статистики, подождите...📈️'
                                 '\nЭто может занять до 10 минут в зависимости от вашего количества матчей')
            try:
                player_full_stat = get_full_stats_for_player(data['nickname_faceit'])
                add_to_database(player_full_stat)
                await message.answer('✅Ваш nickname добавлен в базу данных', reply_markup=create_main_keyboard())
            except Exception as e:
                print(e)
                await message.answer('❌При добавлении произошла ошибка, проверьте корректно ли введен ваш nickname',
                                     reply_markup=create_main_keyboard())
                await bot.send_sticker(message.chat.id, sticker='CAACAgIAAxkBAAEHcfZj0Xa2M9fO0f8ZF4lyZvNE6KoeagAC8BUAAsoz2UvNOg9kKyyIti0E')
        else:
            await message.answer(f'<b>{message.text}</b> уже есть в базе', reply_markup=create_main_keyboard(), parse_mode='html')

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ок', reply_markup=create_main_keyboard())


async def all_players_handler(message: Union[types.Message, types.CallbackQuery]):
    """Вывод списка всех игроков"""
    all_nicknames = get_all_players_nickname_from_db()
    if type(message) == types.Message:
        await message.answer('Список игроков', reply_markup=create_players_inline_keyboard(all_nicknames))
    else:
        await bot.send_message(message.message.chat.id, 'Список игроков', reply_markup=create_players_inline_keyboard(all_nicknames))


async def player_handler(callback: types.CallbackQuery):
    """Вывод основной статистики и клавиатуры меню у конкретного игрока. Callback.data - <faceit_nickname>"""
    faceit_nickname = callback.data.split('$&*')[1]
    player = get_player_info_from_db(faceit_nickname)
    player_avatar_path = get_player_avatar_path(player)
    text_message = get_message_for_player_main_info(player)
    await bot.send_photo(callback.message.chat.id,
                         photo=InputFile(player_avatar_path),
                         caption=text_message,
                         reply_markup=create_players_stats_inline_keyboard(faceit_nickname),
                         parse_mode='html')
    await callback.answer()


async def player_info_handler(callback: types.CallbackQuery):
    """Вывод полной статистики и клавиатуры меню у конкретного игрока. Callback.data - <info$&*nickname>"""
    faceit_nickname = callback.data.split('$&*')[1]
    player = get_player_info_from_db(faceit_nickname)
    text_message = get_message_for_player_info(faceit_nickname, player)
    await bot.send_message(callback.message.chat.id,
                           text=text_message,
                           reply_markup=create_back_inline_keyboard(faceit_nickname),
                           parse_mode='html')
    await callback.answer()


async def player_matches_handler(callback: types.CallbackQuery):
    """Вывод матчей игрока и клавиатуры меню у конкретного игрока. Callback.data - <matches$&*nickname>"""
    faceit_nickname = callback.data.split('$&*')[1]
    matches = get_player_matches_from_db(faceit_nickname)
    text_message = get_text_for_player_matches_handler(faceit_nickname, matches)
    await bot.send_message(callback.message.chat.id, text=text_message,
                           reply_markup=create_back_inline_keyboard(faceit_nickname),
                           parse_mode='html')
    await callback.answer()


async def player_last_stats_handler(callback: types.CallbackQuery):
    """Вывод статистики за последние n матчей. Callback.data - <last_stats$&*nickname>"""
    await FSMMatches.matches_count.set()
    msg = await callback.message.answer('Для получения статистики введите количество матчей или '
                                        'выберите из предложенных значений.', reply_markup=cancel_inline_keyboard)
    # запись в класс для последующего удаления
    FSMMatches.message = msg
    # запись в nickname для поиска матчей игрока
    FSMMatches.faceit_nickname = callback.data.split('$&*')[1]


async def last_n_matches_message_handler(request: Union[types.Message, types.CallbackQuery], state: FSMContext):
    """Вывод определенного количества матчей по количеству из сообщения"""
    if type(request) == types.Message:
        try:
            matches = get_player_matches_from_db(FSMMatches.faceit_nickname, count=int(request.text))  # возможно ValueError
            stats_for_n_matches = get_stats_for_n_matches([match.__dict__ for match in matches])
            await FSMMatches.message.delete()
            text_message = get_msg_for_stats_last_n_matches(stats_for_n_matches, len(matches), FSMMatches.faceit_nickname)
            await request.answer(text_message, parse_mode='html',
                                 reply_markup=create_back_inline_keyboard(FSMMatches.faceit_nickname))
        except ValueError:
            await FSMMatches.message.delete()
            await request.reply('Необходимо ввести число')
            # return

    elif type(request) == types.CallbackQuery:
        await request.message.delete()
        matches = get_player_matches_from_db(FSMMatches.faceit_nickname, count=int(request.data.split('_')[1]))
        stats_for_n_matches = get_stats_for_n_matches([match.__dict__ for match in matches])
        text_message = get_msg_for_stats_last_n_matches(stats_for_n_matches, len(matches), FSMMatches.faceit_nickname)
        await bot.send_message(request.message.chat.id, text_message, parse_mode='html',
                               reply_markup=create_back_inline_keyboard(FSMMatches.faceit_nickname))
        await request.answer()

    await state.finish()


async def cancel_last_n_matches_handler(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await callback.message.delete()
    await callback.message.answer('Ок', reply_markup=create_main_keyboard())


async def best_players_handlers(request: Union[types.CallbackQuery, types.Message]):
    if type(request) == types.CallbackQuery:
        await request.message.answer('Выберите категорию', reply_markup=create_best_players_inline_keyboard())
    elif type(request) == types.Message:
        await request.answer('Выберите категорию', reply_markup=create_best_players_inline_keyboard())


async def best_headshots_handler(callback: types.CallbackQuery):
    """Список игроков с лучшим показателем hs"""
    players_list = get_players_stats_from_db(order_by='hs', limit_count=10)
    players_list_sorted = sorted(players_list, key=lambda player: player.avg_hs_percent, reverse=True)
    await bot.send_sticker(callback.message.chat.id, sticker='CAACAgQAAxkBAAEHcfRj0XZHxl9aj9Y_8gbEAktfNgzlsgAC3hAAAqbxcR5kxlSjbBhzcS0E')
    message_answer = create_message_for_best_players_in_category(
        title='<b>Игроки с лучшим hs:</b>',
        high=50,
        low=45,
        players=players_list_sorted,
        category='avg_hs_percent')
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


async def best_rating_handler(callback: types.CallbackQuery):
    """Список игроков с лучшим показателем rating 1.0"""
    players_list = get_players_stats_from_db(order_by='rating', limit_count=10)
    players_list_sorted = sorted(players_list, key=lambda player: player.rating_1, reverse=True)
    message_answer = create_message_for_best_players_in_category(
        title='<b>Топ игроков по рейтингу 1.0:</b>',
        high=1.10,
        low=1.05,
        players=players_list_sorted,
        category='rating_1')
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


async def best_kd_handler(callback: types.CallbackQuery):
    """Список игроков с лучшим показателем K/D"""
    players_list = get_players_stats_from_db(order_by='kd', limit_count=10)
    players_list_sorted = sorted(players_list, key=lambda player: player.avg_kd, reverse=True)
    message_answer = create_message_for_best_players_in_category(
        title='<b>Игроки с лучшим K/D:</b>',
        high=1.15,
        low=1.08,
        players=players_list_sorted,
        category='avg_kd')
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


async def best_aces_handler(callback: types.CallbackQuery):
    """Список игроков с наибольшим количеством эйсов"""
    players_list = get_players_stats_from_db(order_by='aces', limit_count=10)
    players_list_sorted = sorted(players_list, key=lambda player: player.aces, reverse=True)
    message_answer = create_message_for_best_players_in_category(
        title='<b>Игроки с наибольшим количеством эйсов:</b>',
        high=20,
        low=10,
        players=players_list_sorted,
        category='aces')
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


async def best_avg_kills_handler(callback: types.CallbackQuery):
    """Список игроков с наибольшим количеством средних убийств"""
    players_list = get_players_stats_from_db(order_by='avg_kills', limit_count=10)
    players_list_sorted = sorted(players_list, key=lambda player: player.avg_kills, reverse=True)
    message_answer = create_message_for_best_players_in_category(
        title='<b>Игроки с лучшим показателем среднего кол-ва убийств:</b>',
        high=22,
        low=19,
        players=players_list_sorted,
        category='avg_kills')
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


async def best_elo_handler(callback: types.CallbackQuery):
    """Список игроков с наибольшим количеством elo"""
    players_list = get_players_stats_from_db(order_by='elo', limit_count=10)
    message_answer = get_message_for_best_elo_players(players_list)
    await callback.message.answer(message_answer, parse_mode='html', reply_markup=create_best_players_inline_keyboard())


# Начало сравнения игроков, выбор первого игрока
async def compare_players_handler(message: types.Message):
    await FSMCompare.first_player.set()
    all_players = get_all_players_nickname_from_db()
    msg1 = await message.answer('Для сравнения необходимо выбрать двух игроков из списка.', reply_markup=create_cancel_keyboard())
    msg2 = await message.answer('Выберите первого игрока.',
                         reply_markup=create_players_inline_keyboard(all_players, best_players=False))
    FSMCompare.msg1 = msg1
    FSMCompare.msg2 = msg2


# Выбор второго игрока, запись первого
async def compare_second_player_handler(callback: types.CallbackQuery, state: FSMContext):
    await FSMCompare.msg1.delete()
    await FSMCompare.msg2.delete()
    first_player = callback.data.split('$&*')[1]
    async with state.proxy() as data:
        data['first_player'] = first_player
    await FSMCompare.next()
    all_players = get_all_players_nickname_from_db()
    all_players.remove(first_player)
    msg1 = await callback.message.answer(f'Первый игрок - <b>{first_player}</b>', reply_markup=create_cancel_keyboard(),
                                         parse_mode='html')
    msg2 = await callback.message.answer('Выберите второго игрока',
                                          reply_markup=create_players_inline_keyboard(all_players,
                                          best_players=False))
    FSMCompare.msg1 = msg1
    FSMCompare.msg2 = msg2


async def compare_results_handler(callback: types.CallbackQuery, state: FSMContext):
    await FSMCompare.msg1.delete()
    await FSMCompare.msg2.delete()
    second_player = callback.data.split('$&*')[1]
    async with state.proxy() as data:
        first_player = data['first_player']

    stat1 = get_player_info_from_db(first_player)
    stat2 = get_player_info_from_db(second_player)

    text_message = get_message_for_compare(stat1, stat2)
    await callback.message.answer(text_message, reply_markup=create_main_keyboard(), parse_mode='html')
    await state.finish()


async def empty(message: types.Message):
    await message.answer('Такой команды нет.', parse_mode='html')
    await message.delete()


def register_handlers(dispatcher: Dispatcher):
    # запуск бота, приветствие
    dispatcher.register_message_handler(greeting_handler, commands=['start'])

    # добавление нового игрока в базу данных
    dispatcher.register_message_handler(cancel_handler, commands=['отмена'], state="*")
    dispatcher.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dispatcher.register_message_handler(add_new_player_handler, Text(equals='➕ Добавить нового игрока'), state=None)
    dispatcher.register_message_handler(save_nickname_handler, state=FSMStart.nickname)

    # Список игроков
    dispatcher.register_message_handler(all_players_handler, Text(equals='📃 Список игроков', ignore_case=True))

    # Сравнение игроков
    dispatcher.register_message_handler(compare_players_handler,
                                        Text(equals='📊 Сравнить игроков', ignore_case=True),
                                        state=None)
    dispatcher.register_callback_query_handler(compare_second_player_handler,
                                               lambda callback: callback.data.split('$&*')[0] == 'menu',
                                               state=FSMCompare.first_player)
    dispatcher.register_callback_query_handler(compare_results_handler,
                                               lambda callback: callback.data.split('$&*')[0] == 'menu',
                                               state=FSMCompare.second_player)

    # получение информации по определенному количеству матчей
    dispatcher.register_callback_query_handler(cancel_last_n_matches_handler,
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
    dispatcher.register_callback_query_handler(player_last_stats_handler,
                                               lambda callback: callback.data.split('$&*')[0] == 'last_stats', state=None)

    # хэгдлер для перехода к одному игроку
    dispatcher.register_callback_query_handler(player_handler, lambda callback: callback.data.split('$&*')[0] == 'menu'
                                               and callback.data.split('$&*')[1] in get_all_players_nickname_from_db())

    # лучшие игроки
    dispatcher.register_message_handler(best_players_handlers, Text(equals='🔝 Лучшие игроки'))
    dispatcher.register_callback_query_handler(best_players_handlers, lambda callback: callback.data == 'best_players$&*')
    dispatcher.register_callback_query_handler(best_headshots_handler, lambda callback: callback.data == 'best$&*hs')
    dispatcher.register_callback_query_handler(best_rating_handler, lambda callback: callback.data == 'best$&*rating')
    dispatcher.register_callback_query_handler(best_kd_handler, lambda callback: callback.data == 'best$&*kd')
    dispatcher.register_callback_query_handler(best_aces_handler, lambda callback: callback.data == 'best$&*aces')
    dispatcher.register_callback_query_handler(best_elo_handler, lambda callback: callback.data == 'best$&*elo')
    dispatcher.register_callback_query_handler(best_avg_kills_handler, lambda callback: callback.data == 'best$&*avg_kills')
    dispatcher.register_callback_query_handler(all_players_handler, lambda callback: callback.data == 'best$&*cancel')


    # незарегистрированные команды
    dispatcher.register_message_handler(empty)


