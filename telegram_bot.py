from bot_services.bot_init import register_handlers, dp
from aiogram import executor


register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
