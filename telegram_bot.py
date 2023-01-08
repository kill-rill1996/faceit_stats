from aiogram import Bot, Dispatcher, executor, types

from config import API_BOT_TOKEN
from database.database import Session
from database import tables

API_TOKEN = API_BOT_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    message_answer = 'Для получения статистики введите nickname faceit.\nВ формате !my_nickname'
    await message.reply(message_answer)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
