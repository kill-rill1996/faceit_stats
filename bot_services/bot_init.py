from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text

from config import API_BOT_TOKEN
from database.services import get_all_players_nickname_from_db

API_TOKEN = API_BOT_TOKEN

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



