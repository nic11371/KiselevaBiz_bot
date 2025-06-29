import os
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from handlers.texts import TEXTS
from dotenv import load_dotenv


load_dotenv()


def start_btn():
    btn = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=TEXTS.get("welcome_btn"),
                callback_data="welcome_btn")]
        ]
    )
    return btn


def pay_btn(user_id: int, url_pay, text_btn) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text_btn, url=url_pay)]
    ])
    return kb
