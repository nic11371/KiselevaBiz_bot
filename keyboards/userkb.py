from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from handlers.texts import TEXTS


def start_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=TEXTS.get("welcome_btn"),
                callback_data="welcome_btn")]
        ]
    )
    return btn


def pay_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=TEXTS.get("pay_btn"),
                callback_data="pay_btn")]
        ]
    )
    return btn
