from aiogram import types


kb = [
    [
        types.KeyboardButton(text="Anekdot"),
        types.KeyboardButton(text='Second button'),
        types.KeyboardButton(text='test'),
        types.KeyboardButton(text='Категорії'),
        types.KeyboardButton(text='Coffee'),
        types.KeyboardButton(text='Погода')
    ],
]

keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Обери меню"
    )
