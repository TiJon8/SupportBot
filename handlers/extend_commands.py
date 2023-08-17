from loader import dp, bot, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from states.user_state import UserStates
from utils.db.db_api import db_API

from data.config import SUPPORT_CHAT_ID

# обработка команды завершения сессии с поддержкой пользователем
@dp.message_handler(Command('stop'), state=UserStates.waiting_answer_from_support)
async def remove_session_user_command(message: types.Message, state: FSMContext):

    parent_id = db_API.select_parent_id(message.from_user.id)
    
    ended_session_kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Сессия закрыта', callback_data='ended_session'))

    await bot.edit_message_reply_markup(SUPPORT_CHAT_ID, parent_id, reply_markup=ended_session_kb)
    await bot.send_message(SUPPORT_CHAT_ID, f"Пользователь <code>{message.from_user.id}</code> завершил сессию ☎️")

    db_API.cancel_ids(message.from_user.id)

    await bot.send_message(message.chat.id, "Вы завершили обращение в поддержку")

    await state.finish()