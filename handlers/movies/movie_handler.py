import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hide_link, bold, italic

from keyboards.movies_keyboards import get_first_page_movies_keyboard, get_second_page_movies_keyboard, \
    get_movie_buttons
from filters.callback_factories import PageCallbackFactory, KeyboardMovieCallBackFactory

from handlers.movies.titles_search import get_list_of_movies_for_keyboard
from handlers.search import SearchStates

from models.movie import Movie

router = Router()


@router.message(SearchStates.waiting_for_movie_title)
async def search_movie_title_handler(message: Message, state: FSMContext):
    movies, number_of_movies = await get_list_of_movies_for_keyboard(message.text)
    await state.set_state(SearchStates.FirstPage)
    await state.set_data({"search_query": message.text})
    await message.answer(f" 🔍  <b>Results » {message.text}</b>\n",
                         reply_markup=get_first_page_movies_keyboard(movies, number_of_movies))
    logging.info(f"Movie title: {message.text} , State: {await state.get_state()}")


@router.callback_query(PageCallbackFactory.filter(F.type == "movie" and F.page == 1))
async def movies_first_page_callback_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.FirstPage)
    logging.info(f"Callback query: {query.data} , State: {await state.get_state()}")
    search_query = await state.get_data()
    movies, number_of_movies = await get_list_of_movies_for_keyboard(search_query.get("search_query"))
    await query.message.edit_text(f" 🔍  <b>Results » {search_query.get('search_query')}</b>\n",
                                  reply_markup=get_first_page_movies_keyboard(movies, number_of_movies))


@router.callback_query(PageCallbackFactory.filter(F.type == "movie" and F.page == 2))
async def movies_second_page_callback_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.SecondPage)
    logging.info(f"Callback query: {query.data} , State: {await state.get_state()}")
    search_query = await state.get_data()
    movies, number_of_movies = await get_list_of_movies_for_keyboard(search_query.get("search_query"))
    await query.message.edit_text(f" 🔍  <b>Results » {search_query.get('search_query')}</b>\n",
                                  reply_markup=get_second_page_movies_keyboard(movies, number_of_movies))


@router.callback_query(KeyboardMovieCallBackFactory.filter())
async def movie_callback_handler_first_page(query: CallbackQuery, callback_data: KeyboardMovieCallBackFactory,
                                            state: FSMContext):
    logging.info(f"Callback query: {callback_data.tmdb_id}")
    movie = Movie(tmdb_id=callback_data.tmdb_id)
    await movie.get_movie_details()
    await query.message.edit_text(f"<b>{movie.title}</b>" + "\n\n" + f"<i>{movie.overview}</i>\n\n" + movie.poster_url,
                                  reply_markup=get_movie_buttons(
                                      page=1 if await state.get_state() == SearchStates.FirstPage else 2))
    await query.answer(" 🎬  Movie")
