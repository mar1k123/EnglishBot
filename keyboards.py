from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardRemove)  # тож самое что и Reply только Inline
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Заимпортил билдер (он нужен для того, чтобы не менять знаения через код)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config
from aiogram import Router, Bot, F, types
bot = Bot(token=config.BOT_TOKEN)
router = Router()




main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton (text="add")],
    [KeyboardButton(text="tryMe")]
],                              resize_keyboard=True)

















# --- Reply-клавиатура для выбора уровня ---
def get_levels_keyboard() -> ReplyKeyboardMarkup:
    levels = ["Уровень A1", "Уровень A2", "Уровень B1", "Уровень B2", "Уровень C1"]
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=level)] for level in levels] + [[KeyboardButton(text="Отмена")]],
        resize_keyboard=True
    )

#














My_Profile = ["Git Hub"]


# async def inline_profile(): #создали асинхронную функцию
#     keyboard = InlineKeyboardBuilder()
#     for profile in My_Profile: #rage для предметов в моих предметах
#         keyboard.add(InlineKeyboardButton(text=profile, url="https://github.com/mar1k123?tab=repositories")) # добавили инлайн кнопки и в них ссылка
#     return keyboard.adjust(1).as_markup() #adjust (2 or ....) - сколько кнопок будет в одном ряду, а as_markup() по дефолту
#
#
#
# def main_menu_button(user_telegram_id: int):
#     button = KeyboardButton(text="📜 Главное меню")
#     keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
#     return keyboard
#
#
# def add_button(user_telegram_id: int):
#     button = KeyboardButton(text="Add words")
#     keyboard = ReplyKeyboardMarkup(keyboard=[[button]])
#     return keyboard