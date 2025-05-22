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
from typing import Dict, List, Optional, Tuple
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from keyboards import get_levels_keyboard
import keyboards as kb



# from html import escape
import asyncio
from datetime import datetime
from typing import Callable
import time
import csv
import os
import sqlite3
import sys
from database import init_common_words
import keyboards
import config


'''--------------------------------------------------------------------------------------------------------------------------------------'''
#SQLite functions

# Проверяет существование пользователя
def user_exists(user_id: int) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM users WHERE user_id = ?', (user_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists



# Добавляет нового пользователя
def add_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

# Добавляет слово в словарь пользователя
def add_word(user_id: int, aword: str, rword: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO words (user_id, aword, rword) VALUES (?, ?, ?)',
        (user_id, aword, rword)
    )
    conn.commit()
    conn.close()



# Получить личные слова пользователя
def get_user_words(user_id: int) -> Dict[str, str]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT aword, rword FROM words WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return {aword: rword for aword, rword in rows} if rows else {}


# Получает случайное английское слово пользователя
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



# Получает перевод по английскому слову
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
'''-----------------------------------------------------------------------------------------------------------------------------'''




'''CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV'''

# Получает общие слова из CSV по уровню
def get_common_words(level: str) -> Dict[str, str]:
    words = {}
    with open(COMMON_WORDS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['level'] == level:
                words[row['english']] = row['russian']
    return words



# Получает случайное слово из общих слов по уровню
def get_random_common_word(level: str) -> Optional[Tuple[str, str]]:
    words = []
    with open(COMMON_WORDS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['level'] == level:
                words.append((row['english'], row['russian']))
    return random.choice(words) if words else None



#Получить все доступные уровни из CSV файла с общими словами
def get_available_levels() -> List[str]:
    levels = set()  # Используем set для автоматического удаления дубликатов

    try:
        with open(COMMON_WORDS_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'level' in row:  # Проверяем наличие колонки level
                    levels.add(row['level'])
    except FileNotFoundError:
        print(f"Файл {COMMON_WORDS_CSV} не найден. Создаём новый...")
        init_common_words()  # Пытаемся создать файл, если его нет
        return get_available_levels()  # Рекурсивно вызываем себя после создания файла
    except Exception as e:
        print(f"Ошибка при чтении CSV файла: {e}")
        return []

    # Сортируем уровни в правильном порядке (A1, A2, B1, B2, C1, C2)
    sorted_levels = sorted(levels, key=lambda x: (x[0], int(x[1])))
    return sorted_levels

'''CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV CSV '''





class Words(StatesGroup):
    Translate = State()


class QuizStates(StatesGroup):
    SELECTING_MODE = State()
    SELECTING_LEVEL = State()
    ANSWERING = State()



class DeleteStates(StatesGroup):
    waiting_for_word = State()


running_processes = True
running_processes = True



class Words(StatesGroup):
    Original = State()
    Translate = State()
    Cnt = "cnt"



class Reg(StatesGroup):  #класс нужен для состояния
    Aword = State()
    Rword = State()


class TimerStates(StatesGroup):
    SETTING_INTERVAL = State()
    waiting_interval = State()


DB_PATH = os.path.join(os.path.dirname(__file__), 'vocabulary_bot.db')
COMMON_WORDS_CSV = "common_words.csv"
CSV_PATH = "Users.csv"
DICT_PATH = "Storage.py"







bot = Bot(token=config.BOT_TOKEN)
router = Router()
users = {}


user_timers = {}
user_attempts = {}


'''------------------------------------------------------------------------------------------------------------------------------------'''

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

'''-------------------------------------------------------------------------------------------------------------------------------------'''

# @router.message(F.text == "📜 Главное меню")
# async def main_menu_button_handler(msg: Message):
#     await msg.answer("Выбери одного из нас👇:",
#                      reply_markup=kb.main)


@router.message(Command("myid"))
async def get_my_id(message: Message):
    await message.answer(f"Ваш ID: `{message.from_user.id}`", parse_mode="Markdown")

'''----------------------------------------------------------------------------------------------------------------------------------------'''

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

'''-----------------------------------------------------------------------------------------------------------------------------------------'''

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

'''-----------------------------------------------------------------------------------------------------------------------------------'''


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

#Задать следующее слово
async def ask_next_word(msg: Message, state: FSMContext):
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


'''------------------------------------------------------------------------------------------------------------------------------------'''


#Начало проверки с выбором режима (личные and общие слова)
@router.message(Command("check"))
async def start_check(msg: Message, state: FSMContext):

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


# Обработка выбора режима
@router.message(QuizStates.SELECTING_MODE)
async def select_mode(msg: Message, state: FSMContext):
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

# Обработка выбора уровня для общих слов
@router.message(QuizStates.SELECTING_LEVEL)
async def select_level(msg: Message, state: FSMContext):
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


# Задаем следующее слово для проверки
async def ask_next_word(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    mode = data["mode"]

    if mode == "personal":
        aword = random.choice(list(words.keys()))
        rword = words[aword]
    else:  # common
        level = data["level"]
        word_pair = get_random_common_word(level)
        if not word_pair:
            await msg.answer("Не удалось получить слово. Попробуйте еще раз.")
            return
        aword, rword = word_pair

    await state.update_data({
        "correct_answer": rword,
        "current_word": aword,
        "attempts": 0
    })
    await msg.answer(f"Переведите слово: {aword}")


# Проверка ответа пользователя
@router.message(QuizStates.ANSWERING)
async def check_answer(msg: Message, state: FSMContext):
    data = await state.get_data()

    if msg.text.lower() in ["стоп", "stop", "отмена"]:
        await state.clear()
        return await msg.answer("Проверка завершена", reply_markup=ReplyKeyboardRemove())

    correct = data['correct_answer']
    user_answer = msg.text.lower()

    if user_answer == correct.lower():
        await msg.reply("✅ Верно!")
        return await ask_next_word(msg, state)

    attempts = data['attempts'] + 1
    if attempts >= 2:
        await msg.answer(f"❌ Правильно: {correct}")
        return await ask_next_word(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply("🔄 Попробуйте еще раз")


'''-------------------------------------------------------------------------------------------------------------------------------------------'''
class QuizStates(StatesGroup):
    # Состояния для обычной проверки (англ -> рус)
    SELECTING_MODE = State()
    SELECTING_LEVEL = State()
    ANSWERING = State()

    # Состояния для обратной проверки (рус -> англ)
    REVERSE_SELECTING_MODE = State()
    REVERSE_SELECTING_LEVEL = State()
    REVERSE_ANSWERING = State()

# Обработчик команды /check_reverse
@router.message(Command("check_reverse"))
async def start_check_reverse(msg: Message, state: FSMContext):
    await state.set_state(QuizStates.REVERSE_SELECTING_MODE)
    await msg.answer(
        "Выберите режим (перевод с русского на английский):",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Личные слова")],
                [KeyboardButton(text="Общий словарь")],
                [KeyboardButton(text="Отмена")]
            ],
            resize_keyboard=True
        )
    )


# Обработчик выбора режима для обратной проверки
@router.message(QuizStates.REVERSE_SELECTING_MODE)
async def handle_reverse_mode(msg: Message, state: FSMContext):
    if msg.text == "Отмена":
        await state.clear()
        return await msg.answer("Отменено", reply_markup=ReplyKeyboardRemove())

    if msg.text == "Личные слова":
        words = get_user_words(msg.from_user.id)
        if not words:
            await state.clear()
            return await msg.answer("Ваш словарь пуст. Добавьте слова через /add")

        await state.set_state(QuizStates.REVERSE_ANSWERING)
        await state.update_data({
            "words": words,
            "mode": "personal",
            "level": None
        })
        await msg.answer("Режим: личные слова", reply_markup=ReplyKeyboardRemove())
        return await ask_next_reverse_question(msg, state)

    if msg.text == "Общий словарь":
        await state.set_state(QuizStates.REVERSE_SELECTING_LEVEL)
        return await msg.answer(
            "Выберите уровень:",
            reply_markup=get_levels_keyboard()
        )

    await msg.answer("Пожалуйста, выберите вариант из клавиатуры")


# Обработчик выбора уровня для обратной проверки
@router.message(QuizStates.REVERSE_SELECTING_LEVEL)
async def handle_reverse_level(msg: Message, state: FSMContext):
    if msg.text == "Отмена":
        await state.clear()
        return await msg.answer("Отменено", reply_markup=ReplyKeyboardRemove())

    level = msg.text.replace("Уровень ", "").strip().upper()
    words = get_common_words(level)

    if not words:
        return await msg.answer(f"Для уровня {level} пока нет слов")

    await state.set_state(QuizStates.REVERSE_ANSWERING)
    await state.update_data({
        "words": words,
        "mode": "common",
        "level": level
    })
    await msg.answer(f"Выбран уровень: {level}", reply_markup=ReplyKeyboardRemove())
    await ask_next_reverse_question(msg, state)


# Функция для следующего вопроса при обратной проверке
async def ask_next_reverse_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    mode = data["mode"]

    if mode == "personal":
        aword = random.choice(list(words.keys()))
        rword = words[aword]
    else:
        level = data["level"]
        word_pair = get_random_common_word(level)
        if not word_pair:
            await msg.answer("Не удалось получить слово. Попробуйте еще раз.")
            return
        aword, rword = word_pair

    await state.update_data({
        "correct_answer": aword,
        "current_rword": rword,
        "attempts": 0
    })
    await msg.answer(f"Переведите на английский: {rword}")


# Обработчик ответов для обратной проверки
@router.message(QuizStates.REVERSE_ANSWERING)
async def check_reverse_answer(msg: Message, state: FSMContext):
    data = await state.get_data()

    if msg.text.lower() in ["стоп", "stop", "отмена"]:
        await state.clear()
        return await msg.answer("Проверка завершена", reply_markup=ReplyKeyboardRemove())

    correct = data['correct_answer'].lower()
    user_answer = msg.text.lower()

    if user_answer == correct:
        await msg.reply("✅ Верно!")
        return await ask_next_reverse_question(msg, state)

    attempts = data['attempts'] + 1
    if attempts >= 2:
        await msg.answer(f"❌ Правильно: {data['correct_answer']}")
        return await ask_next_reverse_question(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply("🔄 Попробуйте еще раз")

'''-------------------------------------------------------------------------------------------------------------------------------------'''








# @router.message(Command("check_db"))
# async def check_db(msg: Message):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#
#     # Проверяем количество слов для уровня C2
#     cursor.execute("SELECT COUNT(*) FROM common_words WHERE level = 'C2'")
#     count = cursor.fetchone()[0]
#
#     # Получаем примеры слов
#     cursor.execute("SELECT english, russian FROM common_words WHERE level = 'C2' LIMIT 5")
#     examples = cursor.fetchall()
#
#     conn.close()
#
#     await msg.answer(
#         f"В базе данных:\n"
#         f"Слов C2 уровня: {count}\n"
#         f"Примеры: {examples}"
#     )


















@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")