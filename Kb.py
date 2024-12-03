from aiogram.types import (ReplyKeyboardMarkup,KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton) #тож самое что и Reply только Inline
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder # Заимпортил билдер (он нужен для того, чтобы не менять знаения через код)

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мой профиль🌴", callback_data="My profile")],
    [InlineKeyboardButton(text="Мои предметы📖", callback_data="My subjects")] # cоздал инлайн кнопки с колбэком
])

settings = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="INF", url="https://inf-oge.sdamgia.ru/")],#При создании inlineKey board нужно что то (потом будет Callback)
    [InlineKeyboardButton(text="English", url="https://en-oge.sdamgia.ru/")],
    [InlineKeyboardButton(text="Russian", url="https://rus-oge.sdamgia.ru/")],
    [InlineKeyboardButton(text="Math", url="https://math-oge.sdamgia.ru/")]
])



My_Profile = ["Git Hub"]


async def inline_profile(): #создали асинхронную функцию
    keyboard = InlineKeyboardBuilder()
    for profile in My_Profile: #rage для предметов в моих предметах
        keyboard.add(InlineKeyboardButton(text=profile, url="https://github.com/mar1k123?tab=repositories")) # добавили инлайн кнопки и в них ссылка
    return keyboard.adjust(1).as_markup() #adjust (2 or ....) - сколько кнопок будет в одном ряду, а as_markup() по дефолту



My_Subject = ["INF", "English", "Russian", "Math","<<Назад"]

async def inline_subject(): #создали асинхронную функцию
    keyboard = InlineKeyboardBuilder()
    for subject in My_Subject: #rage для предметов в моих предметах
        keyboard.add(InlineKeyboardButton(text=subject, url="https://inf-oge.sdamgia.ru/")) # добавили инлайн кнопки и в них ссылка
    return keyboard.adjust(2).as_markup() #adjust (2 or ....) - сколько кнопок будет в одном ряду, а as_markup() по дефолту


def main_menu_button(user_telegram_id: int):
    button = KeyboardButton(text="📜 Главное меню")
    keyboard = ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True)
    return keyboard