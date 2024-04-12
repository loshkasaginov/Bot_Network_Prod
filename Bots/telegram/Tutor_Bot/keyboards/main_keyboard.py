from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="инженеры")
    kb.button(text="стационар")
    kb.button(text="заказы")
    kb.button(text="стадии")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def engineers_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="добавить инженера")
    # kb.button(text="посмотреть инженера")
    kb.button(text="посмотреть всех инженеров")
    kb.button(text="удалить инженера")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def orders_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="добавить заказ")
    kb.button(text="посмотреть заказ")
    kb.button(text="посмотреть все заказы")
    kb.button(text="посмотреть все заказы по дате")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def stationary_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="стационарные инженеры")
    kb.button(text="заказы в стационаре")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def stationary_engineer_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="добавить стационарного инженера")
    # kb.button(text="посмотреть стационарного инженера")
    kb.button(text="посмотреть всех стационарных инженеров")
    kb.button(text="удалить стационарного инженера")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def stationary_orders_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="изменить приоритет на заказ")
    kb.button(text="посмотреть все заказы в стационаре")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def stages_tutor_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="согласование")
    kb.button(text="предоплата")
    kb.button(text="оприход")
    kb.button(text="отчет")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)