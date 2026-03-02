import asyncio

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove

from bot_instance import bot, router
from database import (
    get_hard_words,
    get_user_level,
    init_user_stats,
    pick_srs_word,
    update_word_stats,
)
from keyboards import (
    get_levels_keyboard,
    get_translation_choice_keyboard,
    reminder_interval_keyboard,
    reminder_main_keyboard,
    stop_rkb,
)
from services.common_words import get_common_words
from services.context_service import get_context_sentence, highlight_target_word
from services.reminder_service import (
    ensure_reminders_table,
    reminder_disable,
    reminder_enable,
)
from services.translation_service import (
    ENGLISH_PATTERN,
    RUSSIAN_PATTERN,
    STOP_BUTTON_TEXT,
    get_accepted_answers,
    is_stop_requested,
    suggest_translation_en_ru,
)
from services.user_words import (
    add_user,
    add_word,
    get_random_aword,
    get_rword_by_aword,
    get_user_words,
    user_exists,
)
from states.bot_states import DeleteStates, QuizStates, Reg, TimerStates

'''------------------------------------------------------------------------------------------------------------------------------------'''

@router.message(StateFilter("*"), F.text.func(is_stop_requested))
async def stop_active_flow(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "\u23F9 \u0414\u0435\u0439\u0441\u0442\u0432\u0438\u0435 \u043e\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d\u043e.",
        reply_markup=ReplyKeyboardRemove(),
    )

@router.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name  # Получаем имя пользователя
    welcome_text = (
        f"👋 <b>Привет, {first_name}!</b>\n\n"
        "Я твой помощник в изучении английских слов.\n"
        "Храню твой словарь и помогаю улучшать прогресс.\n\n"
        "✨ <b>Что я умею:</b>\n"
        "📝 /add - добавить новое слово и перевод\n"
        "📚 /allwords - показать все твои слова\n"
        "🗑️ /delete_word - удалить слово из словаря\n"
        "🧠 /check - тренировка: английский -> русский\n"
        "🧩 /check_context - перевод слова в контексте предложения\n"
        "🔁 /check_reverse - тренировка: русский -> английский\n"
        "📊 /stats - показать статистику и точность\n"
        "🔥 /hard_words - показать сложные слова\n"
        "🏆 /achievements - показать твой текущий уровень\n"
        "⏰ /reminder N - включить таймер напоминаний в минутах (пример: /reminder 3)\n"
        "🔕 /reminder off - отключить напоминания\n\n"
        "🚀 Начни с /add, чтобы добавить первое слово."
    )

    if not user_exists(user_id):
        add_user(user_id)
        # Для новых пользователей добавляем небольшое руководство
        await message.answer(welcome_text, parse_mode="HTML")
        await message.answer(
            "💡 <b>Совет:</b> Попробуй добавить свое первое слово командой:\n"
            "<code>/add apple - яблоко</code>\n\n"
            "Или просто отправь <code>/add</code> и я помогу тебе добавить слово!",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            f"🎉 <b>С возвращением, {first_name}!</b>\n\n"
            "Твой персональный словарь готов к использованию!\n\n" + welcome_text,
            parse_mode="HTML"
        )


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
ENGLISH_PATTERN = re.compile(r'^[a-zA-Z\s\'-]+$')
RUSSIAN_PATTERN = re.compile(r"^[\u0400-\u04FF\s'-]+$")

