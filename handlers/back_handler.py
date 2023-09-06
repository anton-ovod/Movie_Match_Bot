import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.main_keyboards import get_main_keyboard
from keyboards.search_keyboards import get_type_keyboard, get_only_back_button

from filters.callback_factories import BackCallbackFactory

from aiogram.fsm.context import FSMContext
from handlers.search import SearchStates

router = Router()


@router.callback_query(BackCallbackFactory.filter(F.to == "home"))
async def back_home_callback_handler(query: CallbackQuery):
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text("<b>Welcome to MovieMatcherBot!</b> 🎬🤖\n\n"
                                  "I'm here to help you find your perfect movie match.\n"
                                  "Whether you're in the mood for action-packed adventures or heartwarming "
                                  "romances, I've got you covered."
                                  "Just let me know your preferences, and I'll suggest the best movies for you.\n\n",
                                  reply_markup=get_main_keyboard())
    await query.answer(" 🏠 Home")


@router.callback_query(BackCallbackFactory.filter(F.to == "search"))
async def back_search_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(" 🔍  Search\n\n"
                                  "Choose what you want to search for:\n",
                                  reply_markup=get_type_keyboard())
    await state.clear()
    await query.answer(" 🔍  Search")


@router.callback_query(BackCallbackFactory.filter(F.to == "search:movie"))
async def back_search_callback_handler(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(" 🔍  Search » 🎬  Movie\n\n"
                                  "Simply enter the title of the movie you're searching for, and I'll do my "
                                  "utmost to"
                                  "provide you with a list of matching results\n\n"
                                  "<b>For instance: The Matrix</b>", reply_markup=get_only_back_button())
    await state.set_state(SearchStates.waiting_for_movie_title)
    await query.answer("Movies search")


@router.callback_query(BackCallbackFactory.filter(F.to == "close"))
async def back_close_callback_handler(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.delete()
    await query.answer("Closing... 🚪")
