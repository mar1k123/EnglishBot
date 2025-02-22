import random
from symtable import Class

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext# нужен для управления состояниями
import changer

running_processes = True

import keyboards as kb
from user import User

running = False

class Words(StatesGroup):
    Original = State()
    Translate = State()

class Reg(StatesGroup):  #класс нужен для состояния
    Aword = State()
    Rword = State()


import config

bot = Bot(token=config.BOT_TOKEN)
router = Router()
users = {}



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Hi, I am your english bot,\nChoose one of us👇:",
                     reply_markup=kb.main)


@router.message(F.text == "📜 Главное меню")
async def main_menu_button_handler(msg: Message):
    await msg.answer("Choose one of us👇:",
                     reply_markup=kb.main)





@router.message(Command("add"))
async def step_one(message: Message, state: FSMContext):
    await state.set_state(Reg.Aword)
    users[f'{message.from_user.id}'] = User(message.from_user.id)
    await message.answer("👋Hi, enter english word: \n")



@router.message(Reg.Aword)
async def step_two(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].Aword = message.text
    await state.set_state(Reg.Rword)
    await message.answer("Enter translate:")





@router.message(Reg.Rword)
async def step_four(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].Rword = message.text
    user = users[f'{message.from_user.id}']
    if message.text in ["Стоп","Stop"]:
        await state.clear()
    else:
        user.save()
        await message.answer(f"Current:\nEnter more\n{user}")
        await state.set_state(Reg.Aword)
        await message.answer("Enter english word")



@router.message(Command("allusers"))
async def show_users(msg: Message):
    for user in User.get_all_users().values():
        await msg.answer(str(user))



@router.message(Command("tryMe"))
async def random_ew(msg: Message, state: FSMContext):
    await state.set_state(Words.Original)
    a = random.choice(list((changer.data.keys())))
    await msg.answer(a)
    await msg.answer("Enter the answer:")
    await state.update_data(words = a)





@router.message(Words.Original)
async def translate(msg: Message, state: FSMContext):
    a = (await state.get_data())["words"]
    if msg.text.lower() == changer.data[f"{a}"]["Rword"].lower():
        await msg.reply("Great job")
        a = random.choice(list((changer.data.keys())))
        await msg.answer(a)
        await msg.answer("Enter the answer:")
        await state.update_data(words=a)
    else:
        await msg.answer("Try again")











@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")