@router.message(Command("add"))
async def step_one(message: Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not user_exists(user_id):
        add_user(user_id)

    await state.set_state(Reg.Aword)
    await message.answer(
        f"🌟 <b>{first_name}, давайте добавим новое слово!</b>\n\n"
        "📝 <i>Введите английское слово (только латинские буквы):</i>\n\n"
        "▫️ Для отмены напишите <code>стоп</code> или <code>stop</code>",
        parse_mode="HTML",
        reply_markup=stop_rkb
    )

@router.message(Reg.Aword)
async def step_two(message: Message, state: FSMContext):
    user_text = message.text.strip()
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if user_text.lower() in ["стоп", "stop"]:
        await message.answer(
            "⏸ <b>Ввод приостановлен</b>\n\n"
            "Вы можете продолжить добавление слов командой /add",
            parse_mode="HTML"
        )
        await state.clear()
        return

    # Проверка на английские символы
    if not ENGLISH_PATTERN.fullmatch(user_text):
        await message.answer(
            "⚠️ <b>Пожалуйста, введите слово на английском языке!</b>\n"
            "Используйте только латинские буквы.\n\n"
            "Попробуйте еще раз:",
            parse_mode="HTML"
        )
        return  # Не меняем состояние, остаемся в Aword

    await state.update_data(aword=user_text)
    suggested = await asyncio.to_thread(suggest_translation_en_ru, user_text)

    if suggested:
        await state.update_data(suggested_translation=suggested)
        await state.set_state(Reg.SuggestTranslation)
        await message.answer(
            f"🤖 <b>Предлагаемый перевод для</b> <code>{user_text}</code>:\n"
            f"<code>{suggested}</code>\n\n"
            "Выберите действие:",
            parse_mode="HTML",
            reply_markup=get_translation_choice_keyboard(suggested),
        )
    else:
        await state.set_state(Reg.Rword)
        await message.answer(
            f"🔄 <b>{first_name}, теперь введите русский перевод для слова:</b>\n"
            f"<code>{user_text}</code>\n\n"
            "📌 Можно ввести несколько вариантов перевода через запятую\n"
            "⚠️ <i>Только русские буквы!</i>",
            parse_mode="HTML",
            reply_markup=stop_rkb,
        )


@router.message(Reg.SuggestTranslation)
async def step_three_suggested_translation(message: Message, state: FSMContext):
    user_text = (message.text or "").strip()
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    data = await state.get_data()
    aword = data.get("aword", "")
    suggested = data.get("suggested_translation", "")

    if user_text.lower() in ["стоп", "stop", "❌ отмена", "отмена"]:
        await message.answer(
            "⏸ <b>Ввод приостановлен</b>\n\n"
            "Вы можете продолжить добавление слов командой /add",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        return

    if user_text.startswith("✅ Использовать"):
        add_word(user_id, aword, suggested)
        await send_word_added_message(message, aword, suggested, first_name)
        await state.set_state(Reg.Aword)
        await message.answer("Введите следующее английское слово:", reply_markup=stop_rkb)
        return

    if "вручную" in user_text.lower():
        await state.set_state(Reg.Rword)
        await message.answer(
            f"🔄 <b>{first_name}, теперь введите русский перевод для слова:</b>\n"
            f"<code>{aword}</code>\n\n"
            "📌 Можно ввести несколько вариантов перевода через запятую\n"
            "⚠️ <i>Только русские буквы!</i>",
            parse_mode="HTML",
            reply_markup=stop_rkb,
        )
        return

    await message.answer(
        "Пожалуйста, выберите один из вариантов кнопкой ниже.",
        reply_markup=get_translation_choice_keyboard(suggested),
    )

@router.message(Reg.Rword)
async def step_four(message: Message, state: FSMContext):
    user_text = message.text.strip()
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    data = await state.get_data()
    aword = data.get('aword', '')

    if user_text.lower() in ["стоп", "stop"]:
        await message.answer(
            "⏸ <b>Ввод приостановлен</b>\n\n"
            "Вы можете продолжить добавление слов командой /add",
            parse_mode="HTML"
        )
        await state.clear()
        return

    # Проверка на русские символы
    if not RUSSIAN_PATTERN.fullmatch(user_text):
        await message.answer(
            "⚠️ <b>Пожалуйста, введите перевод на русском языке!</b>\n"
            "Используйте только кириллические буквы.\n\n"
            f"Введите русский перевод для слова <code>{aword}</code>:",
            parse_mode="HTML"
        )
        return  # Не меняем состояние, остаемся в Rword

    # Добавляем слово в базу данных
    add_word(user_id, aword, user_text)
    await send_word_added_message(message, aword, user_text, first_name)
    await state.set_state(Reg.Aword)

'''-----------------------------------------------------------------------------------------------------------------------------------'''

@router.message(Command("delete_word"))
async def delete_word_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    if not user_exists(user_id):
        await message.answer(
            f"📭 <b>{first_name}, ваш словарь пуст!</b>\n\n"
            "Добавьте слова командой /add чтобы начать обучение",
            parse_mode="HTML"
        )
        return

    await state.set_state(DeleteStates.waiting_for_word)
    await message.answer(
        f"🗑 <b>{first_name}, введите слово для удаления:</b>\n\n"
        "• Для отмены напишите <code>стоп</code>",
        parse_mode="HTML",
        reply_markup=stop_rkb,
    )


@router.message(DeleteStates.waiting_for_word)
async def process_deletion(message: Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    word = message.text.strip()

    if word.lower() in ["стоп", "stop"]:
        await message.answer("❌ Удаление отменено")
        await state.clear()
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH, timeout=10)
        conn.execute("PRAGMA journal_mode=WAL")
        cursor = conn.cursor()

        # Проверка существования слова
        cursor.execute("""
            SELECT COUNT(*) FROM words 
            WHERE user_id = ? AND LOWER(aword) = LOWER(?)
        """, (user_id, word))

        count = cursor.fetchone()[0]
        if count == 0:
            await message.answer(
                f"🔍 <b>Слово '{word}' не найдено!</b>\n\n"
                "Проверьте правильность написания или посмотрите все слова командой /allwords",
                parse_mode="HTML"
            )
            return

        # Удаление
        cursor.execute("""
            DELETE FROM words 
            WHERE user_id = ? AND LOWER(aword) = LOWER(?)
        """, (user_id, word))
        conn.commit()

        await message.answer(
            f"✅ <b>Успешно удалено!</b>\n\n"
            f"Слово <code>{word}</code> больше не в вашем словаре\n\n"
            f"Можете удалить ещё слова или ввести <code>стоп</code>",
            parse_mode="HTML"
        )

    except sqlite3.OperationalError as e:
        error_msg = "🔒 База временно заблокирована. Попробуйте через 5 секунд" if "locked" in str(
            e) else f"⚠️ Ошибка базы: {str(e)}"
        await message.answer(error_msg)
    except Exception as e:
        await message.answer(f"⚠️ Неожиданная ошибка: {str(e)}")
    finally:
        if conn:
            conn.close()


'''------------------------------------------------------------------------------------------------------------------------------------'''
# Начало проверки с выбором режима
@router.message(Command("check"))
async def start_check(msg: Message, state: FSMContext):
    await state.set_state(QuizStates.SELECTING_MODE)
    await msg.answer(
        "📚 <b>Выберите режим проверки:</b>",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔒 Личные слова")],
                [KeyboardButton(text="🌍 Общий словарь")],
                [KeyboardButton(text="❌ Отмена")],
                [KeyboardButton(text=STOP_BUTTON_TEXT)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        ),
        parse_mode="HTML"

    )


# Обработка выбора режима
@router.message(QuizStates.SELECTING_MODE)
async def select_mode(msg: Message, state: FSMContext):
    if msg.text == "❌ Отмена":
        await state.clear()
        return await msg.answer(
            "🚫 Проверка отменена",
            reply_markup=ReplyKeyboardRemove()
        )

    if msg.text == "🔒 Личные слова":
        words = get_user_words(msg.from_user.id)
        if not words:
            await state.clear()
            return await msg.answer(
                "📭 <b>Ваш словарь пуст</b>\n\n"
                "Добавьте слова через команду /add",
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove()
            )

        await state.set_state(QuizStates.ANSWERING)
        await state.update_data({
            "words": words,
            "mode": "personal",
            "level": None ,
            "right_cnt": 0 ,
            "wrong_cnt": 0,
        })

        await msg.answer(
            "🔐 <b>Режим: Личные слова</b>\n\n"
            "У вас будет 2 попытки для каждого слова",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        return await ask_next_word(msg, state)

    if msg.text == "🌍 Общий словарь":
        await state.set_state(QuizStates.SELECTING_LEVEL)
        return await msg.answer(
            "📊 <b>Выберите уровень сложности:</b>",
            reply_markup=get_levels_keyboard(),
            parse_mode="HTML"
        )

    await msg.answer(
        "⚠️ Пожалуйста, выберите вариант из предложенных",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔒 Личные слова")],
                [KeyboardButton(text="🌍 Общий словарь")],
                [KeyboardButton(text="❌ Отмена")],
                [KeyboardButton(text=STOP_BUTTON_TEXT)],
            ],
            resize_keyboard=True
        )
    )


# Обработка выбора уровня для общих слов
@router.message(QuizStates.SELECTING_LEVEL)
async def select_level(msg: Message, state: FSMContext):
    if msg.text == "❌ Отмена":
        await state.clear()
        return await msg.answer(
            "🚫 Проверка отменена",
            reply_markup=ReplyKeyboardRemove()
        )

    level = msg.text.replace("Уровень ", "").strip().upper()
    words = get_common_words(level)

    if not words:
        return await msg.answer(
            f"⚠️ Для уровня {level} пока нет слов",
            reply_markup=get_levels_keyboard()
        )

    await state.set_state(QuizStates.ANSWERING)
    await state.update_data({
        "words": words,
        "mode": "common",
        "level": level
    })
    await msg.answer(
        f"📈 <b>Выбран уровень:</b> {level}\n\n"
        "У вас будет 2 попытки для каждого слова",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await ask_next_word(msg, state)


async def ask_next_word(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    user_id = msg.from_user.id

    # Получаем или инициализируем множество использованных слов в состоянии
    used_words = data.get("used_words", set())

    # Для SRS берем только слова, еще не использованные в текущем цикле.
    available_words = {k: v for k, v in words.items() if k not in used_words}
    if not available_words:
        used_words = set()
        available_words = words.copy()

    candidates = list(available_words.keys())
    aword = pick_srs_word(user_id, candidates) or random.choice(candidates)
    rword = available_words[aword]

    # Добавляем слово в использованные
    used_words.add(aword)

    await state.update_data({
        "correct_answer": rword,
        "current_word": aword,
        "attempts": 0,
        "used_words": used_words  # Сохраняем обновленный список использованных слов
    })

    await msg.answer(
        f"🇬🇧 <b>Переведите слово:</b>\n<code>{aword}</code>",
        parse_mode="HTML",
        reply_markup = stop_rkb
    )


# Проверка ответа пользователя
@router.message(QuizStates.ANSWERING)
async def check_answer(msg: Message, state: FSMContext):
    data = await state.get_data()

    # Расширяем список команд для остановки
    if msg.text.lower() in ["стоп", "stop", "отмена", "❌"] or msg.text == "Стоп":
        await state.clear()
        return await msg.answer(
            "🏁 <b>Проверка завершена</b>",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )

    correct = data["correct_answer"]
    user_answer_normalized = _normalize_answer(msg.text or "")
    accepted_answers = await get_accepted_answers(
        source_word=data["current_word"],
        base_answer=correct,
        src_lang="en",
        dst_lang="ru",
    )

    if user_answer_normalized in accepted_answers:
        stats_event = update_word_stats(
            msg.from_user.id,
            data["current_word"],
            True
        )

        right_cnt = data.get("right_cnt", 0) + 1
        await state.update_data({"right_cnt": right_cnt})
        await msg.reply("✅ <b>Верно!</b>", parse_mode="HTML")
        if stats_event.get("hard_removed"):
            await msg.answer(
                f"🎉 Слово <code>{data['current_word']}</code> больше не считается сложным.\n"
                "Если снова будут ошибки, оно может вернуться в список сложных.",
                parse_mode="HTML"
            )
        return await ask_next_word(msg, state)



    attempts = data['attempts'] + 1
    if attempts >= 2:
        update_word_stats(
            msg.from_user.id,
            data["current_word"],
            False
        )
        wrong_cnt = data.get("wrong_cnt", 0) + 1
        await state.update_data({"wrong_cnt": wrong_cnt})

        await msg.reply(
            f"❌ <b>Правильный ответ:</b>\n<code>{correct}</code>",
            parse_mode="HTML"
        )
        return await ask_next_word(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply(
        "🔄 <b>Попробуйте еще раз</b>",
        parse_mode="HTML",
        reply_markup=stop_rkb  # Добавляем кнопку и при повторной попытке
    )


'''-------------------------------------------------------------------------------------------------------------------------------------------'''

@router.message(Command("check_context"))
async def start_check_context(msg: Message, state: FSMContext):
    words = get_user_words(msg.from_user.id)
    if not words:
        await state.clear()
        return await msg.answer(
            "📭 <b>Ваш словарь пуст</b>\n\n"
            "Добавьте слова через команду /add",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )

    await state.set_state(QuizStates.CONTEXT_ANSWERING)
    await state.update_data({
        "words": words,
        "used_context_words": set(),
        "right_cnt": 0,
        "wrong_cnt": 0,
    })
    await msg.answer(
        "🧩 <b>Режим: перевод в контексте</b>\n\n"
        "Я дам предложение на английском, а вы переведете выделенное слово.\n"
        "Для выхода нажмите кнопку <b>Стоп</b>.",
        parse_mode="HTML",
        reply_markup=stop_rkb,
    )
    await ask_next_context_word(msg, state)


async def ask_next_context_word(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data.get("words", {})
    used_words = data.get("used_context_words", set())
    user_id = msg.from_user.id

    available_words = {k: v for k, v in words.items() if k not in used_words}
    if not available_words:
        used_words = set()
        available_words = words.copy()

    candidates = list(available_words.keys())
    aword = pick_srs_word(user_id, candidates) or random.choice(candidates)
    rword = available_words[aword]
    used_words.add(aword)
    sentence = await asyncio.to_thread(get_context_sentence, aword)
    highlighted_sentence = highlight_target_word(sentence, aword)

    await state.update_data({
        "correct_answer": rword,
        "current_word": aword,
        "current_context_sentence": sentence,
        "attempts": 0,
        "used_context_words": used_words,
    })

    await msg.answer(
        "📝 <b>Контекст:</b>\n"
        f"<i>{highlighted_sentence}</i>\n\n"
        f"Переведите слово: <code>{aword}</code>",
        parse_mode="HTML",
        reply_markup=stop_rkb,
    )


@router.message(QuizStates.CONTEXT_ANSWERING)
async def check_context_answer(msg: Message, state: FSMContext):
    data = await state.get_data()
    if msg.text.lower() in ["стоп", "stop", "отмена", "❌"]:
        await state.clear()
        return await msg.answer(
            "🏁 <b>Тренировка в контексте завершена</b>",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove(),
        )

    correct = data["correct_answer"]
    user_answer_normalized = _normalize_answer(msg.text or "")
    accepted_answers = await get_accepted_answers(
        source_word=data["current_word"],
        base_answer=correct,
        src_lang="en",
        dst_lang="ru",
    )

    if user_answer_normalized in accepted_answers:
        stats_event = update_word_stats(
            msg.from_user.id,
            data["current_word"],
            True,
        )
        right_cnt = data.get("right_cnt", 0) + 1
        await state.update_data({"right_cnt": right_cnt})
        await msg.reply("✅ <b>Верно!</b>", parse_mode="HTML")
        if stats_event.get("hard_removed"):
            await msg.answer(
                f"🎉 Слово <code>{data['current_word']}</code> больше не считается сложным.\n"
                "Если снова будут ошибки, оно может вернуться в список сложных.",
                parse_mode="HTML",
            )
        return await ask_next_context_word(msg, state)

    attempts = data["attempts"] + 1
    if attempts >= 2:
        update_word_stats(
            msg.from_user.id,
            data["current_word"],
            False,
        )
        wrong_cnt = data.get("wrong_cnt", 0) + 1
        await state.update_data({"wrong_cnt": wrong_cnt})
        await msg.reply(
            f"❌ <b>Правильный ответ:</b>\n<code>{correct}</code>",
            parse_mode="HTML",
        )
        return await ask_next_context_word(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply(
        "🔄 <b>Попробуйте еще раз</b>",
        parse_mode="HTML",
        reply_markup=stop_rkb,
    )


'''-------------------------------------------------------------------------------------------------------------------------------------------'''

# Обработчик команды /check_reverse
@router.message(Command("check_reverse"))
async def start_check_reverse(msg: Message, state: FSMContext):
    await state.set_state(QuizStates.REVERSE_SELECTING_MODE)
    await msg.answer(
        "🔁 <b>Режим обратной проверки</b>\n\n"
        "<i>Перевод с русского на английский</i>\n\n"
        "Выберите источник слов:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔒 Личные слова")],
                [KeyboardButton(text="🌍 Общий словарь")],
                [KeyboardButton(text="❌ Отмена")],
                [KeyboardButton(text=STOP_BUTTON_TEXT)],
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        ),
        parse_mode="HTML"
    )


@router.message(QuizStates.REVERSE_SELECTING_MODE)
async def handle_reverse_mode(msg: Message, state: FSMContext):
    if msg.text == "❌ Отмена":
        await state.clear()
        return await msg.answer(
            "🚫 Проверка отменена",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )

    if msg.text == "🔒 Личные слова":
        words = get_user_words(msg.from_user.id)
        if not words:
            await state.clear()
            return await msg.answer(
                "📭 <b>Ваш словарь пуст</b>\n\n"
                "Добавьте слова через команду /add",
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove()
            )

        await state.set_state(QuizStates.REVERSE_ANSWERING)
        await state.update_data({
            "words": words,
            "mode": "personal",
            "level": None
        })
        await msg.answer(
            "🔐 <b>Режим: Личные слова</b>\n\n"
            "У вас будет 2 попытки для каждого слова",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
        return await ask_next_reverse_question(msg, state)

    if msg.text == "🌍 Общий словарь":
        await state.set_state(QuizStates.REVERSE_SELECTING_LEVEL)
        return await msg.answer(
            "📊 <b>Выберите уровень сложности:</b>",
            reply_markup=get_levels_keyboard(),
            parse_mode="HTML"
        )

    await msg.answer(
        "⚠️ Пожалуйста, выберите вариант из предложенных",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔒 Личные слова")],
                [KeyboardButton(text="🌍 Общий словарь")],
                [KeyboardButton(text="❌ Отмена")],
                [KeyboardButton(text=STOP_BUTTON_TEXT)],
            ],
            resize_keyboard=True
        )
    )

@router.message(QuizStates.REVERSE_SELECTING_LEVEL)
async def handle_reverse_level(msg: Message, state: FSMContext):
    if msg.text == "❌ Отмена":
        await state.clear()
        return await msg.answer(
            "🚫 Проверка отменена",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode="HTML"
        )

    level = msg.text.replace("Уровень ", "").strip().upper()
    words = get_common_words(level)

    if not words:
        return await msg.answer(
            f"⚠️ Для уровня {level} пока нет слов",
            reply_markup=get_levels_keyboard(),
            parse_mode="HTML"
        )

    await state.set_state(QuizStates.REVERSE_ANSWERING)
    await state.update_data({
        "words": words,
        "mode": "common",
        "level": level
    })
    await msg.answer(
        f"📈 <b>Выбран уровень:</b> {level}\n\n"
        "У вас будет 2 попытки для каждого слова",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )
    await ask_next_reverse_question(msg, state)


async def ask_next_reverse_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    words = data["words"]
    user_id = msg.from_user.id

    # Храним использованные английские слова, чтобы корректно работать и
    # с личным, и с общим словарем (в русском возможны дубликаты).
    used_words = data.get("used_reverse_words", set())
    available_words = {k: v for k, v in words.items() if k not in used_words}
    if not available_words:
        used_words = set()
        available_words = words.copy()
        if not available_words:
            await msg.answer("⚠️ Нет доступных слов для перевода.")
            return

    candidates = list(available_words.keys())
    aword = pick_srs_word(user_id, candidates) or random.choice(candidates)
    rword = available_words[aword]

    # Добавляем слово в использованные
    used_words.add(aword)

    await state.update_data({
        "correct_answer": aword,
        "current_rword": rword,
        "attempts": 0,
        "used_reverse_words": used_words
    })

    await msg.answer(
        f"🇷🇺 <b>Переведите на английский:</b>\n<code>{rword}</code>",
        parse_mode="HTML",
        reply_markup = stop_rkb
    )


@router.message(QuizStates.REVERSE_ANSWERING)
async def check_reverse_answer(msg: Message, state: FSMContext):
    data = await state.get_data()

    if msg.text.lower() in ["стоп", "stop", "отмена", "❌"]:
        await state.clear()
        return await msg.answer(
            "🏁 <b>Проверка завершена</b>",
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )

    correct = data["correct_answer"]
    user_answer_normalized = _normalize_answer(msg.text or "")
    accepted_answers = await get_accepted_answers(
        source_word=data["current_rword"],
        base_answer=correct,
        src_lang="ru",
        dst_lang="en",
    )

    if user_answer_normalized in accepted_answers:
        stats_event = update_word_stats(
            msg.from_user.id,
            data["correct_answer"],
            True
        )
        await msg.reply("✅ <b>Верно!</b>", parse_mode="HTML")
        if stats_event.get("hard_removed"):
            await msg.answer(
                f"🎉 Слово <code>{data['correct_answer']}</code> больше не считается сложным.\n"
                "Если снова будут ошибки, оно может вернуться в список сложных.",
                parse_mode="HTML"
            )
        return await ask_next_reverse_question(msg, state)

    attempts = data['attempts'] + 1
    if attempts >= 2:
        update_word_stats(
            msg.from_user.id,
            data["correct_answer"],
            False
        )
        await msg.reply(
            f"❌ <b>Правильный ответ:</b>\n<code>{data['correct_answer']}</code>",
            parse_mode="HTML"
        )
        return await ask_next_reverse_question(msg, state)

    await state.update_data({"attempts": attempts})
    await msg.reply("🔄 <b>Попробуйте еще раз</b>", parse_mode="HTML", reply_markup=stop_rkb)

'''----------------------------------------------------------------------------------------------------------------------------'''


@router.message(Command("stats"))
async def cmd_stats(msg: Message):
    user_id = msg.from_user.id
    init_user_stats(user_id)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT total_correct, total_wrong, learned_words
        FROM user_stats WHERE user_id = ?
    """, (user_id,))
    correct, wrong, learned = cursor.fetchone()
    conn.close()

    percent = round((correct / max(correct + wrong, 1)) * 100, 1)

    await msg.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"📚 Выучено слов: {learned}\n"
        f"✅ Правильных: {correct}\n"
        f"❌ Ошибок: {wrong}\n"
        f"🎯 Точность: {percent}%",
        parse_mode="HTML"
    )



'''-------------------------------------------------------------------------------------------------------------------------------------------'''

@router.message(Command("hard_words"))
async def cmd_hard_words(msg: Message):
    words = get_hard_words(msg.from_user.id)

    if not words:
        return await msg.answer("🎉 У вас нет сложных слов!")

    await msg.answer(
        "🔥 <b>Сложные слова:</b>\n\n"
        + "\n".join(words)
        + "\n\nℹ️ Слово убирается из этого списка после 10 правильных ответов на него.\n"
        + "Если снова будут ошибки, слово может вернуться в сложные.",
        parse_mode="HTML"
    )






'''-------------------------------------------------------------------------------------------------------------------------------------------'''


@router.message(Command("achievements"))
async def cmd_achievements(msg: Message):
    level = get_user_level(msg.from_user.id)

    titles = {
        1: "🌱 Новичок",
        2: "🥉 Ученик",
        3: "🥈 Продвинутый",
        4: "🥇 Эксперт",
        5: "🏆 Мастер"
    }

    await msg.answer(
        f"🏅 <b>Ваш уровень:</b> {titles[level]}\n\n"
        "Нажмите кнопку ниже, чтобы посмотреть как перейти на следующий уровень.",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="📈 Как повысить уровень")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    )


@router.message(F.text == "📈 Как повысить уровень")
async def achievements_levels_info(msg: Message):
    await msg.answer(
        "📚 <b>Описание уровней:</b>\n\n"
        "🌱 Новичок: 0–99 выученных слов\n"
        "🥉 Ученик: 100–199 выученных слов\n"
        "🥈 Продвинутый: 200–499 выученных слов\n"
        "🥇 Эксперт: 500–999 выученных слов\n"
        "🏆 Мастер: 1000+ выученных слов\n\n"
        "Чтобы перейти на следующий уровень, увеличивайте число выученных слов "
        "(слово считается выученным после 10 правильных ответов).",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove()
    )



'''-------------------------------------------------------------------------------------------------------------------------------------------'''



@router.message(Command("reminder"))
async def cmd_reminder(msg: Message, state: FSMContext):
    ensure_reminders_table()
    args = msg.text.split()

    # Backward compatibility: /reminder 3, /reminder off
    if len(args) > 1:
        raw_value = args[1].strip().lower()
        if raw_value == "off":
            reminder_disable(msg.from_user.id)
            await state.clear()
            return await msg.answer("🔕 Напоминания отключены", reply_markup=ReplyKeyboardRemove())

        try:
            minutes = int(raw_value)
        except ValueError:
            return await msg.answer("Нужно указать число минут. Пример: /reminder 3")

        if minutes <= 0:
            return await msg.answer("нтервал должен быть больше 0 минут.")

        reminder_enable(msg.from_user.id, minutes)
        await state.clear()
        return await msg.answer(
            f"⏰ Таймер установлен: каждые {minutes} мин.\n"
            f"Первое напоминание придет через {minutes} мин.",
            reply_markup=ReplyKeyboardRemove()
        )

    await state.set_state(TimerStates.SETTING_INTERVAL)
    await msg.answer(
        "⏰ Настройка напоминаний.\nВыберите действие:",
        reply_markup=reminder_main_keyboard()
    )


@router.message(TimerStates.SETTING_INTERVAL)
async def reminder_choose_action(msg: Message, state: FSMContext):
    text = (msg.text or "").strip().lower()

    if text.startswith("❌") or text in {"отмена", "cancel"}:
        await state.clear()
        return await msg.answer("Настройка напоминаний отменена.", reply_markup=ReplyKeyboardRemove())

    if text.startswith("🔕") or "выключ" in text:
        reminder_disable(msg.from_user.id)
        await state.clear()
        return await msg.answer("🔕 Напоминания отключены", reply_markup=ReplyKeyboardRemove())

    if text.startswith("🔔") or "включ" in text:
        await state.set_state(TimerStates.waiting_interval)
        await state.update_data(reminder_custom=False)
        return await msg.answer(
            "Выберите интервал напоминаний:",
            reply_markup=reminder_interval_keyboard()
        )

    await msg.answer("Выберите кнопку: включить, выключить или отмена.", reply_markup=reminder_main_keyboard())


@router.message(TimerStates.waiting_interval)
async def reminder_set_interval(msg: Message, state: FSMContext):
    text_raw = (msg.text or "").strip()
    text = text_raw.lower()
    data = await state.get_data()
    custom_mode = data.get("reminder_custom", False)

    if text.startswith("❌") or text in {"отмена", "cancel"}:
        await state.clear()
        return await msg.answer("Настройка напоминаний отменена.", reply_markup=ReplyKeyboardRemove())

    if text == "15 минут":
        minutes = 15
    elif text == "1 час":
        minutes = 60
    elif text == "5 часов":
        minutes = 300
    elif text.startswith("🛠") or "свое время" in text:
        await state.update_data(reminder_custom=True)
        return await msg.answer(
            "Введите интервал в минутах (например: 45).",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="❌ Отмена")],
                    [KeyboardButton(text=STOP_BUTTON_TEXT)],
                ],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )
    elif custom_mode:
        if not text.isdigit():
            return await msg.answer("Введите целое число минут, например: 45")
        minutes = int(text)
    else:
        return await msg.answer("Выберите кнопку с интервалом или 'Свое время'.", reply_markup=reminder_interval_keyboard())

    if minutes <= 0:
        return await msg.answer("нтервал должен быть больше 0 минут.")

    reminder_enable(msg.from_user.id, minutes)
    await state.clear()
    await msg.answer(
        f"⏰ Таймер установлен: каждые {minutes} мин.\n"
        f"Первое напоминание придет через {minutes} мин.",
        reply_markup=ReplyKeyboardRemove()
    )



'''-------------------------------------------------------------------------------------------------------------------------------------------'''
