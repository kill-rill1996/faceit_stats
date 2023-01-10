from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from config import API_BOT_TOKEN
from .fsm_start import greeting, get_nickname_faceit, cancel_handler, FSMStart

API_TOKEN = API_BOT_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(cancel_handler, commands=['отмена'], state="*")
    dispatcher.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dispatcher.register_message_handler(greeting, commands=['start'], state=None)
    dispatcher.register_message_handler(get_nickname_faceit, state=FSMStart.nickname)

