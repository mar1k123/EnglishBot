from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext    # нужен для управления состояниями



import keyboards as kb
from user import User


class Reg(StatesGroup):    #класс нужен для состояния
    name = State()
    Age = State()
    Sex = State()


import config

bot = Bot(token=config.BOT_TOKEN)
router = Router()
users = {}

@router.message(Command("hi"))
async def start_handler(msg: Message):
    await msg.answer("Привет, я бот тестировщик,\nвыбери кого то из нас👇:",
                     reply_markup=kb.main)