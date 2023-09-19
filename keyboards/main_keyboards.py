from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❓  Help", callback_data="help")
    keyboard.button(text="🔍  Search", callback_data="search")
    keyboard.button(text="🍿  Cinema", callback_data="cinema")
    keyboard.button(text="🌟  Discover", callback_data="discover")
    keyboard.button(text="⚙️  Settings", callback_data="settings")

    keyboard.adjust(1, 2, 2)
    return keyboard.as_markup()
