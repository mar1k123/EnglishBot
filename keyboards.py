from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton) #тож самое что и Reply только Inline
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Заимпортил билдер (он нужен для того, чтобы не менять знаения через код)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton (text="add")],
    [KeyboardButton(text="tryMe")]
],                              resize_keyboard=True)











My_Profile = ["Git Hub"]


async def inline_profile(): #создали асинхронную функцию
    keyboard = InlineKeyboardBuilder()
    for profile in My_Profile: #rage для предметов в моих предметах
        keyboard.add(InlineKeyboardButton(text=profile, url="https://github.com/mar1k123?tab=repositories")) # добавили инлайн кнопки и в них ссылка
    return keyboard.adjust(1).as_markup() #adjust (2 or ....) - сколько кнопок будет в одном ряду, а as_markup() по дефолту



def main_menu_button(user_telegram_id: int):
    button = KeyboardButton(text="📜 Главное меню")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard


def add_button(user_telegram_id: int):
    button = KeyboardButton(text="Add words")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]])
    return keyboard










