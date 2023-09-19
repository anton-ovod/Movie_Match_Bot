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
    logging.info(f"User's nickname: {message.from_user.username}")
    await message.answer(
        "<b>Welcome to MovieMatcherBot!</b> 🎬🤖\n\n"
        "I'm here to help you find your perfect movie match.\n"
        "Whether you're in the mood for action-packed adventures or heartwarming romances, I've got you covered. "
        "Just let me know your preferences, and I'll suggest the best movies for you.\n\n",
        reply_markup=get_main_keyboard())


@router.message(Command("about"))
async def start_command_handler(message: Message):
    await message.answer("<b>🎬 Movie Match Bot - About 🎬</b>\n\n"

                         "Welcome to <i>Movie Match Bot</i>! We're here to help you discover the perfect movies based "
                         "on your preferences.\n\n"
                         
                         "<b>🔍 Key Features:</b>\n"
                         "- Personalized movie recommendations\n"
                         "- Explore trending, top-rated, and upcoming films\n"
                         "- Search for movies by title, genre, and cast\n"
                         "- Search for TV shows by title, genre, and cast\n"
                         "- Search for person profiles on <a href='https://www.themoviedb.org/'>TMDb</a> by name\n"
                         "- Explore airing today, top-rated, and popular TV shows\n\n"

                         "<b>📊 Data Sources — API's:</b>\n"
                         "• <a href='https://developer.themoviedb.org/docs'>TMDb</a>\n"
                         "• <a href='https://www.omdbapi.com/'>OMDb</a>\n"
                         "• <a href='https://www.justwatch.com/'>JustWatch.com</a>\n\n"

                         "<b>❓ Need Help?</b>\n"
                         "We have a dedicated support bot to assist you with any questions, issues, or feedback "
                         "related to our project. Just send a message to our <i>Support Bot</i> to get quick "
                         "assistance.\n\n"

                         "<b>🔐 Privacy:</b>\n"
                         "We respect your privacy. Your data is securely handled and not shared with third parties.\n\n"

                         "<b>🌐 Join Our Community:</b>\n"
                         "- Join our Telegram community: <a "
                         "href='https://t.me/filmatcherchannel'>https://t.me/filmatcherchannel</a>\n\n"

                         "Enjoy discovering new movies with <i>Movie Match Bot</i>! 🍿🎥", disable_web_page_preview=True)

# help, settings commands need to be added
