from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pyexpat.errors import messages
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.context import FSMContext    # нужен для управления состояниями



import keyboards as kb
from user import User


class Reg(StatesGroup):    #класс нужен для состояния
    Aword = State()
    Rword = State()


import config

bot = Bot(token=config.BOT_TOKEN)
router = Router()
users = {}

@router.message(Command("hi"))
async def start_handler(msg: Message):
    await msg.answer("Привет, я бот тестировщик,\nвыбери кого то из нас👇:",
                     reply_markup=kb.main) #kb.main было для ReplyKB, settings для Inline KB + awain... для моей асинхронной функции в KB


@router.message(F.text == "📜 Главное меню")
async def main_menu_button_handler(msg: Message):
    await msg.answer("Выбери кого то из нас👇:",
                     reply_markup=kb.main)



@router.callback_query(F.data == "My profile")
async def my_profile(callback: CallbackQuery):
    await callback.answer("") #короткое уведомление + show_alert=True делает всплывающее окно
    await callback.message.edit_text("Вот мой профиль на Git Hub:", reply_markup=await kb.inline_profile())



@router.message(Command("start"))
async def step_one(message: Message, state: FSMContext):
    await state.set_state(Reg.Aword)
    users[f'{message.from_user.id}'] = User(message.from_user.id)
    await message.answer("👋Привет, введи англ слово: \n")


@router.message(Reg.Aword)
async def step_two(message: Message, state: FSMContext):   # Словиле имя
    users[f'{message.from_user.id}'].Aword = message.text
    await state.set_state(Reg.Rword)
    await message.answer("Введите перевод:")




@router.message(Reg.Rword)
async def step_four(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].Rword = message.text
    user = users[f'{message.from_user.id}']
    user.save()
    await message.answer(f"Ты записал слова😀.Для продолжения нажмите Главное меню👇\n\n{user}", reply_markup=kb.main_menu_button(message.from_user.id))
    await state.set_state(Reg.Aword)
    await message.answer("Введите англ слово")






@router.message(Command("allusers"))
async def show_users(msg: Message):
    for user in User.get_all_users().values():
        await msg.answer(str(user))










@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")