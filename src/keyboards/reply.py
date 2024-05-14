from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

rmk = ReplyKeyboardRemove()

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☕ Искать собеседника")
        ],
        [
            KeyboardButton(text="🍪 Профиль")
        ],
        [
            KeyboardButton(text="👩🏿‍🤝‍👩🏿 Написать другу")
        ]
    ],
    resize_keyboard=True
)

reg_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✔️ Написать Био")
        ]
    ],
    resize_keyboard=True
)

search_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✋ Остановить поиск", callback_data="search_stop")
        ],
    ],
)

profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="👤 Изменить био", callback_data="change_bio")
        ],
        [
            InlineKeyboardButton(text="⬅️ На главное меню", callback_data="go_back")
        ],
    ]
)

chatting_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Закончить Диалог",)
        ],
        [
            KeyboardButton(text="🔎 Поиск нового собеседника")
        ],
        [
            KeyboardButton(text="🤝 Добавить в друзья")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

add_friend_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✔️️ Принять", callback_data="accept")
        ],
        [
            InlineKeyboardButton(text="❌ Отклонить", callback_data="decline")
        ],
    ],
)

permission_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✔️️ Принять", callback_data="perm_accept")
        ],
        [
            InlineKeyboardButton(text="❌ Отклонить", callback_data="perm_decline")
        ],
    ],
)
