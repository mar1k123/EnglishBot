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
                     reply_markup=kb.main) #kb.main было для ReplyKB, settings для Inline KB + awain... для моей асинхронной функции в KB


@router.message(F.text == "📜 Главное меню")
async def main_menu_button_handler(msg: Message):
    await msg.answer("Выбери кого то из нас👇:",
                     reply_markup=kb.main)

@router.message(Command ("id"))
async def id_handler(msg: Message):
    await msg.answer(f"Ваш <b>Username</b>: {msg.from_user.username}\n"
                      f"Ваш Id: {msg.from_user.id}", parse_mode="HTML")


@router.message(Command("photo_id"))
async def photo_id_handler(msg: Message):
    await msg.answer("Отправь картинку и получи id")




@router.message(F.photo)
async def id_photo(msg: Message):
    await msg.reply(f"ID фотоc: {msg.photo[-1].file_id}")


@router.message(Command("my_logo"))
async def my_logo_handler(msg: Message):
    await msg.answer_photo(photo="AgACAgIAAxkBAAM1Zuwh_WXGTvXVHB1S7TOxhonWdf8AAs7eMRvSDGFLRZRnRZH6hO4BAAMCAAN4AAM2BA")


@router.callback_query(F.data == "My profile")
async def my_profile(callback: CallbackQuery):
    await callback.answer("") #короткое уведомление + show_alert=True делает всплывающее окно
    await callback.message.edit_text("Вот мой профиль на Git Hub:", reply_markup=await kb.inline_profile())




@router.callback_query(F.data == "My subjects")
async def my_profile(callback: CallbackQuery):
    await callback.answer("") #короткое уведомление + show_alert=True делает всплывающее окно
    await callback.message.edit_text("Вот что я сдаю на огэ:", reply_markup=await kb.inline_subject()) #пример колбэковского хэндлера+ инлайн ответ ,(edit_text для ответа), await перед путем ответа т.к функция асинхронная



@router.callback_query(F.data == "My commands")
async def my_commands(callback: CallbackQuery):
    await callback.answer("") #короткое уведомление + show_alert=True делает всплывающее окно
    await callback.message.edit_text("Вот какие команды я сделал:", reply_markup=await kb.inline_commands())




@router.message(Command("start"))
async def step_one(message: Message, state: FSMContext):
    await state.set_state(Reg.name)    # Устанавливаем состояние регистрации.имя
    users[f'{message.from_user.id}'] = User(message.from_user.id)
    await message.answer("👋Привет, для начала нужно зарегистрироваться\n\nВведите Ваше имя:")

@router.message(Reg.name)
async def step_two(message: Message, state: FSMContext):   # Словиле имя
    users[f'{message.from_user.id}'].name = message.text
    await state.set_state(Reg.Age)  #Изменили стоятояние на возраст
    await message.answer("Введите Ваш возраст:")


@router.message(Reg.Age)
async def step_three(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].age = int(message.text)

    await state.set_state(Reg.Sex)
    await message.answer("Введите Ваш пол:")




@router.message(Reg.Sex)
async def step_four(message: Message, state: FSMContext):
    users[f'{message.from_user.id}'].sex = message.text
    user = users[f'{message.from_user.id}']
    user.save()
    await message.answer(f"Спасибо, регистрация завершена😀.Для продолжения нажмите Главное меню👇\n\n{user}", reply_markup=kb.main_menu_button(message.from_user.id))
    await state.clear()


@router.message(Command("allusers"))
async def show_users(msg: Message):
    for user in User.get_all_users().values():
        await msg.answer(str(user))




@router.message()
async def noCommands_handler(msg: Message):
    await msg.reply("Такой команды нету")