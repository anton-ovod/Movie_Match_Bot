import logging
import json

from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.search_keyboards import get_type_keyboard, get_only_back_button
from keyboards.movies_keyboards import get_first_page_movies_keyboard, get_second_page_movies_keyboard

from filters.callback_factories import SearchCallbackFactory, PageCallbackFactory

from handlers.movie_search import get_list_of_movies_for_keyboard

router = Router()


class SearchStates(StatesGroup):
    waiting_for_movie_title = State()
    FirstPage = State()
    SecondPage = State()


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
    await state.clear()
    await state.set_state(SearchStates.waiting_for_movie_title)
    await query.answer(" I'm ready to search for movies!")


@router.message(SearchStates.waiting_for_movie_title)
async def search_movie_title_handler(message: Message, state: FSMContext):
    movies, number_of_movies = await get_list_of_movies_for_keyboard(message.text)
    await message.answer(f" 🔍  <b>Results » {message.text}</b>\n",
                         reply_markup=get_first_page_movies_keyboard(movies, number_of_movies))
    await state.set_state(SearchStates.FirstPage)
    await state.update_data(search_query=message.text)


@router.callback_query(PageCallbackFactory.filter(F.type == "movie" and F.page == 1))
async def movies_first_page_callback_handler(query: CallbackQuery, state: FSMContext):
    search_query = await state.get_data()
    movies, number_of_movies = await get_list_of_movies_for_keyboard(search_query.get("search_query"))
    await query.message.edit_text(f" 🔍  <b>Results » {search_query.get('search_query')}</b>\n",
                                  reply_markup=get_first_page_movies_keyboard(movies, number_of_movies))
    await state.set_state(SearchStates.FirstPage)


@router.callback_query(PageCallbackFactory.filter(F.type == "movie" and F.page == 2))
async def movies_second_page_callback_handler(query: CallbackQuery, state: FSMContext):
    search_query = await state.get_data()
    movies, number_of_movies = await get_list_of_movies_for_keyboard(search_query.get("search_query"))
    await query.message.edit_text(f" 🔍  <b>Results » {search_query.get('search_query')}</b>\n",
                                  reply_markup=get_second_page_movies_keyboard(movies, number_of_movies))
    await state.set_state(SearchStates.SecondPage)
