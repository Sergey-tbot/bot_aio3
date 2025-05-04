import datetime as dt

from aiogram import types, Router, F, Bot
from boto3.dynamodb.conditions import Key, Attr

from data import cfg
from data.config_ydb import table_bl, table_message, table_banned_user
from keyboards import keyboard

router = Router()
router.message.filter(F.chat.type.in_({"private"}), F.from_user.id.in_(cfg.list_admin))

@router.message(F.text == 'Admin')
async def admin_dialog(message: types.Message):
    await message.reply('Возможно тут будет более полезный функционал.',
                        reply_markup=keyboard.keyboard_private_admin)


# Удаление Админом из Ч.С. по Коду DFBD*
@router.message(F.text.startswith('DFBD*'))
async def del_from_bd(message: types.Message):
    msg_split = message.text.split('*')
    from_user = int(msg_split[1])
    date = str(msg_split[2])
    response = table_bl.query(
        KeyConditionExpression=Key('from_user').eq(from_user) & Key('date').eq(date)
    )
    answer = f"Код:\n" \
             f"&lt;{message.text}&gt;\n" \
             f"Запись для удаления:\n\n" \
             f"Название/Ф.И.О.:\n" \
             f"{response['Items'][0]['body']['name']}\n\n" \
             f"Контакты (контактное лицо):\n" \
             f"{response['Items'][0]['body']['contact']}\n\n" \
             f"Комментарий (причина добавления):\n" \
             f"{response['Items'][0]['body']['comment']}\n\n" \
             f"Дата добавления:\n" \
             f"{str(dt.datetime.strptime(response['Items'][0]['date'], '%Y%m%d%H%M'))}\n\n"
    await message.answer(answer, reply_markup=keyboard.dfbd_admin)


# Проверка и подтверждение удаления из Ч.С.
@router.callback_query(F.data.startswith('dfbd_admin_'))
async def del_confirm(call: types.CallbackQuery):
    await call.answer()
    if call.data == 'dfbd_admin_y':

        data = call.message.text.split('DFBD*')[1].split('*')
        from_user = int(data[0])
        date = str(data[1])[:12]
        try:
            table_bl.delete_item(
                Key={'from_user': from_user,
                     'date': date}
            )
            await call.message.edit_text('Запись удалена за базы')
        except:
            await call.message.edit_text('Что-то пошло не так.')
    else:
        await call.message.edit_text('Окей. Не буду удалять.')


@router.message(F.forward_origin)
async def forwarded_message_to_ban(message: types.Message, bot: Bot):
    time_ban = dt.datetime.now() + dt.timedelta(days=30)  # Время бана.
    permissions = types.chat_permissions.ChatPermissions(can_send_messages=False)
    chat_id = cfg.my_group
    date_message = int(message.forward_date.strftime('%Y%m%d%H%M'))
    comment = '&lt;Комментария нет&gt;'
    try:
        id_user_to_ban = message.forward_from.id  # Если профиль открыт и можно получить ID
        response = table_message.query(
            KeyConditionExpression=Key('id_user').eq(id_user_to_ban),
            FilterExpression=Attr('date_message').eq(date_message)
        )
        name_user = message.forward_from.first_name
        if message.forward_from.last_name is not None:
            name_user = name_user + ' ' + message.forward_from.last_name

    except:  # Если профиль закрыт и ID не передаётся

        response = table_message.scan(FilterExpression=Attr('date_message').eq(date_message))
        id_user_to_ban = response['Items'][0]['id_user']
        name_user = message.forward_sender_name
    id_message = int(response['Items'][0]['message_text']['id_message'])
    await message.answer(f'Выдан кляп на 30 дней:\n\n'
                         f'Участник:\n{name_user}\n'
                         f'Сообщение:\n{message.text}\n\n'
                         f'------------------\n'
                         f'Комментарий админа:\n{comment}\n\n'
                         f'*Для изменеия/добавления комментария отправь сообщение ОТВЕТОМ на это сообщение*\n'
                         f'ID участника: {id_user_to_ban}\n\n'
                         f'Изменить?',
                         reply_markup=keyboard.silens_choice
                         )
    table_banned_user.put_item(
        Item={
            'id_user': id_user_to_ban,
            'body': {
                'message_text': message.text,
                'date': str(message.date),
                'comment': comment
            }
        }
    )
    await bot.restrict_chat_member(chat_id, id_user_to_ban, permissions, until_date=time_ban)
    try:  # Попытка удаления сообщения пользователя
        await bot.delete_message(chat_id, id_message)
    except:
        print('Сообщение из основной группы не получилось удалить')


