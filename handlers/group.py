from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import BaseFilter
from boto3.dynamodb.conditions import Key, Attr
from typing import Union
from data.cfg import my_group
from lexicon import bad_words_list
from data import cfg
import re
import random
import datetime as dt

router= Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))


# Разбивка текста в список для фильтрации
def filter_user_text(text_message):
    user_text = (text_message.lower()).strip()
    expression = r'[^\w\s]'
    user_text = re.sub(expression, "", user_text)
    return user_text.split()

# Поиск слов в библиотеке с матом
def filter_bad_words(text_message):
    for word in text_message:
        if word in bad_words_list.bad_words:
            return True



@router.message(F.chat.id == my_group)
async def group_admin(message: Message, admin_ids):
    await message.answer('hello people')
    print(message.chat.id)
    if message.from_user.id not in admin_ids:  # Игнорирует админов
        text_message = filter_user_text(message.text)
        # Стирает сообщения меньше 5 слов
        if len(text_message) <= 5 or \
                db_message(message.from_user.id, message.message_id, message.text, message.date.strftime('%Y%m%d%H%M')):
            try:
                await message.delete()
            except:
                print('Сообщение не удалено')
        elif filter_bad_words(text_message):  # Фильтр мата
            await message.reply('Выражайтесь культурнее, пожалуйста!')


# async def user_joined(message: types.Message):
#     try:
#         await message.delete()
#     except:
#         print('Message Nof Found')
#     new_user_name = message['new_chat_member']['first_name']
#     answer = await message.answer(f'{new_user_name}, добро пожаловать в чат "Геодезия работа"!\nПожалуйста '
#                                   f'ознакомьтесь с полными правилами чата, нажав кнопу ниже.\n\n~~~~~~~~~~~~~\n'
#
#                                   f'{random.choice(reminders.reminders)}',
#                                   disable_notification=True, reply_markup=button.welcome_button)
#     try:
#         await bot.delete_message(message.chat.id, id_last_message(answer.message_id))
#     except:
#         print('Message delete NO BOT')


# Обработчик сообщений для других групп
@router.message()
async def other_group(message: Message):
    await message.answer(f'Привет. Я предназначен для работы только в одной конкретной группе. Если хотите'
                         f' воспользоваться функционалом данного бота, свяжитесь с разработчиком: '
                         f'https://t.me/L_Sergey_Vladimirovich')


# # ~~~~~~~~~~~~~~~~ Работа с базой данных ~~~~~~~~~~~~~~~~~~
# # Сохранение id_message  для удаления
# def id_last_message(id_message):
#     try:
#         response = table_welcome.get_item(Key={'id': 1})
#     except:
#         print('Error')
#     else:
#         id_message_old = int(response['Item']['id_messages']['id_message'])
#
#     table_welcome.update_item(
#         Key={
#             'id': 1,
#         },
#         UpdateExpression="set id_messages.id_message = :d",
#         ExpressionAttributeValues={
#             ':d': id_message,
#         },
#         ReturnValues="UPDATED_NEW"
#     )
#
#     return id_message_old
#
#
# # Загрузка и сохранение в базу сообщений пользователя
# def db_message(id_user, id_message, text, date_message):
#     time_check = int((dt.datetime.now() - dt.timedelta(days=7)).strftime('%Y%m%d%H%M'))
#     response = table_message.scan(FilterExpression=Attr('date_message').lt(time_check))
#     for item in response['Items']:   # Чистит базу от старых сообщений
#         try:
#             table_message.delete_item(
#                 Key={'id_user': item['id_user'],
#                      'date_message': item['date_message']})
#         except:
#             print('Что-то пошло не так.')
#     response = table_message.query(
#         KeyConditionExpression=Key('id_user').eq(id_user)
#     )
#     msg = response['Items']
#     uniq = False
#     if len(msg) != 0:
#         for data in msg:
#             if text.find(data['message_text']['text']) != -1 or data['message_text']['text'].find(text) != -1:
#                 uniq = True
#     if not uniq:
#         table_message.put_item(
#             Item={
#                 'id_user': id_user,
#                 'date_message': int(date_message),
#                 'message_text': {
#                     'text': text,
#                     'id_message': int(id_message),
#                 }
#             },
#         )
#     return uniq
