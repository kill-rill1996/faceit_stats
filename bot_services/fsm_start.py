from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from aiogram.dispatcher import FSMContext

from config import PLAYERS_LIST
from full_statistic import read_players_nickname_from_file


class FSMStart(StatesGroup):
    nickname = State()


async def greeting(message: types.Message):
    await FSMStart.nickname.set()
    await message.answer('Для получения статистики введите nickname faceit.')


async def get_nickname_faceit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nickname_faceit'] = message.text

    async with state.proxy() as data:
        if data['nickname_faceit'] not in read_players_nickname_from_file():
            with open(f'{PLAYERS_LIST}', 'a') as f:
                f.write(f'\n{message.text}')
            await message.answer('Ваш nickname добавлен в базу данных.')
        else:
            await message.answer('Ваш nickname уже был добавлен в базу.')

    await state.finish()


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('Ок')








