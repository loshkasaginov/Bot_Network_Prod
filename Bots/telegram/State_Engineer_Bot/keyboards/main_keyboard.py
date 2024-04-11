from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_state_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="личный кабинет")
    kb.button(text="заказы")
    kb.button(text="правила")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def state_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="посмотреть доступные заказы")
    kb.button(text="посмотреть личные заказы")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)