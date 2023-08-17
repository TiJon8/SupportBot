from loader import dp, bot, types


# обработчик команды start
@dp.message_handler(commands=['start'])
async def start_command_user(message: types.Message):

    await bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKH2TcEetyfliMxmt4NHwBgHvJ9csRAALzAgACtXHaBneinRza8T0KMAQ')
    await bot.send_message(message.chat.id, "Привет, это шаблон бота поддержки. Хочешь связаться с тех поддержкой? Напиши команду /support 😉")


# Обработка команды support
@dp.message_handler(commands=['support'], state='*')
async def ask_question(message: types.Message):

    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Поддержка", callback_data='support'))

    await bot.send_message(message.chat.id, "Чтобы написать сообщение тех поддержке, нажмите ниже", reply_markup=keyboard)