@router.callback_query(F.data.startswith('change_permission_'))
async def permission_change(call: types.CallbackQuery, bot: Bot):
    await call.answer()
    chat_id = cfg.my_group
    time_ban = dt.datetime.now()
    permissions = types.chat_permissions.ChatPermissions(can_send_messages=False)
    id_user_to_ban = int(call.message.text.split('ID участника: ')[1].split('\n\n')[0])
    finish = True
    if call.data == 'change_permission_7':
        time_ban = time_ban + dt.timedelta(days=7)
        await call.message.edit_text(f'Кляп изменен и выдан на 7 дней.\n\n'
                                     f'{call.message.text[24:-11]}')
    elif call.data == 'change_permission_+30' or call.data == 'change_permission_-30':
        new_days_ban = int(call.message.text.split('Выдан кляп на ')[1].split(' дней:')[0]) + int(call.data[-3:])
        if new_days_ban > 30:
            markup = keyboard.change_30
        else:
            markup = keyboard.change_up30_only
        await call.message.edit_text(f'Выдан кляп на {new_days_ban} дней:'
                                     f'{call.message.text.split("дней:")[1][:-11]}\n\n'
                                     f'Подтверди',
                                     reply_markup=markup)
        finish = False
    elif call.data == 'change_permission_save':
        days_ban = int(call.message.text.split('Выдан кляп на ')[1].split(' дней:')[0])
        time_ban = time_ban + dt.timedelta(days=days_ban)
        await call.message.edit_text(f'{call.message.text[:-11]}\n\n'
                                     f'Готово')
    elif call.data == 'change_permission_forever':
        time_ban = None
        await call.message.edit_text(f'Выдан кляп навсегда:\n\n'
                                     f'{call.message.text[24:-11]}')
    if finish:
        await bot.restrict_chat_member(chat_id, id_user_to_ban, permissions, until_date=time_ban)


@router.callback_query(F.data.startswith('ban_user'))
async def ban_user(call: types.CallbackQuery, bot: Bot):
    await call.answer()
    if call.data == 'ban_user_choice':
        await call.message.edit_text(f'Выдать бан навсегда:\n\n'
                                     f'{call.message.text[24:-11]}\n\n'
                                     f'Уверен в выборе?',
                                     reply_markup=keyboard.ban_user_confirm)
    elif call.data == 'ban_user_yes':
        chat_id = cfg.my_group
        id_user_to_ban = int(call.message.text.split('ID участника: ')[1].split('\n\n')[0])
        await bot.ban_chat_member(chat_id, id_user_to_ban)
        await call.message.edit_text(f'Выдан{call.message.text[6:-16]}')
    elif call.data == 'ban_user_no':
        await call.message.edit_text(f'Выдан кляп на 30 дней:\n\n'
                                     f'{call.message.text[22:-16]}'
                                     f'Изменить?',
                                     reply_markup=keyboard.silens_choice)


@router.message(F.reply_to_message)
async def edit_comment(message: types.Message, bot: Bot):
    if message.reply_to_message.from_user.is_bot:
        markup = None
        if message.reply_to_message.text[-9:] == 'Изменить?':
            markup = keyboard.silens_choice
        await bot.edit_message_text(message.reply_to_message.html_text,
                                    chat_id=message.reply_to_message.chat.id,
                                    message_id=message.reply_to_message.message_id)
        parsing_message = message.reply_to_message.text.split('Комментарий админа:')
        new_answer = f"{parsing_message[0]}" \
                     f"Комментарий админа:\n{message.text}\n\n" \
                     f"*Для{parsing_message[1].split('*Для')[1]}"
        id_banned_user = int(message.reply_to_message.text.split('ID участника: ')[1].split('\n\n')[0])
        table_banned_user.update_item(
            Key={
                'id_user': id_banned_user
            },
            UpdateExpression="set body.comment = :c",
            ExpressionAttributeValues={
                ':c': message.text
            },
            ReturnValues="UPDATED_NEW"
        )
        await message.answer(new_answer, reply_markup=markup)
