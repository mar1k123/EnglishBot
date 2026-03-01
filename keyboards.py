from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


stop_rkb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Стоп")]],
    resize_keyboard=True,
    one_time_keyboard=True,
)


def get_levels_keyboard() -> ReplyKeyboardMarkup:
    levels = [
        "Уровень A1",
        "Уровень A2",
        "Уровень B1",
        "Уровень B2",
        "Уровень C1",
    ]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=level)] for level in levels]
        + [[KeyboardButton(text="Отмена")], [KeyboardButton(text="Стоп")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# Left for compatibility with existing references (currently unused in active handlers).
main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="add")], [KeyboardButton(text="tryMe")]],
    resize_keyboard=True,
)
