from loader import dp, bot, types
from aiogram.dispatcher.filters import IsReplyFilter, IDFilter, ChatTypeFilter

from aiogram.dispatcher import FSMContext
from states.user_state import UserStates
from utils.db.db_api import db_API

from data.config import SUPPORT_CHAT_ID

import json

# оработка сообщения пользователя и отправка в чат операторам
@dp.message_handler(state=UserStates.writing_message)
async def forward_question_to_support(message: types.Message, state: FSMContext):

    # lmessage_id = message.message_id -1
    await bot.delete_message(message.chat.id, message.message_id-1)

    keyboard = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('Завершить сессию', callback_data='remove_session_admin'))

    async with state.proxy() as data:
        data["writing_message"] = message.text

    async with state.proxy() as message_id:
        message_id["writing_message"] = message.message_id


    a = await bot.send_message(SUPPORT_CHAT_ID, text=f'{data["writing_message"]}\n\n<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>, @{message.from_user.username}, (#ID{message.from_user.id})\n\n<i>Чтобы ответить, нажмите reply и введите сообщение</i> | <code>{message.from_user.id}</code>', reply_markup=keyboard, disable_web_page_preview=True)

    isin = db_API.isinstancedb(message.from_user.id)
    if not isin:
        db_API.add_new_user(message.from_user.id, a.message_id)
    else:
        db_API.update_parent_msg_id(message.from_user.id, a.message_id)

    await bot.send_message(message.chat.id, 'Ваше сообщение отправленно в тех поддержку. Чтобы завершить обращение введите команду /stop\n\nОжидайте ответа...')

    await UserStates.waiting_answer_from_support.set()



@dp.message_handler(state=UserStates.waiting_answer_from_support)
async def add_question(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        data["writing_message"] = message.text

    async with state.proxy() as message_id:
        message_id["writing_message"] = message.message_id

    info = db_API.check_ids(message.from_user.id)
    if info[1] == None:
        child_messages = []
        b = await bot.send_message(SUPPORT_CHAT_ID, text=f'{data["writing_message"]}\n\n<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>, @{message.from_user.username}, (#ID{message.from_user.id})\n\n<code>Дополнение от {message.from_user.id}</code>', disable_web_page_preview=True, reply_to_message_id=info[0])
        
        child_messages.append(b.message_id)
        db_API.update_child_ids(json.dumps(child_messages), message.from_user.id)
    elif info[1] != None:
        child_messages = json.loads(info[1])
        b = await bot.send_message(SUPPORT_CHAT_ID, text=f'{data["writing_message"]}\n\n<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>, @{message.from_user.username}, (#ID{message.from_user.id})\n\n<code>Дополнение от {message.from_user.id}</code>', disable_web_page_preview=True, reply_to_message_id=child_messages[-1])
        
        child_messages.append(b.message_id)
        db_API.update_child_ids(json.dumps(child_messages), message.from_user.id)



# ответ оператора пользователю
@dp.message_handler(IsReplyFilter(is_reply=True), IDFilter(chat_id=SUPPORT_CHAT_ID))
async def answer_for_user(message: types.Message):

    message_to_reply = message.reply_to_message.text
    user_id = message_to_reply[message_to_reply.find('D')+1 : message_to_reply.find(')')]
    
    if message.reply_to_message.from_user.is_bot == False:
        pass
    else:
        isin = db_API.select_parent_id(user_id)
        if isin:
            await bot.send_message(chat_id=user_id, text=message.text)
        else:
            await message.reply(f'<b>Оповещение</b>\n\nПользователь <code>{user_id}</code> не в активной сессии, <u>не отвечайте на это сообщение</u>')


# обработка любых сообщений
@dp.message_handler(ChatTypeFilter(types.ChatType.PRIVATE), state=None)
async def spam(message: types.Message):
    await bot.send_message(message.chat.id, "Данный бот создан для технических вопросов, чтобы связаться с поддержкой введите /support")