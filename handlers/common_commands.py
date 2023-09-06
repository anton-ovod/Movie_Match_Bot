import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.main_keyboards import get_main_keyboard

router = Router()


@router.message(Command("start"))
async def start_command_handler(message: Message):
    user = message.from_user

    language = user.language_code or "en"

    logging.info(f"User's language: {language}")
    await message.answer(
        "<b>Welcome to MovieMatcherBot!</b> 🎬🤖\n\n"
        "I'm here to help you find your perfect movie match.\n"
        "Whether you're in the mood for action-packed adventures or heartwarming romances, I've got you covered. "
        "Just let me know your preferences, and I'll suggest the best movies for you.\n\n",
        reply_markup=get_main_keyboard())

# about, help, settings commands need to be added
