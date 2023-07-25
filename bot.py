from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token='5343916790:AAF-Ua72J2AHwhYMw1RFqACfhC33Fk9aRVI')
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def send_hello_message(message: types.Message):
    await bot.send_message(message.chat.id, message)
    await bot.send_message(message.chat.id, 'Привет, мир!')

executor.start_polling(dispatcher=dp)