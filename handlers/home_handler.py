import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.main_keyboards import get_home_button

router = Router()


@router.callback_query(F.data == "help")
async def help_callback_handler(query: CallbackQuery):
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text("<b>🎬 Movie Match Bot - Help 🎬</b>\n\n"

                                  "I'm here to assist you with various tasks. Here are some of the commands you can use:\n\n"

                                  "<b>/start</b> — Start using the bot.\n"
                                  "<b>/about</b> — Get general info about the bot.\n"
                                  "<b>/settings</b> — Configure bot settings.\n"
                                  "<b>/help</b> — Get some usage examples.\n\n"
                                  "Usage Examples:\n"
                                  "<b>Search Movie by Title:</b> <i>Search ➡️ Movie</i>\n"
                                  "<b>Search TV Show by Title:</b> <i>Search ➡️ Show</i>\n"
                                  "<b>Search TV Person Profile by Name:</b> <i>Search ➡️ Person</i>\n\n"

                                  "<b>Discover Movie by Genre or Cast:</b> <i>Discover ➡️ Movie ➡️ cast / genre</i>\n"
                                  "<b>Discover TV Show by Genre or Cast:</b> <i>Discover ➡️ Show ➡️ cast / genre</i>\n"
                                  "<b>Discover Top Rated Films or TV Shows:</b> <i>Discover ➡️ Movie / Show ➡️ Top "
                                  "Rated</i>\n"
                                  "<b>Discover Trending Films:</b> <i>Discover ➡️ Movies ➡️ Trending</i>\n"
                                  "<b>Discover Upcoming Films:</b> <i>Discover ➡️ Movies ➡️ Upcoming</i>\n"
                                  "<b>Discover Airing Today TV Shows:</b> <i>Discover ➡️ Shows ➡️ Airing Today</i>\n\n"

                                  "If you need assistance, have questions, or want to report issues, feel free to contact our "
                                  "support bot at <a "
                                  "href='https://t.me/film_matcher_bot'>Support bot</a>\n\n"

                                  "Enjoy using Movie Match Bot 🥰"
                                  , disable_web_page_preview=True,
                                  reply_markup=get_home_button())
    await query.answer(" ❓ Help")


@router.callback_query(F.data == "about")
async def about_callback_handler(query: CallbackQuery):
    await query.message.edit_text("<b>🎬 Movie Match Bot - About 🎬</b>\n\n"

                                  "Welcome to <i>Movie Match Bot</i>! We're here to help you discover the perfect "
                                  "movies based"
                                  "on your preferences.\n\n"

                                  "<b>🔍 Key Features:</b>\n"
                                  "- Personalized movie recommendations\n"
                                  "- Explore trending, top-rated, and upcoming films\n"
                                  "- Search for movies by title, genre, and cast\n"
                                  "- Search for TV shows by title, genre, and cast\n"
                                  "- Search for person profiles on <a href='https://www.themoviedb.org/'>TMDb</a> by "
                                  "name\n"
                                  "- Explore airing today, top-rated, and popular TV shows\n\n"

                                  "<b>📊 Data Sources — API's:</b>\n"
                                  "• <a href='https://developer.themoviedb.org/docs'>TMDb</a>\n"
                                  "• <a href='https://www.omdbapi.com/'>OMDb</a>\n"
                                  "• <a href='https://www.justwatch.com/'>JustWatch.com</a>\n\n"

                                  "<b>❓ Need Help?</b>\n"
                                  "We have a dedicated support bot to assist you with any questions, issues, "
                                  "or feedback"
                                  "related to our project. Just send a message to our <a href = "
                                  "'https://t.me/film_matcher_bot'>Support Bot</a> to "
                                  "get quick"
                                  "assistance.\n\n"

                                  "<b>🔐 Privacy:</b>\n"
                                  "We respect your privacy. Your data is securely handled and not shared with third "
                                  "parties.\n\n"

                                  "<b>🌐 Join Our Community:</b>\n"
                                  "- Join our Telegram community: <a "
                                  "href='https://t.me/filmatcherchannel'>https://t.me/filmatcherchannel</a>\n\n"

                                  "Enjoy discovering new movies with <i>Movie Match Bot</i>! 🍿🎥",
                                  disable_web_page_preview=True,
                                  reply_markup=get_home_button())
    await query.answer(" 📚 About")


@router.callback_query(F.data == "settings")
async def settings_callback_handler(query: CallbackQuery):
    await query.answer(" ⚙️ Settings not implemented yet", show_alert=True)


@router.callback_query(F.data == "cinema")
async def cinema_callback_handler(query: CallbackQuery):
    await query.answer(" 🍿 Cinema not implemented yet", show_alert=True)


@router.callback_query(F.data == "discover")
async def discover_callback_handler(query: CallbackQuery):
    await query.answer(" 🌟 Discover not implemented yet", show_alert=True)
