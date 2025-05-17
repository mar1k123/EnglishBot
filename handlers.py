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

# from html import escape
import asyncio
from datetime import datetime
from typing import Callable
import time
import csv
import os
import sqlite3


def init_db():
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()

    # Создаем таблицу пользователей, если ее нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY
    )
    ''')

    # Создаем таблицу слов, если ее нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        aword TEXT,
        rword TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    conn.commit()
    conn.close()


# Инициализируем базу данных при старте
init_db()

def user_exists(user_id):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


# Функция для добавления нового пользователя
def add_user(user_id):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()


# Функция для добавления слова
def add_word(user_id, aword, rword):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO words (user_id, aword, rword) VALUES (?, ?, ?)',
                   (user_id, aword, rword))
    conn.commit()
    conn.close()


# Функция для получения всех слов пользователя
def get_user_words(user_id):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT aword, rword FROM words WHERE user_id = ?', (user_id,))
    words = cursor.fetchall()
    conn.close()

    # Преобразуем в словарь для удобства
    words_dict = {aword: rword for aword, rword in words}
    return words_dict


# Функция для получения случайного английского слова пользователя
def get_random_aword(user_id):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT aword FROM words WHERE user_id = ? ORDER BY RANDOM() LIMIT 1', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Функция для получения перевода по английскому слову
def get_rword_by_aword(user_id, aword):
    conn = sqlite3.connect('vocabulary_bot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT rword FROM words WHERE user_id = ? AND aword = ?', (user_id, aword))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None





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
        await message.answer("Привет! Я бот для изучения слов. Я создал для вас персональный словарь.")
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















@router.message(Command("check"))
async def random_ew(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    if not user_exists(user_id):
        await msg.answer("Сначала добавьте слова с помощью команды /add")
        return

    words_dict = get_user_words(user_id)
    if not words_dict:
        await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
        return

    aword = random.choice(list(words_dict.keys()))
    await state.set_state(Words.Original)
    await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
    await msg.answer(aword)
    await msg.answer("Введите перевод:")


@router.message(Words.Original)
async def translate(msg: Message, state: FSMContext):
    user_id = msg.from_user.id
    data = await state.get_data()
    aword = data["words"]
    cnt = data["cnt"]
    waiting_for_answer = data.get("waiting_for_answer", True)

    if not waiting_for_answer:
        return

    rword = get_rword_by_aword(user_id, aword)
    if not rword:
        await msg.answer("Произошла ошибка. Попробуйте снова.")
        await state.clear()
        return

    user_answer = msg.text.strip().lower()

    if user_answer == rword.lower():
        await msg.reply("✅ Отличная работа!")
        words_dict = get_user_words(user_id)
        if not words_dict:
            await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
            await state.clear()
            return

        aword = random.choice(list(words_dict.keys()))
        await msg.answer(aword)
        await msg.answer("Введите перевод:")
        await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
    elif user_answer in ["стоп", "stop"]:
        await msg.answer("<b>Вы завершили серию</b>\nВыберите нужную вам команду👇", parse_mode="HTML")
        await state.clear()
    else:
        cnt += 1
        if cnt >= 2:
            await msg.answer(f"❌ Правильный перевод: <b>{rword}</b>", parse_mode="HTML")
            time.sleep(1)

            words_dict = get_user_words(user_id)
            if not words_dict:
                await msg.answer("Ваш словарь пуст. Добавьте слова с помощью команды /add")
                await state.clear()
                return

            aword = random.choice(list(words_dict.keys()))
            await msg.answer(aword)
            time.sleep(1)
            await msg.answer("Введите перевод:")
            await state.update_data(words=aword, cnt=0, waiting_for_answer=True)
        else:
            await msg.answer("🔄 Попробуй еще раз")
            await state.update_data(cnt=cnt, waiting_for_answer=True)










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
















@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")