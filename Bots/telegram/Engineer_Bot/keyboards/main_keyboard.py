from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="личный кабинет")
    kb.button(text="заказы")
    kb.button(text="правила")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def account_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="штрафы")
    kb.button(text="заработано за последние 10 дней")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def orders_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="согласование")
    kb.button(text="предоплата")
    kb.button(text="стационар")
    kb.button(text="оприход")
    kb.button(text="отчет")
    kb.button(text="назад")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def back_to_orders_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="назад к заказам")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def agreement_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="удалось согласовать")
    kb.button(text="отказ")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def prepayment_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="да")
    kb.button(text="нет")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def report_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="договор есть")
    kb.button(text="без договора")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def prepayment_type_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="наличные")
    kb.button(text="безнал")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

def report_type_engineer_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="бн оплачен")
    kb.button(text="наличные")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)