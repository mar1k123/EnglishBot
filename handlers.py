import random
from email.policy import default
from symtable import Class
# from aiogram.client.default import DefaultBotProperties, Default
# from aiogram.enums import ParseMode
from aiogram import Router, Bot, F, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, User, Chat, Update
from pyexpat.errors import messages
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext# нужен для управления состояниями
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
# В самом начале handlers.py
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Правильный импорт:




# from html import escape
import asyncio
from datetime import datetime
from typing import Callable
import time
import csv
import os
import sqlite3
import sys
from database import init_db
import keyboards




def get_levels_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

    for level in levels:
        builder.button(text=f"Уровень {level}")

    builder.button(text="Отмена")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)






class QuizStates(StatesGroup):
    SELECTING_MODE = State()
    SELECTING_LEVEL = State()
    ANSWERING = State()


DB_PATH = os.path.join(os.path.dirname(__file__), 'vocabulary_bot.db')








#Проверяет существование пользователя
def user_exists(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


#Добавляет нового пользователя
def add_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


#Добавляет слово в словарь пользователя
def add_word(user_id: int, aword: str, rword: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO words (user_id, aword, rword) VALUES (?, ?, ?)',
        (user_id, aword, rword)
    )
    conn.commit()
    conn.close()




def get_user_words(user_id: int) -> dict:
    """Получить личные слова пользователя"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT aword, rword FROM words WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {aword: rword for aword, rword in rows} if rows else {}

#Получает случайное английское слово пользователя
def get_random_aword(user_id: int) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT aword FROM words 
        WHERE user_id = ? 
        ORDER BY RANDOM() 
        LIMIT 1
    ''', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None



#Получает перевод по английскому слову
def get_rword_by_aword(user_id: int, aword: str) -> Optional[str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rword FROM words 
        WHERE user_id = ? AND aword = ?
    ''', (user_id, aword))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def get_common_words(level: str) -> dict:
    """Получить слова для уровня из базы данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT english, russian FROM common_words WHERE level = ?", (level,))
    rows = cursor.fetchall()
    conn.close()
    return {eng: rus for eng, rus in rows}






















class DeleteStates(StatesGroup):
    waiting_for_word = State()

CSV_PATH = "Users.csv"
DICT_PATH = "Storage.py"

running_processes = True

import keyboards as kb
# Def = DefaultBotProperties(parse_mode=ParseMode.HTML)

running_processes = True

class Words(StatesGroup):
    Original = State()
    Translate = State()
    Cnt = "cnt"

user_timers = {}


class Reg(StatesGroup):  #класс нужен для состояния
    Aword = State()
    Rword = State()


class TimerStates(StatesGroup):
    SETTING_INTERVAL = State()
    waiting_interval = State()


user_attempts = {}


import config

bot = Bot(token=config.BOT_TOKEN)
router = Router()
users = {}







@router.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    if not user_exists(user_id):
        add_user(user_id)
        await message.answer("Привет! Я бот для изучения слов. Я создам для вас персональный словарь.")
    else:
        await message.answer("С возвращением! Ваш персональный словарь готов к использованию.")
    await message.answer("\n<b>Доступные команды</b>:"
                     "\n/add - добавить английское слово в список и его перевод"
                     "\n/delete_word - удалить слово из словаря"
                     "\n/allwords - посмотреть все записанные слова"
                     "\n/check - бот выведет слова на английском (2 попытки)👇"
                     "\n/check_reverse - то же самое что и check, но выводит русские слова", parse_mode="HTML")





# @router.message(F.text == "📜 Главное меню")
# async def main_menu_button_handler(msg: Message):
#     await msg.answer("Выбери одного из нас👇:",
#                      reply_markup=kb.main)



@router.message(Command("myid"))
async def get_my_id(message: Message):
    await message.answer(f"Ваш ID: `{message.from_user.id}`", parse_mode="Markdown")



@router.message(Command("allwords"))
async def show_my_words(message: Message):
    user_id = message.from_user.id
    words = get_user_words(user_id)

    if not words:
        await message.answer("Ваш словарь пуст. Добавьте слова с помощью /add")
        return

    response = "📚 Ваш словарь:\n\n"
    for aword, rword in words.items():
        response += f"{aword} - {rword}\n"

    # Разбиваем на части, если сообщение слишком длинное
    if len(response) > 4000:
        for x in range(0, len(response), 4000):
            await message.answer(response[x:x + 4000])
    else:
        await message.answer(response)






@router.message(Command("add"))
async def step_one(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not user_exists(user_id):
        add_user(user_id)

    await state.set_state(Reg.Aword)
    await message.answer("Привет, введи английское слово:\n"
                         "<i>Ты всегда можешь прекратить ввод слов, вписав в чат <b>'Стоп'</b> или <b>'Stop'</b></i>",
                         parse_mode="HTML")


@router.message(Reg.Aword)
async def step_two(message: Message, state: FSMContext):
    user_text = message.text.strip()
    user_id = message.from_user.id

    if user_text.lower() in ["стоп", "stop"]:
        await message.answer("Вы приостановили ввод слов\nВыберите нужную вам команду👇")
        await state.clear()
        return

    await state.update_data(aword=user_text)
    await state.set_state(Reg.Rword)
    await message.answer("Введите перевод:")


@router.message(Reg.Rword)
async def step_four(message: Message, state: FSMContext):
    user_text = message.text.strip()
    user_id = message.from_user.id
    data = await state.get_data()
    aword = data.get('aword', '')

    if user_text.lower() in ["стоп", "stop"]:
        await message.answer("Вы приостановили ввод слов\nВыберите нужную вам команду👇")
        await state.clear()
        return

    # Добавляем слово в базу данных
    add_word(user_id, aword, user_text)

    await message.answer(f"<b>Добавлено слово:</b>\n{aword} - {user_text}\n\nВведите следующее английское слово:",
                         parse_mode="HTML")
    await state.set_state(Reg.Aword)












@router.message(Command("delete_word"))
async def delete_word_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not user_exists(user_id):
        await message.answer("❌ Ваш словарь пуст. Используйте /add")
        return

    await state.set_state(DeleteStates.waiting_for_word)
    await message.answer("📝 Введите английское слово для удаления:")


@router.message(DeleteStates.waiting_for_word)
async def process_deletion(message: Message, state: FSMContext):
    user_id = message.from_user.id
    word = message.text.strip()

    conn = None
    try:
        conn = sqlite3.connect('vocabulary_bot.db', timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        cursor = conn.cursor()

        # Проверка существования слова
        cursor.execute("""
            SELECT COUNT(*) FROM words 
            WHERE user_id = ? AND LOWER(aword) = LOWER(?)
        """, (user_id, word))

        if cursor.fetchone()[0] == 0:
            await message.answer(f"❌ Слово '{word}' не найдено")
            return

        # Удаление
        cursor.execute("""
            DELETE FROM words 
            WHERE user_id = ? AND LOWER(aword) = LOWER(?)
        """, (user_id, word))
        conn.commit()

        await message.answer(f"✅ Слово '{word}' удалено!")

    except sqlite3.OperationalError as e:
        if "locked" in str(e):
            await message.answer("🔒 База временно заблокирована. Попробуйте через 5 секунд")
        else:
            await message.answer(f"⚠️ Ошибка базы: {str(e)}")
    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {str(e)}")
    finally:
        if conn:
            conn.close()
    await state.clear()






async def ask_next_word(msg: Message, state: FSMContext):
    """Задать следующее слово"""
    data = await state.get_data()
    words = data['words']

    if not words:
        await state.clear()
        return await msg.answer("Слова закончились!", reply_markup=ReplyKeyboardRemove())

    aword = random.choice(list(words.keys()))
    await state.update_data({
        "current_word": aword,
        "attempts": 0,
        "correct_answer": words[aword],
        "remaining_words": {k: v for k, v in words.items() if k != aword}
    })
    await msg.answer(f"🇬🇧 Слово: {aword}\nВведите перевод:")






@router.message(Command("check"))
async def start_check(msg: Message, state: FSMContext):
    """Начало проверки с выбором режима"""
    await state.set_state(QuizStates.SELECTING_MODE)
    await msg.answer(
        "Выберите режим:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Личные слова")],
                [KeyboardButton(text="Общий словарь")],
                [KeyboardButton(text="Отмена")]
            ],
            resize_keyboard=True
        )
    )

