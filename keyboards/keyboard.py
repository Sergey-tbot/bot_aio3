from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from data import cfg

url_button_welcome = InlineKeyboardButton(
    text="👉 💠️ Главное меню группы   👈",
    url=cfg.url_bot)

welcome_button = InlineKeyboardMarkup(inline_keyboard=[[url_button_welcome]])

# Кнопки в личке
button_1 = KeyboardButton(text='Правила группы')
button_2 = KeyboardButton(text='Поиск по черным спискам')
button_3 = KeyboardButton(text='Добавить в черные списки')
button_4 = KeyboardButton(text='Узнать причину бана')

keyboard_private = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button_1], [button_2], [button_3], [button_4]])

# Инлайн для добавления в Ч.С.
bl_add_org = InlineKeyboardButton(text='Организацию', callback_data='bl_add_org')
bl_add_sotr = InlineKeyboardButton(text='Сотрудника', callback_data='bl_add_sotr')
bl_add_stop = InlineKeyboardButton(text='⛔️Отмена', callback_data='cancel')
bl_add_save_false = InlineKeyboardButton(text='✏️Изменить', callback_data='bl_save_Edit')
bl_add_save_true = InlineKeyboardButton(text='💾 Сохранить', callback_data='bl_save_Save')
bl_add_cancel = InlineKeyboardMarkup(inline_keyboard=[[bl_add_stop]])
bl_search_personal = InlineKeyboardButton(text='Посмотреть мои записи', callback_data='black_list_my')
bl_add = InlineKeyboardMarkup(inline_keyboard=[[bl_add_org],[bl_add_sotr],[bl_search_personal]])
bl_add_save = InlineKeyboardMarkup(inline_keyboard=[[bl_add_save_true],[bl_add_save_false],[bl_add_stop]])
bl_add_edit_name = InlineKeyboardButton(text='Название/Ф.И.О.', callback_data='bl_edit_name')
bl_add_edit_contact = InlineKeyboardButton(text='Контакты', callback_data='bl_edit_contact')
bl_add_edit_comment = InlineKeyboardButton(text='Коментарий', callback_data='bl_edit_comment')
bl_add_edit = InlineKeyboardMarkup(inline_keyboard=[[bl_add_edit_name], [bl_add_edit_contact], [bl_add_edit_comment]])
bl_search_org = InlineKeyboardButton(text='Организаций', callback_data='black_list_org')
bl_search_sotr = InlineKeyboardButton(text='Сотрудников', callback_data='black_list_sotr')
bl_delete_u = InlineKeyboardButton(text='Удалить ⤴️', callback_data='bl_delete_user')
bl_delete_a = InlineKeyboardButton(text='Удалить ⤴️', callback_data='bl_delete_admin')

bl_delete = InlineKeyboardMarkup(inline_keyboard=[[bl_delete_u]])
bl_delete_admin = InlineKeyboardMarkup(inline_keyboard=[[bl_delete_a]])
bl_search = InlineKeyboardMarkup(inline_keyboard=[[bl_search_org, bl_search_sotr]])
bl_full_base_button = InlineKeyboardButton(text='Весь список', callback_data='full_base')
bl_full_base = InlineKeyboardMarkup(inline_keyboard=[[bl_full_base_button], [bl_add_stop]])

# Кнопики для админов
button_admin_1 = KeyboardButton(text='Admin')
button_admin_2 = KeyboardButton(text='Правила группы')
button_admin_3 = KeyboardButton(text='Поиск по черным спискам')
button_admin_4 = KeyboardButton(text='Добавить в черные списки')
keyboard_private_admin = ReplyKeyboardMarkup(resize_keyboard=True,
                                             keyboard=[[button_admin_1],
                                                       [button_admin_2],
                                                       [button_admin_3],
                                                       [button_admin_4]])

dfbd_admin_y = InlineKeyboardButton(text='Подтвердить', callback_data='dfbd_admin_y')
dfbd_admin_n = InlineKeyboardButton(text='Отмена', callback_data='dfbd_admin_n')
dfbd_admin = InlineKeyboardMarkup(inline_keyboard=[[dfbd_admin_y, dfbd_admin_n]])
silens_7days = InlineKeyboardButton(text='7 дней', callback_data='change_permission_7')
silens_up30_days = InlineKeyboardButton(text='+30 дней', callback_data='change_permission_+30')
silens_down30_days = InlineKeyboardButton(text='-30 дней', callback_data='change_permission_-30')
silens_forever = InlineKeyboardButton(text='Навсегда', callback_data='change_permission_forever')
silens_30_confirm = InlineKeyboardButton(text='Подтвердить', callback_data='change_permission_save')
ban_user = InlineKeyboardButton(text='Забанить участника', callback_data='ban_user_choice')
ban_user_y = InlineKeyboardButton(text='Да', callback_data='ban_user_yes')
ban_user_n = InlineKeyboardButton(text='Нет', callback_data='ban_user_no')
silens_choice = InlineKeyboardMarkup(inline_keyboard=[[silens_7days], [silens_up30_days], [silens_forever], [ban_user]])
change_30 = InlineKeyboardMarkup(inline_keyboard=[[silens_up30_days, silens_down30_days], [silens_30_confirm]])
change_up30_only = InlineKeyboardMarkup(inline_keyboard=[[silens_up30_days], [silens_30_confirm]])
ban_user_confirm = InlineKeyboardMarkup(inline_keyboard=[[ban_user_y, ban_user_n]])