from aiogram.fsm.state import State, StatesGroup


class QuizStates(StatesGroup):
    SELECTING_MODE = State()
    SELECTING_LEVEL = State()
    ANSWERING = State()
    CONTEXT_ANSWERING = State()
    REVERSE_SELECTING_MODE = State()
    REVERSE_SELECTING_LEVEL = State()
    REVERSE_ANSWERING = State()
    right_cnt = "right_cnt"
    wrong_cnt = "wrong_cnt"


class DeleteStates(StatesGroup):
    waiting_for_word = State()


class Reg(StatesGroup):
    Aword = State()
    SuggestTranslation = State()
    Rword = State()


class TimerStates(StatesGroup):
    SETTING_INTERVAL = State()
    waiting_interval = State()