@router.message(QuizStates.SELECTING_MODE)
async def select_mode(msg: Message, state: FSMContext):
    """Обработка выбора режима"""
    if msg.text == "Отмена":
        await state.clear()
        return await msg.answer("Отменено", reply_markup=ReplyKeyboardRemove())

    if msg.text == "Личные слова":
        words = get_user_words(msg.from_user.id)
        if not words:
            await state.clear()
            return await msg.answer("Ваш словарь пуст. Добавьте слова через /add")

        await state.set_state(QuizStates.ANSWERING)
        await state.update_data({
            "words": words,
            "mode": "personal",
            "level": None
        })
        await msg.answer("Режим: личные слова", reply_markup=ReplyKeyboardRemove())
        return await ask_next_word(msg, state)

    if msg.text == "Общий словарь":
        await state.set_state(QuizStates.SELECTING_LEVEL)
        return await msg.answer(
            "Выберите уровень:",
            reply_markup=get_levels_keyboard()
        )

    await msg.answer("Пожалуйста, выберите вариант из клавиатуры")


@router.message(QuizStates.SELECTING_LEVEL)
async def select_level(msg: Message, state: FSMContext):
    """Обработка выбора уровня"""
    if msg.text == "Отмена":
        await state.clear()
        return await msg.answer("Отменено", reply_markup=ReplyKeyboardRemove())

    level = msg.text.replace("Уровень ", "").strip().upper()
    words = get_common_words(level)

    if not words:
        return await msg.answer(f"Для уровня {level} пока нет слов")

    await state.set_state(QuizStates.ANSWERING)
    await state.update_data({
        "words": words,
        "mode": "common",
        "level": level
    })
    await msg.answer(f"Выбран уровень: {level}", reply_markup=ReplyKeyboardRemove())
    await ask_next_word(msg, state)


