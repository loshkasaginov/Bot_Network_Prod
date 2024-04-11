from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_superuser_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="добавить куратора")
    kb.button(text="посмотреть всех кураторов")
    kb.button(text="удалить куратора")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)