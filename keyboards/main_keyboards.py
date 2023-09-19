from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters.callback_factories import BackCallbackFactory


def get_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="❓  Help", callback_data="help")
    keyboard.button(text="📚  About", callback_data="about")
    keyboard.button(text="🔍  Search", callback_data="search")
    keyboard.button(text="🍿  Cinema", callback_data="cinema")
    keyboard.button(text="🌟  Discover", callback_data="discover")
    keyboard.button(text="⚙️  Settings", callback_data="settings")

    keyboard.adjust(2)
    return keyboard.as_markup()


def get_home_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="🏠 Home", callback_data=BackCallbackFactory(to="home"))

    keyboard.adjust(1)
    return keyboard.as_markup()