@router.message(QuizStates.ANSWERING)
async def check_answer(msg: Message, state: FSMContext):
    """Проверка ответа"""
    data = await state.get_data()

    if msg.text.lower() in ["стоп", "stop", "отмена"]:
        await state.clear()
        return await msg.answer("Проверка завершена", reply_markup=ReplyKeyboardRemove())

    correct = data['correct_answer']
    user_answer = msg.text.lower()

    if user_answer == correct.lower():
        await msg.reply("✅ Верно!")
        await state.update_data({"words": data.get("remaining_words", {})})
        return await ask_next_word(msg, state)

    attempts = data['attempts'] + 1
    if attempts >= 2:
        await msg.answer(f"❌ Правильно: {correct}")
        await state.update_data({"words": data.get("remaining_words", {})})
        return await ask_next_word(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply("🔄 Попробуйте еще раз")








@router.message(Command("check_reverse"))
async def random_rw(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if not user_exists(user_id):
        await msg.answer("Сначала добавьте слова с помощью команды /add")
        return

    words_dict = get_user_words(user_id)
    if not words_dict:
        await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
        return

    aword = random.choice(list(words_dict.keys()))
    rword = words_dict[aword]

    await state.set_state(Words.Translate)
    await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
    await msg.answer(rword)
    await msg.answer("Введите английский перевод:")


@router.message(Words.Translate)
async def check_english(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    aword = data["words"]
    cnt = data["cnt"]
    waiting_for_answer = data.get("waiting_for_answer", True)

    if not waiting_for_answer:
        return

    user_answer = msg.text.strip().lower()

    if user_answer == aword.lower():
        await msg.reply("✅ Отличная работа!")
        words_dict = get_user_words(user_id)
        if not words_dict:
            await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
            await state.clear()
            return

        aword = random.choice(list(words_dict.keys()))
        rword = words_dict[aword]
        await msg.answer(rword)
        await msg.answer("Введите английский перевод:")
        await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
    elif user_answer in ["стоп", "stop"]:
        await msg.answer("<b>Вы завершили серию</b>\nВыберите нужную вам команду👇", parse_mode="HTML")
        await state.clear()
    else:
        cnt += 1
        if cnt >= 2:
            await msg.answer(f"❌ Правильный перевод: <b>{aword}</b>", parse_mode="HTML")
            time.sleep(1)

            words_dict = get_user_words(user_id)
            if not words_dict:
                await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
                await state.clear()
                return

            aword = random.choice(list(words_dict.keys()))
            rword = words_dict[aword]
            await msg.answer(rword)
            time.sleep(1)
            await msg.answer("Введите английский перевод:")
            await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
        else:
            await msg.answer("🔄 Попробуй еще раз")
            await state.update_data(cnt=cnt, waiting_for_answer=True)




@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")