import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.search_keyboards import get_type_keyboard, get_only_back_button

from filters.callback_factories import SearchCallbackFactory

router = Router()


class SearchStates(StatesGroup):
    waiting_for_movie_title = State()
    movie_pagination = State()
    movie_overview = State()


@router.callback_query(F.data == "search")
async def search_callback_handler(query: CallbackQuery):
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text(" 🔍  Search\n\n"
                                  "Choose what you want to search for: ",
                                  reply_markup=get_type_keyboard())
    await query.answer(" 🔍  Search")


@router.callback_query(SearchCallbackFactory.filter(F.type == "movie"))
async def search_movie_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(" 🔍  Search » 🎬  Movie\n\n"
                                  "Simply enter the title of the movie you're searching for, and I'll do my utmost to "
                                  "provide you with a list of matching results\n\n"
                                  "<b>For instance: The Matrix</b>", reply_markup=get_only_back_button())
    await state.clear()
    await state.set_state(SearchStates.waiting_for_movie_title)
    await query.answer(" I'm ready to search for movies!")
