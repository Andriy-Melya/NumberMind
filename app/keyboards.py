from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

setting_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='2'), KeyboardButton(text='3'), KeyboardButton(text='4'), KeyboardButton(text='5')],
    [KeyboardButton(text='6'), KeyboardButton(text='7'), KeyboardButton(text='8'), KeyboardButton(text='9')]
], resize_keyboard=True)

play_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Грати', callback_data='play_game')],
    [InlineKeyboardButton(text='Налаштування', callback_data='settings'), InlineKeyboardButton(text='Правила ГРИ', callback_data='help')],
    [InlineKeyboardButton(text='Challenge', callback_data='challenge')]])

challenge_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Взяти участь у челенжі', callback_data='start_challenge')]])

res_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Таблиця результатів', callback_data='table_result')]])

main_challenge_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Мій результат', callback_data='result_challenge')],
    [InlineKeyboardButton(text='Покинути челендж', callback_data='exit_challenge')]])

admin_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Грати', callback_data='play_game')],
    [InlineKeyboardButton(text='Налаштування', callback_data='settings'), InlineKeyboardButton(text='Правила ГРИ', callback_data='help')],
    [InlineKeyboardButton(text='Challenge', callback_data='challenge')],
    [InlineKeyboardButton(text='Створити ЧЕЛЕНДЖ', callback_data='create_challenge')],
    [InlineKeyboardButton(text='Завершити ЧЕЛЕНДЖ', callback_data='EXIT_challenge')],
    [InlineKeyboardButton(text='Таблиця результатів', callback_data='table_result')],
    [InlineKeyboardButton(text='Скинути таблицю результатів', callback_data='table_result_zero')]
])
