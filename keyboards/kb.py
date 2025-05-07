from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def channels_kb(kb_list: list):
    inline_keyboard = []

    for channel_data in kb_list:
        label = channel_data.get('label')
        url = channel_data.get('url')
        if label and url:
            kb = [InlineKeyboardButton(text=label, url=url)]
            inline_keyboard.append(kb)

    inline_keyboard.append([
        InlineKeyboardButton(
            text="Проверить подписку", callback_data="check_subscription")
    ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)