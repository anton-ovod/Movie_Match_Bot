import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.search_keyboards import get_type_keyboard, get_only_back_button

from filters.callback_factories import SearchCallbackFactory

from handlers.movie_search import get_movies_by_title

router = Router()


class SearchStates(StatesGroup):
    waiting_for_movie_title = State()


@router.callback_query(F.data == "search")
async def search_callback_handler(query: CallbackQuery):
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text(" 🔍  Search\n\n"
                                  "Choose what you want to search for:\n",
                                  reply_markup=get_type_keyboard())
    await query.answer(" 🔍  Search")


@router.callback_query(SearchCallbackFactory.filter(F.type == "movie"))
async def search_movie_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(" 🔍  Search » 🎬  Movie\n\n"
                                  "Simply enter the title of the movie you're searching for, and I'll do my utmost to "
                                  "provide you with a list of matching results\n\n"
                                  "<b>For instance: The Matrix</b>", reply_markup=get_only_back_button())
    await state.set_state(SearchStates.waiting_for_movie_title)
    await query.answer(" I'm ready to search for movies!")


@router.message(SearchStates.waiting_for_movie_title)
async def search_movie_title_handler(message: Message, state: FSMContext):
    movies_data = await get_movies_by_title(message.text)
    await message.answer(f"Found {movies_data['total_results']} results for <b>{message.text}</b>\n")
    logging.info(movies_data['results'][0])
    await state.clear()
