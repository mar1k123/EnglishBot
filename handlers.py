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
import changer
# from html import escape
import asyncio
from datetime import datetime
from typing import Callable


running_processes = True

import keyboards as kb
from user import User
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
async def start_handler(msg: Message):
    await msg.answer("Привет, Я твой <i>English bot</i>, помогу тебе выучить английский быстрее✔"
                     "\n\n<b>Доступные команды</b>:"
                     "\n/add - добавить английское слово в список и его перевод"
                     "\n/check - бот выведет слова на английском (2 попытки)👇", parse_mode="HTML")



@router.message(F.text == "📜 Главное меню")
async def main_menu_button_handler(msg: Message):
    await msg.answer("Выбери одного из нас👇:",
                     reply_markup=kb.main)





@router.message(Command("add"))
async def step_one(message: Message, state: FSMContext):
    await state.set_state(Reg.Aword)
    users[f'{message.from_user.id}'] = User(message.from_user.id)
    await message.answer("Привет, введи английское слово:\n"
                         "<i>Ты всегда можешь прекратить ввод слов, вписав в чат <b>'Cтоп'</b> или <b>'Stop'</b> 2 раза\n</i>", parse_mode="HTML")



@router.message(Reg.Aword)
async def step_two(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].Aword = message.text
    await state.set_state(Reg.Rword)
    await message.answer("Введите перевод:")





@router.message(Reg.Rword)
async def step_four(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].Rword = message.text
    user = users[f'{message.from_user.id}']
    if message.text in ["Стоп","Stop"]:
        await message.answer("Вы приостановили ввод слов\nВыберите нужную вам команду👇")
        await state.clear()
    else:
        user.save()
        await message.answer(f"<b>Текущее</b>:\n{user}Введите больше", parse_mode="HTML")
        await state.set_state(Reg.Aword)
        await message.answer("Введите англ. слово")



@router.message(Command("allusers"))
async def show_users(msg: Message):
    for user in User.get_all_users().values():
        await msg.answer(str(user))


@router.message(Command("check"))
async def random_ew(msg: Message, state: FSMContext):
    await state.set_state(Words.Original)
    a = random.choice(list(changer.data.keys()))
    await msg.answer(a)
    await msg.answer("Введите ответ:")
    await state.update_data(words=a, cnt=0, waiting_for_answer=True)


@router.message(Words.Original)
async def translate(msg: Message, state: FSMContext):
    data = await state.get_data()
    a = data["words"]
    cnt = data["cnt"]
    waiting_for_answer = data.get("waiting_for_answer", True)

    if waiting_for_answer:
        if msg.text.lower() == changer.data[a]["Rword"].lower():
            await msg.reply("✅ Отличная работа!")
            a = random.choice(list(changer.data.keys()))
            await msg.answer(a)
            await msg.answer("Введите ответ:")
            await state.update_data(words=a, cnt=0, waiting_for_answer=True)
        elif msg.text.lower() in ["стоп", "stop"]:
            await msg.answer("<b>Вы завершили серию</b>\nВыберите нужную вам команду👇", parse_mode="HTML")
            await state.clear()
        else:
            cnt += 1
            if cnt >= 2:
                await msg.answer(f"❌ Правильный перевод: {changer.data[a]['Rword']}")
                a = random.choice(list(changer.data.keys()))
                await msg.answer(a)
                await msg.answer("Введите ответ:")
                await state.update_data(words=a, cnt=0, waiting_for_answer=True)
            else:
                await msg.answer("🔄 Попробуй еще раз")
                await state.update_data(cnt=cnt, waiting_for_answer=True)
    else:
        await state.update_data(waiting_for_answer=True)










@router.message(Command("check_reverse"))
async def random_rw(msg: Message, state: FSMContext):
    await state.set_state(Words.Translate)
    a = random.choice(list(changer.data.keys()))
    russian_word = changer.data[a]["Rword"]
    await msg.answer(russian_word)
    await msg.answer("Введите английский перевод:")
    await state.update_data(words=a, cnt=0, waiting_for_answer=True)


@router.message(Words.Translate)
async def check_english(msg: Message, state: FSMContext):
    data = await state.get_data()
    a = data["words"]
    cnt = data["cnt"]
    waiting_for_answer = data.get("waiting_for_answer", True)

    if waiting_for_answer:
        if msg.text.lower() == a.lower():
            await msg.reply("✅ Отличная работа!")
            a = random.choice(list(changer.data.keys()))
            russian_word = changer.data[a]["Rword"]
            await msg.answer(russian_word)
            await msg.answer("Введите английский перевод:")
            await state.update_data(words=a, cnt=0, waiting_for_answer=True)
        elif msg.text.lower() in ["стоп", "stop"]:
            await msg.answer("<b>Вы завершили серию</b>\nВыберите нужную вам команду👇", parse_mode="HTML")
            await state.clear()
        else:
            cnt += 1
            if cnt >= 2:
                await msg.answer(f"❌ Правильный перевод: {a}")
                a = random.choice(list(changer.data.keys()))
                russian_word = changer.data[a]["Rword"]
                await msg.answer(russian_word)
                await msg.answer("Введите английский перевод:")
                await state.update_data(words=a, cnt=0, waiting_for_answer=True)
            else:
                await msg.answer("🔄 Попробуй еще раз")
                await state.update_data(cnt=cnt, waiting_for_answer=True)
    else:
        await state.update_data(waiting_for_answer=True)









@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")











