from loader import dp, bot, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from states.user_state import UserStates
from utils.db.db_api import db_API

from data.config import SUPPORT_CHAT_ID

# обработка callback запроса при нажатии инлайн кнопки
@dp.callback_query_handler(Text("support"), state=None)
async def callback_data(callback: types.CallbackQuery):

    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Отменить обращение", callback_data="exit_support"))

    await bot.edit_message_text('Напишите свой вопрос ✍️', callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)

    await UserStates.writing_message.set()


@dp.callback_query_handler(Text("support"), state=UserStates.waiting_answer_from_support)
async def awaiting_answer(callback: types.CallbackQuery):

    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("Завершить обращение", callback_data="remove_session_user"))

    await bot.edit_message_text('Вы уже обратились в поддержку, можете дополнить сообщение или завершить обращение ✍️\n\nВам ответит первый освободившийся оператор', callback.message.chat.id, callback.message.message_id, reply_markup=keyboard)


# callback'и отмены и завершения сессий
@dp.callback_query_handler(Text("exit_support"), state=UserStates.writing_message)
async def cancel_question(callback: types.CallbackQuery, state: FSMContext):

    await bot.delete_message(callback.message.chat.id, callback.message.message_id)
    await state.finish()


@dp.callback_query_handler(Text("remove_session_user"), state=UserStates.waiting_answer_from_support)
async def remove_session_user(callback: types.CallbackQuery, state: FSMContext):

    parent_id = db_API.select_parent_id(callback.from_user.id)
    
    ended_session_kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Сессия закрыта', callback_data='ended_session'))

    await bot.edit_message_reply_markup(SUPPORT_CHAT_ID, parent_id, reply_markup=ended_session_kb)
    await bot.send_message(SUPPORT_CHAT_ID, f"Пользователь <code>{callback.message.chat.id}</code> завершил сессию")

    db_API.cancel_ids(callback.from_user.id)

    await callback.answer()
    await bot.send_message(callback.message.chat.id, "Вы завершили обращение в поддержку")

    await state.finish()


@dp.callback_query_handler(Text("remove_session_admin"))
async def remove_session_support(callback: types.CallbackQuery, state: FSMContext):

    info = db_API.find_user_id(callback.message.message_id)
    
    ended_session_kb = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Сессия закрыта', callback_data='ended_session'))

    state = dp.current_state(chat=info, user=info)
    await state.set_state(state=None)

    await bot.edit_message_reply_markup(callback.message.chat.id, callback.message.message_id, reply_markup=ended_session_kb)

    await bot.send_message(info, "Оператор завершил сессию")
    await bot.send_message(callback.message.chat.id, f"{callback.from_user.username} завершил сессию с <code>{info}</code>")

    db_API.cancel_ids(callback.from_user.id)

    await callback.answer()
    await state.finish()


@dp.callback_query_handler(Text("ended_session"))
async def ended_session_message(callback: types.CallbackQuery):
    await callback.answer()