from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

rmk = ReplyKeyboardRemove()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☕ Искать собеседника")
        ],
        [
            KeyboardButton(text="🍪 Профиль")
        ]
    ],
    resize_keyboard=True
)

reg_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Зарегистрироваться")
        ]
    ],
    resize_keyboard=True
)

search_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Остановить поиск", callback_data="search_stop")
        ],
    ],
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить био", callback_data="change_bio")
        ],
        [
            InlineKeyboardButton(text="На главное меню", callback_data="go_back")
        ],
    ],
)

chatting_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/stop_chatting",)
        ],
        [
            KeyboardButton(text="/next")
        ]
    ],
    resize_keyboard=True
)