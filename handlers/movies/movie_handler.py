import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.movies_keyboards import (get_page_of_movies_keyboard, get_back_button, get_movie_buttons)
from filters.callback_factories import PageCallbackFactory, KeyboardMovieCallBackFactory, MovieCallBackFactory

from handlers.search import SearchStates
from utils.imdb_api import get_movies_by_title, get_movie_details_tmdb
from utils.omdb_api import get_movie_details_omdb
from models.movie import Movie

router = Router()


@router.message(SearchStates.waiting_for_movie_title)
async def search_movie_title_handler(message: Message, state: FSMContext):
    movies = await get_movies_by_title(message.text)
    if movies:
        await state.set_data({"movies": movies, "search_query": message.text})
        await state.set_state(SearchStates.movie_pagination)
        await message.answer(f" 🔍  <b>Results » {message.text}</b>\n",
                             reply_markup=get_page_of_movies_keyboard(movies, page_number=1))
    else:
        await message.answer(" ‼️ No movies found, please try again ‼️ ", reply_markup=get_back_button())
        await state.clear()


@router.callback_query(PageCallbackFactory.filter(F.type == "movie"))
async def movies_first_page_callback_handler(query: CallbackQuery, callback_data: PageCallbackFactory,
                                             state: FSMContext):
    state_data = await state.get_data()
    movies = state_data.get("movies")
    search_query = state_data.get("search_query")
    await query.message.edit_text(f" 🔍  <b>Results » {search_query}</b>\n",
                                  reply_markup=get_page_of_movies_keyboard(movies, page_number=callback_data.page))
    await query.answer(f" 🔍 Page {callback_data.page}")


@router.callback_query(KeyboardMovieCallBackFactory.filter())
async def movie_callback_handler_first_page(query: CallbackQuery, callback_data: KeyboardMovieCallBackFactory):
    logging.info(f"Callback query: {query.data}")
    movie = Movie(tmdb_id=callback_data.tmdb_id)
    await get_movie_details_tmdb(movie)
    if movie.imdb_id:
        await get_movie_details_omdb(movie)

    logging.info(f"Movie: {movie.model_dump_json(indent=4)}")
    await query.message.edit_text(movie.message, parse_mode="HTML",
                                  reply_markup=get_movie_buttons(movie_data=movie, page=callback_data.page))
    await query.answer(f" 🔍  {movie.pretty_title}")


@router.callback_query(MovieCallBackFactory.filter(F.feature == "watch"))
async def providers_callback_handler(query: CallbackQuery, callback_data: MovieCallBackFactory):

    await query.answer(text="🗂 Recommendations")


# @router.callback_query(MovieCallBackFactory.filter(F.feature == "recommendations"))
# async def providers_callback_handler(query: CallbackQuery):
#     await query.answer(text="Not implemented yet", show_alert=True)
