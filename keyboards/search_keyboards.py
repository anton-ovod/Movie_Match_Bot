from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_factories import BackCallbackFactory, SearchCallbackFactory


def get_type_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=" 🎬 Movie", callback_data=SearchCallbackFactory(type="movie"))
    keyboard.button(text=" 📺 TV Show", callback_data=SearchCallbackFactory(type="tv"))
    keyboard.button(text=" 👤 Person", callback_data=SearchCallbackFactory(type="person"))
    keyboard.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="home"))

    keyboard.adjust(3, 1)
    return keyboard.as_markup()


def get_only_back_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=" ⬅️ Back", callback_data=BackCallbackFactory(to="search"))

    keyboard.adjust(1)
    return keyboard.as_markup()
