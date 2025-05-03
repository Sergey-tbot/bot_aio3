from aiogram import Router, F, Bot
from aiogram.types import Message
from boto3.dynamodb.conditions import Key, Attr
from data.cfg import my_group, list_admin
from data.config_bot import table_welcome, table_message
from lexicon import bad_words_list, reminders
from keyboards.keyboard import welcome_button
from aiogram.exceptions import TelegramAPIError
import re
import random

from datetime import datetime, timedelta

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
async def group_admin(message: Message):
    if message.from_user.id not in list_admin:  # Игнорирует админов
        text_message = filter_user_text(message.text)
        # Стирает сообщения меньше 5 слов
        if len(text_message) <= 5 or \
                db_message(message.from_user.id, message.message_id, message.text, message.date.strftime('%Y%m%d%H%M')):
            try:
                await message.delete()
            except TelegramAPIError:
                print('Сообщение не удалено')
        elif filter_bad_words(text_message):  # Фильтр мата
            await message.reply('Выражайтесь культурнее, пожалуйста!')

@router.message(F.new_chat_members)
async def user_joined(message: Message, bot: Bot):
    try:
        await message.delete()
    except:
        print('Message Nof Found')
    new_user_name = ''
    for user in message.new_chat_members:
        new_user_name += user.full_name
    answer = await message.answer(f'{new_user_name}, добро пожаловать в чат "Геодезия работа"!\nПожалуйста '
                                  f'ознакомьтесь с полными правилами чата, нажав кнопу ниже.\n\n~~~~~~~~~~~~~\n'

                                  f'{random.choice(reminders.reminders)}',
                                  disable_notification=True, reply_markup=welcome_button)
    try:
        await bot.delete_message(message.chat.id, id_last_message(answer.message_id))
    except TelegramAPIError:
        print('Message delete NO BOT')


# Обработчик сообщений для других групп
@router.message()
async def other_group(message: Message):
    await message.answer(f'Привет. Я предназначен для работы только в одной конкретной группе. Если хотите'
                         f' воспользоваться функционалом данного бота, свяжитесь с разработчиком: '
                         f'https://t.me/L_Sergey_Vladimirovich')


# ~~~~~~~~~~~~~~~~ Работа с базой данных ~~~~~~~~~~~~~~~~~~
# Сохранение id_message для удаления
def id_last_message(id_message):
    try:
        response = table_welcome.get_item(Key={'id': 1})
    except Exception as e:
        print(f'Ошибка: {e}')
    else:
        id_message_old = int(response['Item']['id_messages']['id_message'])

    table_welcome.update_item(
        Key={
            'id': 1,
        },
        UpdateExpression="set id_messages.id_message = :d",
        ExpressionAttributeValues={
            ':d': id_message,
        },
        ReturnValues="UPDATED_NEW"
    )

    return id_message_old


# Загрузка и сохранение в базу сообщений пользователя
def db_message(id_user, id_message, text, date_message):
    uniq = False
    time_check = int((datetime.now() - timedelta(days=7)).strftime('%Y%m%d%H%M'))

    try:
        response = table_message.scan(
            FilterExpression=Attr('date_message').lt(time_check)
        )
        for item in response.get('Items', []):  # Чистит базу от старых сообщений
            table_message.delete_item(
                Key={
                    'id_user': item['id_user'],
                    'date_message': item['date_message']
                }
            )

        response = table_message.query(
            KeyConditionExpression=Key('id_user').eq(id_user)
        )

        msg = response.get('Items', [])


        if msg:
            for data in msg:
                if text.find(data['message_text']['text']) != -1 or data['message_text']['text'].find(text) != -1:
                    uniq = True
                    break

        if not uniq:
            table_message.put_item(
                Item={
                    'id_user': id_user,
                    'date_message': int(date_message),
                    'message_text': {
                        'text': text,
                        'id_message': int(id_message)
                    }
                }
            )

    except Exception as e:
        print(f'Произошла ошибка: {e}')

    return uniq
