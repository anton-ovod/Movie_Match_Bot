import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from keyboards.back_keyboard import get_back_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboard import get_main_keyboard
router = Router()


class SearchState(StatesGroup):
    mainMenu = State()
    search = State()


@router.callback_query(F.data == "search")
async def callback_query_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.search)
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text("What movie are you looking for?",
                                  reply_markup=get_back_keyboard())
    await query.answer("Ok, let's search for a movie!")


@router.callback_query(F.data == "back")
async def callback_query_handler(query: CallbackQuery, state: FSMContext):
    await state.set_state(SearchState.mainMenu)
    logging.info(f"Callback query: {query.data}")
    await query.message.edit_text("Main menu",
                                  reply_markup=get_main_keyboard())
    await query.answer("Ok, let's go back to the main menu!")
