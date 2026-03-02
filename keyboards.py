from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from services.translation_service import STOP_BUTTON_TEXT

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


def get_translation_choice_keyboard(suggested: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=f"✅ Использовать: {suggested}")],
            [KeyboardButton(text="✍️ Ввести перевод вручную")],
            [KeyboardButton(text="❌ Отмена")],
            [KeyboardButton(text=STOP_BUTTON_TEXT)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def reminder_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔔 Включить"), KeyboardButton(text="🔕 Выключить")],
            [KeyboardButton(text="❌ Отмена")],
            [KeyboardButton(text=STOP_BUTTON_TEXT)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def reminder_interval_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="15 минут"), KeyboardButton(text="1 час")],
            [KeyboardButton(text="5 часов"), KeyboardButton(text="🛠 Свое время")],
            [KeyboardButton(text="❌ Отмена")],
            [KeyboardButton(text=STOP_BUTTON_TEXT)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


# Left for compatibility with existing references (currently unused in active handlers).
main = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="add")], [KeyboardButton(text="tryMe")]],
    resize_keyboard=True,
)
