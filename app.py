# импортируем executor для обращения на сервера Телеграм
from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_startup import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db.db_api import db_API



async def on_startup(dp):

    await set_default_commands(dp)
    db_API.check_table()

    await on_startup_notify(dp=dp)


# запуск поллинга
if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)